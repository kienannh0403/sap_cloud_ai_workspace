#!/usr/bin/env python3
"""Convert .docx / .xlsx / .xls FS documents to Markdown for skill document-markdown-converter.

Adapted from StormShynn/sap-abap-agent `reference/scripts/office_to_md.py` (MIT License,
https://github.com/StormShynn/sap-abap-agent). Changes: no mcp_sap_connect dependency, no
implicit in/ out/ folders (input and -o are required), UTF-8 stdout forced, .doc rejected
with a hint instead of a silent skip.

Why this script and not MarkItDown:
- .docx: embedded images (incl. EMF/WMF screenshots) are written to "<file>_assets/";
  MarkItDown drops them.
- .xlsx/.xls: every cell is read as text (dtype=str), so SAP codes keep leading zeros
  ("000000001234567890" stays as is, "1000" never becomes "1000.0", blanks stay blank).

Usage (from the workspace root, venv per the skill):
  ./.venv_markitdown/Scripts/python.exe .claude/scripts/office_to_md.py \
      "artifacts/targets/<T>/fs/<file>.docx" -o "artifacts/targets/<T>/fs/"
"""

import argparse
import re
import sys
from pathlib import Path

import mammoth
import markdownify
import pandas as pd

SUPPORTED_EXTENSIONS = {".docx", ".xlsx", ".xls"}

# EMF/WMF are Windows vector formats Office uses for pasted screenshots.
_EXTENSION_FIXUPS = {"x-emf": "emf", "x-wmf": "wmf", "svg+xml": "svg", "jpeg": "jpg"}

# Compound File Binary header: legacy .doc, or an encrypted / IRM-protected Office file.
_OLE_SIGNATURE = bytes.fromhex("d0cf11e0a1b11ae1")


def _clean_extension(content_type: str) -> str:
    ext = content_type.partition("/")[2].partition(";")[0].strip()
    return _EXTENSION_FIXUPS.get(ext, ext or "bin")


def convert_docx(input_path: Path, output_dir: Path):
    """Return (md path, number of extracted images, mammoth warnings)."""
    with input_path.open("rb") as f:
        if f.read(8) == _OLE_SIGNATURE:
            raise ValueError(
                "file is an OLE container, not a docx zip: either a legacy .doc renamed "
                "to .docx or a password/IRM-protected document - open it in Word, remove "
                "protection if any, Save As .docx, then convert again"
            )
    assets_dir = output_dir / f"{input_path.stem}_assets"
    counter = {"n": 0}

    def save_image(image):
        counter["n"] += 1
        ext = _clean_extension(image.content_type or "")
        filename = f"image{counter['n']:02d}.{ext}"
        assets_dir.mkdir(parents=True, exist_ok=True)
        with image.open() as src:
            (assets_dir / filename).write_bytes(src.read())
        return {"src": f"{assets_dir.name}/{filename}"}

    with input_path.open("rb") as f:
        result = mammoth.convert_to_html(
            f, convert_image=mammoth.images.img_element(save_image)
        )

    # Mammoth wraps every image in <p>, also inside table cells (td > p > img).
    # markdownify drops alt-less images in cells unless "p" keeps inline images.
    md_text = markdownify.markdownify(
        result.value, heading_style=markdownify.ATX, keep_inline_images_in=["p"]
    )
    md_text = re.sub(r"\n{3,}", "\n\n", md_text).strip() + "\n"

    output_dir.mkdir(parents=True, exist_ok=True)
    out_path = output_dir / f"{input_path.stem}.md"
    out_path.write_text(md_text, encoding="utf-8")

    warnings = [m.message for m in result.messages if m.type == "warning"]
    return out_path, counter["n"], warnings


def convert_xlsx(input_path: Path, output_dir: Path):
    """Return (md path, number of sheets). One Markdown table per sheet."""
    # dtype=str keeps SAP codes exactly as typed (no leading-zero loss, no 1000.0).
    engine = "xlrd" if input_path.suffix.lower() == ".xls" else "openpyxl"
    sheets = pd.read_excel(input_path, sheet_name=None, engine=engine, dtype=str)

    parts = []
    for sheet_name, df in sheets.items():
        parts.append(f"## {sheet_name}\n")
        html_table = df.to_html(index=False, na_rep="")
        parts.append(
            markdownify.markdownify(html_table, heading_style=markdownify.ATX).strip()
        )

    md_text = "\n\n".join(parts).strip() + "\n"

    output_dir.mkdir(parents=True, exist_ok=True)
    out_path = output_dir / f"{input_path.stem}.md"
    out_path.write_text(md_text, encoding="utf-8")
    return out_path, len(sheets)


def iter_input_files(inputs):
    files = []
    for p in inputs:
        if p.is_dir():
            for ext in sorted(SUPPORTED_EXTENSIONS):
                files.extend(sorted(p.glob(f"*{ext}")))
        elif p.suffix.lower() in SUPPORTED_EXTENSIONS:
            files.append(p)
        elif p.suffix.lower() == ".doc":
            print(
                f"[skip] {p}: legacy .doc is not supported - open it in Word and "
                "Save As .docx, then convert the .docx",
                file=sys.stderr,
            )
        else:
            print(f"[skip] {p}: unsupported format", file=sys.stderr)
    # Skip Office lock files (~$name.docx).
    return [f for f in files if not f.name.startswith("~$")]


def main():
    # Workspace paths contain non-ASCII characters; never depend on the console code page.
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(
        description="Convert .docx/.xlsx/.xls to Markdown (images and SAP codes preserved)."
    )
    parser.add_argument("inputs", nargs="+", type=Path, help="Input files or folders")
    parser.add_argument(
        "-o", "--output", type=Path, required=True, help="Output folder for .md and _assets/"
    )
    args = parser.parse_args()

    files = iter_input_files(args.inputs)
    if not files:
        print("No .docx/.xlsx/.xls file to convert.", file=sys.stderr)
        sys.exit(1)

    failed = 0
    for f in files:
        print(f"Converting: {f}")
        try:
            if f.suffix.lower() == ".docx":
                out_path, n_images, warnings = convert_docx(f, args.output)
                print(f"  -> {out_path} ({n_images} images in {out_path.stem}_assets/)")
                for w in warnings:
                    print(f"  [warning] {w}")
            else:
                out_path, n_sheets = convert_xlsx(f, args.output)
                print(f"  -> {out_path} ({n_sheets} sheets)")
        except Exception as e:  # report and continue with the next file
            failed += 1
            print(f"  [ERROR] {f}: {e}", file=sys.stderr)
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
