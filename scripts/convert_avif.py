#!/usr/bin/env python3
"""Convert PNG assets to AVIF and wire them into HTML/CSS."""

from __future__ import annotations

import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
IMAGES = ROOT / "images"
QUALITY = 58
SPEED = 4

SKIP_AVIF: set[Path] = set()


def convert_png_to_avif(png: Path) -> Path:
    avif = png.with_suffix(".avif")
    if png in SKIP_AVIF:
        return avif
    subprocess.run(
        [
            "avifenc",
            "-q",
            str(QUALITY),
            "-s",
            str(SPEED),
            str(png),
            str(avif),
        ],
        check=True,
        capture_output=True,
    )
    return avif


def image_set(png_url: str) -> str:
    avif_url = png_url.replace(".png", ".avif")
    return (
        f"image-set(url('{avif_url}') type('image/avif'), "
        f"url('{png_url}') type('image/png'))"
    )


def update_css() -> None:
    css_path = ROOT / "css" / "styles.css"
    css = css_path.read_text()

    css = re.sub(
        r"url\('(\.\./images/[^']+\.png)'\)",
        lambda m: image_set(m.group(1)),
        css,
    )
    css_path.write_text(css)


def srcset_avif(srcset: str) -> str:
    return re.sub(r"\.png", ".avif", srcset)


def wrap_img_tags(html: str) -> str:
    pattern = re.compile(
        r'<img\b([^>]*?)\bsrc="([^"]+\.png)"([^>]*?)>',
        re.IGNORECASE,
    )

    def repl(match: re.Match[str]) -> str:
        before, src, after = match.group(1), match.group(2), match.group(3)
        attrs = f"{before}src=\"{src}\"{after}"
        srcset_match = re.search(r'\bsrcset="([^"]+)"', attrs)
        sizes_match = re.search(r'\bsizes="([^"]+)"', attrs)

        source_attrs = ['type="image/avif"']
        if srcset_match:
            source_attrs.append(f'srcset="{srcset_avif(srcset_match.group(1))}"')
        else:
            source_attrs.append(f'srcset="{src.replace(".png", ".avif")}"')
        if sizes_match:
            source_attrs.append(f'sizes="{sizes_match.group(1)}"')

        img_tag = f"<img{before}src=\"{src}\"{after}>"
        return (
            "<picture>"
            f"<source {' '.join(source_attrs)}>"
            f"{img_tag}"
            "</picture>"
        )

    return pattern.sub(repl, html)


def update_html() -> None:
    html_path = ROOT / "index.html"
    html = html_path.read_text()
    html_path.write_text(wrap_img_tags(html))


def main() -> None:
    pngs = sorted(IMAGES.rglob("*.png"))
    before = sum(p.stat().st_size for p in pngs)
    avif_total = 0

    for png in pngs:
        avif = convert_png_to_avif(png)
        if avif.exists():
            avif_total += avif.stat().st_size

    update_css()
    update_html()

    print(f"Converted {len(pngs)} PNG files")
    print(f"PNG total: {before / 1024 / 1024:.2f} MB")
    print(f"AVIF total: {avif_total / 1024 / 1024:.2f} MB")


if __name__ == "__main__":
    main()
