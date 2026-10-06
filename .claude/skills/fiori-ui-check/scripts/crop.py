"""crop.py - cut a screenshot to the region a check needs before reading it (saves tokens).

python crop.py <png> <x0> <y0> <x1> <y1> [out.png]
python crop.py <png> --rows <y0> <y1> [out.png]        full-width band
Without out.png the result is written next to the input as <name>_crop.png. Prints the output path and size.
"""
import sys
from pathlib import Path

from PIL import Image

a = sys.argv[1:]
if len(a) < 3:
    sys.exit(__doc__)
src = Path(a[0])
im = Image.open(src)
if a[1] == "--rows":
    box, rest = (0, int(a[2]), im.width, int(a[3])), a[4:]
else:
    if len(a) < 5:
        sys.exit(__doc__)
    box, rest = tuple(int(v) for v in a[1:5]), a[5:]
box = (max(0, box[0]), max(0, box[1]), min(im.width, box[2]), min(im.height, box[3]))
out = Path(rest[0]) if rest else src.with_name(src.stem + "_crop.png")
im.crop(box).save(out)
print(f"{out} {box[2] - box[0]}x{box[3] - box[1]}")
