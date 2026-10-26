"""Photo Palette Sorter.

Drop in a folder of photos and this sorts them into subfolders by
dominant color, or pulls out a hex palette for a single image.

Usage:
    pip install Pillow
    python palette_sorter.py photos/            # sort into photos_sorted/
    python palette_sorter.py --palette img.jpg  # print the image's palette
    python palette_sorter.py --demo             # try it on generated images
"""

import argparse
import shutil
import sys
from collections import Counter
from pathlib import Path

try:
    from PIL import Image
except ImportError:  # pragma: no cover
    print("Pillow is required: pip install Pillow")
    sys.exit(1)

NAMED_COLORS = {
    "red": (220, 38, 38),
    "orange": (234, 88, 12),
    "yellow": (250, 204, 21),
    "green": (22, 163, 74),
    "blue": (37, 99, 235),
    "purple": (147, 51, 234),
    "pink": (236, 72, 153),
    "brown": (120, 53, 15),
    "black": (20, 20, 20),
    "white": (245, 245, 245),
    "gray": (128, 128, 128),
}

IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".webp", ".bmp"}


def dominant_color(path):
    """Most common color in the image, as an (r, g, b) tuple."""
    img = Image.open(path).convert("RGB").resize((100, 100))
    counts = img.getcolors(100 * 100)
    return max(counts, key=lambda c: c[0])[1]


def nearest_name(rgb):
    """Name of the closest basic color to an (r, g, b) tuple."""
    def dist(a, b):
        return sum((x - y) ** 2 for x, y in zip(a, b))

    return min(NAMED_COLORS, key=lambda name: dist(rgb, NAMED_COLORS[name]))


def palette(path, n=5):
    """Up to n distinct hex colors that best represent the image."""
    img = Image.open(path).convert("RGB").resize((100, 100))
    counts = sorted(img.getcolors(100 * 100), reverse=True)
    picked = []
    for _, rgb in counts:
        if all(sum((a - b) ** 2 for a, b in zip(rgb, other)) > 1500
               for other in picked):
            picked.append(rgb)
        if len(picked) == n:
            break
    return ["#%02x%02x%02x" % c for c in picked]


def sort_folder(src, dst):
    """Copy every image in src into dst/<dominant-color>/."""
    src, dst = Path(src), Path(dst)
    results = Counter()
    for path in sorted(src.iterdir()):
        if path.suffix.lower() not in IMAGE_EXTS:
            continue
        color = nearest_name(dominant_color(path))
        target = dst / color
        target.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, target / path.name)
        results[color] += 1
    return results


def demo():
    """Generate three solid-color images and sort them."""
    demo_dir = Path("demo_photos")
    demo_dir.mkdir(exist_ok=True)
    for name, rgb in [("sunset", (236, 72, 153)),
                      ("ocean", (37, 99, 235)),
                      ("lemon", (250, 204, 21))]:
        Image.new("RGB", (200, 200), rgb).save(demo_dir / f"{name}.png")
    results = sort_folder(demo_dir, Path("demo_sorted"))
    for color, count in sorted(results.items()):
        print(f"{color}: {count} photo(s)")
    print("Sorted into demo_sorted/")


def main():
    parser = argparse.ArgumentParser(description="Sort photos by dominant color.")
    parser.add_argument("folder", nargs="?", help="folder of photos to sort")
    parser.add_argument("--palette", metavar="IMAGE", help="print hex palette")
    parser.add_argument("--demo", action="store_true", help="run the demo")
    args = parser.parse_args()

    if args.demo:
        demo()
    elif args.palette:
        print(" ".join(palette(args.palette)))
    elif args.folder:
        results = sort_folder(args.folder, Path(args.folder).parent
                              / f"{Path(args.folder).name}_sorted")
        for color, count in sorted(results.items()):
            print(f"{color}: {count} photo(s)")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
