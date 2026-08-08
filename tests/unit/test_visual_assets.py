"""Integrity checks for the approved Release 1 visual assets.

Verifies that the repository masters are pixel-exact copies of the approved
sources and that the generated delivery derivatives exist with the expected
formats and dimensions. See frontend/static/images/README.md for provenance
and the generation procedure.
"""

import hashlib
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
IMAGES_DIR = REPO_ROOT / "frontend" / "static" / "images"

BRAND_MASTER = IMAGES_DIR / "brand" / "lf-information-system.png"
PROFILE_MASTER = IMAGES_DIR / "profile" / "luis-franca.png"

BRAND_MASTER_HASH = (
    "65610007eafd5d27d53b81819a31a44ea2a07322260dd4a64dfe589a161181fc"
)
PROFILE_MASTER_HASH = (
    "b80db13f3044c862321e4b081e67a20ca7b8af3f65f70b5470cfd9eacd25bacb"
)

PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
WEBP_SIGNATURE = b"RIFF"
WEBP_MAGIC = b"WEBP"
ICO_SIGNATURE = b"\x00\x00\x01\x00"

EXPECTED_BRAND_WEBP = {1254: (1254, 1254), 600: (600, 600), 300: (300, 300)}
EXPECTED_PROFILE_WEBP = {896: (896, 1195), 640: (640, 854), 400: (400, 533)}


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _png_dimensions(path: Path) -> tuple[int, int]:
    data = path.read_bytes()
    if data[:8] != PNG_SIGNATURE:
        raise AssertionError(f"{path} is not a PNG file")
    width = int.from_bytes(data[16:20], "big")
    height = int.from_bytes(data[20:24], "big")
    return width, height


def _webp_dimensions(path: Path) -> tuple[int, int]:
    data = path.read_bytes()
    if data[:4] != WEBP_SIGNATURE or data[8:12] != WEBP_MAGIC:
        raise AssertionError(f"{path} is not a WebP file")
    pos = 12
    while pos + 8 <= len(data):
        tag = data[pos : pos + 4]
        size = int.from_bytes(data[pos + 4 : pos + 8], "little")
        if tag == b"VP8 ":
            width = int.from_bytes(data[pos + 14 : pos + 16], "little") & 0x3FFF
            height = int.from_bytes(data[pos + 16 : pos + 18], "little") & 0x3FFF
            return width, height
        pos += 8 + size + (size & 1)
    raise AssertionError(f"{path} contains no VP8 image data")


def test_brand_master_matches_approved_source() -> None:
    assert BRAND_MASTER.is_file()
    assert _png_dimensions(BRAND_MASTER) == (1254, 1254)
    assert _sha256(BRAND_MASTER) == BRAND_MASTER_HASH


def test_profile_master_matches_approved_source() -> None:
    assert PROFILE_MASTER.is_file()
    assert _png_dimensions(PROFILE_MASTER) == (896, 1195)
    assert _sha256(PROFILE_MASTER) == PROFILE_MASTER_HASH


def test_brand_webp_derivatives() -> None:
    for width, expected in EXPECTED_BRAND_WEBP.items():
        path = IMAGES_DIR / "brand" / f"lf-information-system-{width}.webp"
        assert path.is_file(), f"missing {path.name}"
        assert _webp_dimensions(path) == expected


def test_profile_webp_derivatives() -> None:
    for width, expected in EXPECTED_PROFILE_WEBP.items():
        path = IMAGES_DIR / "profile" / f"luis-franca-{width}.webp"
        assert path.is_file(), f"missing {path.name}"
        assert _webp_dimensions(path) == expected


def test_favicon_candidates() -> None:
    favicon_dir = IMAGES_DIR / "favicon"
    assert favicon_dir.is_dir()
    assert _png_dimensions(favicon_dir / "lf-mark-master.png") == (1019, 1019)
    assert _png_dimensions(favicon_dir / "favicon-16x16.png") == (16, 16)
    assert _png_dimensions(favicon_dir / "favicon-32x32.png") == (32, 32)
    assert _png_dimensions(favicon_dir / "apple-touch-icon.png") == (180, 180)
    ico = (favicon_dir / "favicon.ico").read_bytes()
    assert ico[:4] == ICO_SIGNATURE
    assert ico[4] == 3
