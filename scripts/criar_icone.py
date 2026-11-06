"""Gera assets/icon.ico (navy + ouro, estilo TRT)."""
from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "icon.ico"
OUT.parent.mkdir(parents=True, exist_ok=True)


def draw(size: int) -> Image.Image:
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    pad = max(1, size // 16)
    d.rounded_rectangle(
        (pad, pad, size - pad - 1, size - pad - 1),
        radius=size // 5,
        fill=(15, 39, 64, 255),
    )
    cx, cy = size // 2, size // 2
    gold = (196, 149, 74, 255)
    cream = (247, 241, 232, 255)
    # balança
    arm_y = cy - size // 10
    d.line((size // 4, arm_y, 3 * size // 4, arm_y), fill=gold, width=max(2, size // 28))
    d.line((cx, arm_y - size // 10, cx, cy + size // 5), fill=gold, width=max(2, size // 28))
    r = size // 9
    for x in (size // 4, 3 * size // 4):
        d.ellipse((x - r, arm_y, x + r, arm_y + 2 * r), outline=gold, width=max(2, size // 32))
        d.ellipse((x - r // 2, arm_y + r // 2, x + r // 2, arm_y + 3 * r // 2), fill=cream)
    d.polygon(
        [(cx, arm_y - size // 8), (cx - size // 18, arm_y - size // 28), (cx + size // 18, arm_y - size // 28)],
        fill=gold,
    )
    return img


def main() -> None:
    sizes = [16, 32, 48, 64, 128, 256]
    images = [draw(s) for s in sizes]
    images[-1].save(OUT, format="ICO", sizes=[(s, s) for s in sizes])
    png = ROOT / "assets" / "icon.png"
    images[-1].save(png)
    print(f"Ícone: {OUT}")


if __name__ == "__main__":
    main()
