---
name: document-markdown-converter
description: Hướng dẫn tiền xử lý (pre-processing) tài liệu FS nhị phân (DOCX, XLSX, PDF, PPTX, HTML, v.v.) thành Markdown (MD) trước khi phân tích trong các workflow SAP — dùng `scripts/office_to_md.py` cho DOCX/XLSX (giữ ảnh, giữ mã số SAP) và MarkItDown cho PDF/PPTX/HTML. Sử dụng khi một tài liệu thiết kế FS/spec được cung cấp làm đầu vào cho workflow phân tích (fs-analytic, bug-fix...) — KHÔNG dùng cho các thao tác PDF/Word/Excel tổng quát (tạo, chỉnh sửa, merge file — việc đó thuộc các skill pdf/docx/xlsx chuyên dụng). Triggers: `markitdown`, `office_to_md`, `convert fs`, `parse FS document`, `tiền xử lý tài liệu FS`, `đọc file FS`, `convert docx sang md`, `convert excel sang md`.
---

# Document Markdown Converter

Guide for pre-processing binary Functional Specification (FS) documents into Markdown for token-efficient analysis.

## Core Objective

Never read raw binary files (`.pdf`, `.docx`, `.xlsx`) directly. Convert to structured Markdown first, then analyse the Markdown.

**Pick the tool by file type — this is not interchangeable:**

| Input | Tool | Why |
|---|---|---|
| `.docx` | `scripts/office_to_md.py` | Extracts embedded images to real files. MarkItDown destroys them. |
| `.xlsx` / `.xls` | `scripts/office_to_md.py` | Reads every cell as text. MarkItDown corrupts SAP numeric codes. |
| `.pdf` / `.pptx` / `.html` / `.csv` / `.msg` | MarkItDown CLI | `office_to_md.py` does not support these. |

## Environment

Both tools live in the same virtual environment, which already has every dependency (`mammoth`, `markdownify`, `pandas`, `openpyxl`, `xlrd` came in with `markitdown[all]`).

```bash
./.venv_markitdown/Scripts/markitdown.exe --version
```

This is a **Windows** venv: executables are in `Scripts/`, not `bin/`. If the command is not found, create the venv (requires Python >= 3.10):

```bash
python -m venv .venv_markitdown && ./.venv_markitdown/Scripts/pip.exe install 'markitdown[all]'
```

## 1. DOCX — use `office_to_md.py`, keep the images

```bash
./.venv_markitdown/Scripts/python.exe -X utf8 scripts/office_to_md.py \
  "FS/[Target]/[File].docx" -o "artifacts/targets/[Target]/build/"
```

Produces `[File].md` plus a sibling `[File]_assets/` folder holding the real embedded images, and prints how many it extracted.

Two invocation rules, both verified on this machine — skipping either one breaks the run:

- **`-X utf8` is mandatory.** The workspace path contains non-ASCII characters ("dự án"); without it Windows Python encodes stdout as cp1252 and the script dies with `UnicodeEncodeError: 'charmap' codec can't encode character 'ự'`.
- **Always pass the input path and `-o` explicitly.** The script's built-in defaults resolve to `in/` and `out/` one level *above* this workspace (it assumes it lives in `reference/scripts/`, not `scripts/`). Never rely on them.

### Why not MarkItDown for DOCX

Measured on `FS/ZPM01/PTB_GO_FS_FA_ZPM01_...docx`, same input file:

| | `office_to_md.py` | MarkItDown CLI |
|---|---|---|
| Images | **2 real PNGs on disk** (47 KB + 332 KB) | 1 line `![](data:image/png;base64...)` — a truncated placeholder, image data discarded |
| Table rows | 125 | 125 (identical) |

The 332 KB image was a legible Fiori screenshot with a business rule highlighted in red. MarkItDown's output made it unrecoverable. Tables come out the same either way, so **images are the entire reason** to prefer the script for `.docx`.

### Image caveats

- Filenames containing spaces or `( )` produce `![](My File (1)_assets/image01.png)` — an **unescaped link that will not resolve** in a Markdown viewer. The file is on disk and the Read tool opens it fine, which is all [Skill: fs-vision-extractor] needs. Do not trust the inline link.
- `.emf`/`.wmf` assets (screenshots pasted from the Windows/Office clipboard) are Windows vector formats that **do not render** in Markdown viewers or browsers. Open them via Word (Save as Picture) or convert to PNG. Say so explicitly rather than silently skipping the content.
- If a section produces images but no accompanying table or descriptive text, that section's meaning lives entirely in the picture — hand it to [Skill: fs-vision-extractor] and warn the user, never treat it as empty.

## 2. XLSX / XLS — never use MarkItDown

```bash
./.venv_markitdown/Scripts/python.exe -X utf8 scripts/office_to_md.py \
  "FS/[Target]/[File].xlsx" -o "artifacts/targets/[Target]/build/"
```

One Markdown table per sheet, each under an `## <SheetName>` heading.

MarkItDown reads Excel through pandas with inferred dtypes, which **silently corrupts SAP business codes**:

- `000000001234567890` → `1234567890` (leading zeros stripped)
- `1000` → `1000.0`
- empty cell → `NaN`

Material, Plant, Order and Batch numbers are all numeric-looking codes that may carry leading zeros. `office_to_md.py` avoids this by reading with `dtype=str` and rendering blanks as empty.

## 3. PDF / PPTX / other — MarkItDown CLI

```bash
./.venv_markitdown/Scripts/markitdown.exe "FS/[Target]/[File].pdf" \
  -o "artifacts/targets/[Target]/fs/fs_markdown.md"
```

Same image limitation applies: embedded pictures are lost. For a PDF whose content is largely diagrams or mockups, fall back to [Skill: fs-vision-extractor] on the original.

## 4. Verify before reporting success

Per `sap-dev-rule.md` §11, "it converted" is not evidence the content survived. Check, then report:

1. **Tables intact** — count rows (`grep -c '^|'`) and confirm no table is cut off mid-way.
2. **Business codes unchanged** (Excel, and any DOCX with data tables) — spot-check a few Material/Plant/Order values in the `.md` against the original file. A stripped leading zero here becomes a wrong requirement in the TS.
3. **Images accounted for** — compare the count the script printed against `ls [File]_assets/`, and name any section whose meaning is image-only.

## 5. Hand off to analysis

Once the `.md` exists, **stop reading the original document** — read `artifacts/targets/[Target]/fs/[File].md` instead. It preserves headings, lists and tables for Data Model and UI element extraction. Images in `[File]_assets/` go to [Skill: fs-vision-extractor] for transcription.
