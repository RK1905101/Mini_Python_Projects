"""Palette extraction utilities.

Try to use colorgram to extract colors; if unavailable or failing, fall back to Pillow-based extraction
using Image.quantize/adaptive palette. If neither is available, return a built-in fallback palette.
"""
from typing import List, Tuple

try:
    import colorgram  # type: ignore
except Exception:
    colorgram = None

try:
    from PIL import Image
except Exception:
    Image = None  # type: ignore


FALLBACK_PALETTE: List[Tuple[int, int, int]] = [
    (253, 251, 247), (253, 248, 252), (235, 252, 243), (198, 13, 32),
    (248, 236, 25), (40, 76, 188), (244, 247, 253), (39, 216, 69),
    (238, 227, 5), (227, 159, 49)
]


def extract_with_colorgram(image_path: str, count: int = 10) -> List[Tuple[int, int, int]]:
    palette = []
    if colorgram is None:
        return palette
    try:
        colors = colorgram.extract(image_path, count)
        for c in colors:
            r = c.rgb.r
            g = c.rgb.g
            b = c.rgb.b
            palette.append((r, g, b))
    except Exception:
        return []
    return palette


def extract_with_pillow(image_path: str, count: int = 10) -> List[Tuple[int, int, int]]:
    if Image is None:
        return []
    try:
        img = Image.open(image_path).convert('RGBA')
        # Resize to speed up palette extraction
        img_thumb = img.copy()
        img_thumb.thumbnail((200, 200))
        # Convert to palette using adaptive quantization
        paletted = img_thumb.convert('P', palette=Image.ADAPTIVE, colors=count)
        palette = paletted.getpalette() or []
        result = []
        for i in range(0, min(len(palette), count * 3), 3):
            r = palette[i]
            g = palette[i + 1]
            b = palette[i + 2]
            result.append((r, g, b))
        return result
    except Exception:
        return []


def extract_palette(image_path: str = 'hirst-painting.jpg', count: int = 10) -> List[Tuple[int, int, int]]:
    """Try multiple strategies and return a palette list of (r,g,b) tuples.

    Order: colorgram -> Pillow -> fallback built-in palette.
    """
    # 1) try colorgram
    pal = extract_with_colorgram(image_path, count)
    if pal:
        return pal[:count]

    # 2) try Pillow
    pal = extract_with_pillow(image_path, count)
    if pal:
        return pal[:count]

    # 3) fallback
    return FALLBACK_PALETTE[:count]
