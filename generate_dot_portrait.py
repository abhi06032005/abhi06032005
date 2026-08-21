import argparse
import sys
from pathlib import Path

from PIL import Image, ImageOps


def build_svg(img: Image.Image, cols: int, invert: bool, dark_bg: bool,
              max_radius: float, cell: int, stagger: float, duration: float) -> str:
    w, h = img.size
    rows = round(cols * h / w)
    small = img.resize((cols, rows), Image.LANCZOS)
    gray = ImageOps.grayscale(small)
    gray = ImageOps.autocontrast(gray, cutoff=1)
    if invert:
        gray = ImageOps.invert(gray)

    px = gray.load()

    svg_w = cols * cell
    svg_h = rows * cell

    bg = "#000000" if dark_bg else "#ffffff"
    dot = "#ffffff" if dark_bg else "#000000"

    circles = []
    delay_index = 0
    for y in range(rows):
        for x in range(cols):
            brightness = px[x, y] / 255.0
            level = 1.0 - brightness
            if level < 0.04:
                continue
            r = round(max_radius * level, 2)
            cx = x * cell + cell / 2
            cy = y * cell + cell / 2
            delay = round((delay_index * stagger) % duration, 3)
            delay_index += 1
            circles.append(
                f'<circle cx="{cx}" cy="{cy}" r="0" fill="{dot}">'
                f'<animate attributeName="r" values="0;{r};{r}" '
                f'keyTimes="0;0.15;1" dur="{duration}s" begin="{delay}s" '
                f'repeatCount="indefinite" calcMode="spline" '
                f'keySplines="0.2 0.8 0.2 1;0 0 1 1"/></circle>'
            )

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {svg_w} {svg_h}" width="{svg_w}" height="{svg_h}">
  <rect x="0" y="0" width="{svg_w}" height="{svg_h}" fill="{bg}"/>
  {''.join(circles)}
</svg>'''
    return svg


def main():
    ap = argparse.ArgumentParser(description="Photo -> animated B&W dot-matrix SVG")
    ap.add_argument("photo", help="Path to your photo (jpg/png)")
    ap.add_argument("--out", default="assets/dot-portrait.svg", help="Output SVG path")
    ap.add_argument("--cols", type=int, default=64, help="Dot grid columns (higher = more detail, bigger file)")
    ap.add_argument("--cell", type=int, default=10, help="Pixel size per grid cell")
    ap.add_argument("--max-radius", type=float, default=4.6, help="Max dot radius")
    ap.add_argument("--stagger", type=float, default=0.012, help="Seconds between each dot's animation start")
    ap.add_argument("--duration", type=float, default=6.0, help="Loop duration in seconds")
    ap.add_argument("--invert", action="store_true", help="Invert brightness mapping")
    ap.add_argument("--dark-bg", action="store_true", default=True, help="Black background, white dots (default)")
    ap.add_argument("--light-bg", dest="dark_bg", action="store_false", help="White background, black dots")
    args = ap.parse_args()

    photo_path = Path(args.photo)
    if not photo_path.exists():
        sys.exit(f"Photo not found: {photo_path}")

    img = Image.open(photo_path).convert("RGB")
    w, h = img.size
    side = min(w, h)
    left = (w - side) // 2
    top = (h - side) // 2
    img = img.crop((left, top, left + side, top + side))

    svg = build_svg(
        img,
        cols=args.cols,
        invert=args.invert,
        dark_bg=args.dark_bg,
        max_radius=args.max_radius,
        cell=args.cell,
        stagger=args.stagger,
        duration=args.duration,
    )

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(svg, encoding="utf-8")
    print(f"Wrote {out_path}  ({args.cols}x{round(args.cols*img.size[1]/img.size[0])} dots)")


if __name__ == "__main__":
    main()