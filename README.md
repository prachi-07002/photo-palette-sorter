# Photo Palette Sorter

Sort a folder of photos by dominant color, or pull a hex palette out of
a single image. Built with Python + Pillow.

## Setup

```bash
pip install Pillow
```

## Usage

```bash
python palette_sorter.py photos/            # sorts into photos_sorted/
python palette_sorter.py --palette img.jpg  # prints a hex palette
python palette_sorter.py --demo             # tries it on generated images
```

## How it works

Each image is shrunk to 100x100, the most frequent pixel color wins, and
that color is matched to the nearest basic color name (pink, blue, gold,
etc.) by RGB distance. The palette mode picks up to 5 colors that are
visually distinct from each other.

## Ideas to extend

- Cluster colors with k-means instead of raw frequency
- Build a collage per color folder
- Export palettes as CSS variables or an ASE file
