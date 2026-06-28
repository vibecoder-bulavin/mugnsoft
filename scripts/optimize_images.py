#!/usr/bin/env python3
"""Compress images and organize into proper folders."""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "images"
OUT = ROOT / "images_optimized"

BG_WIDTHS = [500, 800, 1080, 1600, 2000, 2600]
BG_FILES = {
    "hero-bg": [500, 800, 1080, 1600, 2000, 2600],
    "tabs-bg": [500, 800, 1080, 1600, 2000, 2600],
    "plan-dp-bg": [500, 800, 1080, 1600, 2000, 2600],
    "cta-bg": [500, 800, 1080, 1600, 2000],
    "footer-bg": [500, 800, 1080, 1600, 2000],
}

CONTENT_SRCSETS = {
    "video-thumb": [500, 800, 1080, 1600, 2000],
    "timing": [500, 800],
    "bugs-2": [500, 800],
    "tab_1": [500, 800, 1080],
    "tab-2": [500, 800, 1080],
    "tab-3": [500, 800, 1080],
    "tab-4": [500, 800, 1080],
    "detectez-1": [500],
    "detectez-2": [500],
    "detectez-3": [500],
    "demarez-1": [500],
    "demarez-2": [500],
    "demarez-3": [500],
}

ICONS = [
    "Shine.svg",
    "arrow.svg",
    "bug.svg",
    "button-hradient-border.svg",
    "iconamoon_menu-burger-horizontal.svg",
    "icons.svg",
    "logo-cta.svg",
    "majesticons_close-line.svg",
    "mobile-bg-footer.svg",
    "poplar.svg",
    "tab-icon.svg",
    "favicon.ico",
    "webclip.png",
]

LOGOS = [f"slide_{i}.png" for i in range(1, 7)]
AVATARS = ["face-1.png", "face-2.png", "theresa.png"]


def pngquant(path: Path) -> None:
    tmp = path.with_suffix(".tmp.png")
    result = subprocess.run(
        [
            "pngquant",
            "--quality=65-85",
            "--speed=1",
            "--strip",
            "--force",
            "--output",
            str(tmp),
            str(path),
        ],
        capture_output=True,
    )
    if result.returncode == 0 and tmp.exists():
        tmp.replace(path)
    elif tmp.exists():
        tmp.unlink()


def save_png(src: Path, dst: Path, width: int | None = None) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    im = Image.open(src)
    if im.mode not in ("RGB", "RGBA"):
        im = im.convert("RGBA" if "A" in im.getbands() else "RGB")
    if width and im.width > width:
        height = round(im.height * width / im.width)
        im = im.resize((width, height), Image.Resampling.LANCZOS)
    im.save(dst, "PNG", optimize=True)
    pngquant(dst)


def copy_file(src: Path, dst: Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)
    if dst.suffix.lower() == ".png":
        pngquant(dst)


def main() -> None:
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir()

    bg_dir = OUT / "backgrounds"
    content_dir = OUT / "content"
    icons_dir = OUT / "icons"
    logos_dir = OUT / "logos"
    avatars_dir = OUT / "avatars"

    for name, widths in BG_FILES.items():
        src = SRC / f"{name}.png"
        if not src.exists():
            continue
        full_dst = bg_dir / f"{name}.png"
        save_png(src, full_dst)
        for w in widths:
            save_png(src, bg_dir / f"{name}-{w}.png", width=w)

    for base, widths in CONTENT_SRCSETS.items():
        src = SRC / f"{base}.png"
        if not src.exists():
            continue
        save_png(src, content_dir / f"{base}.png")
        for w in widths:
            existing = SRC / f"{base}-p-{w}.png"
            source = existing if existing.exists() else src
            save_png(source, content_dir / f"{base}-{w}.png", width=w)

    for icon in ICONS:
        src = SRC / icon
        if src.exists():
            copy_file(src, icons_dir / icon)

    for logo in LOGOS:
        src = SRC / logo
        if src.exists():
            save_png(src, logos_dir / logo, width=200)

    for avatar in AVATARS:
        src = SRC / avatar
        if src.exists():
            save_png(src, avatars_dir / avatar, width=120)

    total = sum(f.stat().st_size for f in OUT.rglob("*") if f.is_file())
    print(f"Optimized total: {total / 1024 / 1024:.2f} MB")


if __name__ == "__main__":
    main()
