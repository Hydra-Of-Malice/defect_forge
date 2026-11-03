"""Find the part (SAM 3.1 point prompt seeded by an Otsu centroid) and sample defect locations on it."""
from __future__ import annotations

import cv2
import numpy as np
from PIL import Image, ImageOps

from ..config import CROP, MAX_SIDE
from ..meta.client import sam_segment


def load_image(path) -> Image.Image:
    img = ImageOps.exif_transpose(Image.open(path)).convert("RGB")
    if max(img.size) > MAX_SIDE:
        img.thumbnail((MAX_SIDE, MAX_SIDE), Image.LANCZOS)
    return img


def otsu_mask(img: Image.Image) -> np.ndarray:
    g = cv2.GaussianBlur(cv2.cvtColor(np.array(img), cv2.COLOR_RGB2GRAY), (5, 5), 0)
    _, o = cv2.threshold(g, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    # keep the largest component: the part on a darker background
    n, lab, stats, _ = cv2.connectedComponentsWithStats(o)
    if n <= 1:
        return np.ones(o.shape, bool)
    i = 1 + int(np.argmax(stats[1:, cv2.CC_STAT_AREA]))
    return lab == i


def part_mask(img: Image.Image, run_id: str | None = None) -> tuple[np.ndarray, str]:
    """SAM 3.1 point prompt at the Otsu centroid. Concept prompts return empty on studio scans (gate T3)."""
    o = otsu_mask(img)
    ys, xs = np.nonzero(o)
    cx, cy = (int(xs.mean()), int(ys.mean())) if len(xs) else (img.size[0] // 2, img.size[1] // 2)
    try:
        r = sam_segment(img, points=[[(cx, cy)]], run_id=run_id, op="part_mask")
        masks = [ob["mask"] for ob in r["objects"] if ob["mask"] is not None]
        if masks and masks[0].mean() > 0.02:
            return masks[0], "sam-3.1 point prompt"
    except Exception:
        pass
    return o, "otsu fallback"


def crop_size(img: Image.Image) -> int:
    return int(min(CROP, min(img.size)))


def sample_centres(mask: np.ndarray, n: int, crop: int, rng: np.random.Generator) -> list[tuple[int, int]]:
    """Defect centres well inside the part, spread out, and far enough from the border for a full crop."""
    H, W = mask.shape
    # keep centres in the inner part of the object, away from tips and edges where edits turn into slices
    dist = cv2.distanceTransform(mask.astype(np.uint8), cv2.DIST_L2, 5)
    er = dist >= 0.45 * dist.max()
    ys, xs = np.nonzero(er)
    if len(xs) == 0:
        ys, xs = np.nonzero(mask)
    pts: list[tuple[int, int]] = []
    for _ in range(n * 40):
        if len(pts) >= n:
            break
        i = rng.integers(len(xs))
        p = (int(xs[i]), int(ys[i]))
        if all((p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2 > (0.12 * W) ** 2 for q in pts):
            pts.append(p)
    while len(pts) < n:
        i = rng.integers(len(xs))
        pts.append((int(xs[i]), int(ys[i])))
    return pts


def crop_box(img_size: tuple[int, int], cx: int, cy: int, crop: int) -> tuple[int, int, int, int]:
    W, H = img_size
    x0 = int(np.clip(cx - crop // 2, 0, W - crop))
    y0 = int(np.clip(cy - crop // 2, 0, H - crop))
    return x0, y0, x0 + crop, y0 + crop
