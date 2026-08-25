#!/usr/bin/env bash
# Generate responsive delivery derivatives and favicon candidates from the
# approved repository masters for the Site Portfolio visual assets.
#
# Provenance and governance:
#   - The approved visual masters are the authoritative raster sources and are
#     NEVER regenerated or modified by this script.
#   - The LF brand mark is NOT redrawn, recolored, vectorized or otherwise
#     recreated: the favicon source is a deterministic pixel crop of the
#     approved logo master.
#   - Derived files have deterministic names and deterministic content for a
#     fixed ImageMagick version and parameters.
#
# Regeneration command (from the repository root):
#   bash scripts/generate-assets.sh
# or:
#   make generate-assets
#
# Requirements:
#   - ImageMagick 7 (`magick`) or 6 (`convert`) with PNG and WebP delegates.
#
# No project dependency is required: asset generation is a build-time,
# host-level step that leaves the uv-managed dependency set unchanged.

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BRAND_DIR="${REPO_ROOT}/frontend/static/images/brand"
PROFILE_DIR="${REPO_ROOT}/frontend/static/images/profile"
BACKGROUND_DIR="${REPO_ROOT}/frontend/static/images/background"
PROJECTS_DIR="${REPO_ROOT}/frontend/static/images/projects"
FAVICON_DIR="${REPO_ROOT}/frontend/static/images/favicon"

BRAND_MASTER="lf-information-system.png"
PROFILE_MASTER="luis-franca.png"
HOMEPAGE_PORTRAIT_MASTER="luis-franca-transparent-02.png"
HOMEPAGE_BACKGROUND_MASTER="homepage-background-desktop-02.png"

# Approved Release 1 featured project screenshots (SPEC-003-REQ-002).
PROJECT_MASTERS=(
    "enterprise-platform.png:1480x16384"
    "intelligent-currency-platform.png:1480x16384"
    "sistema_cotacao_moedas.png:1480x7636"
)

# --- Locate ImageMagick -----------------------------------------------------

IM=""
if command -v magick >/dev/null 2>&1; then
    IM="magick"
elif command -v convert >/dev/null 2>&1; then
    IM="convert"
else
    echo "ERROR: ImageMagick (magick/convert) is required to generate assets." >&2
    exit 1
fi

# --- Guard: masters must exist with the expected dimensions -----------------

"${IM}" identify -format "%wx%h" "${BRAND_DIR}/${BRAND_MASTER}" 2>/dev/null \
    | grep -q "^1254x1254$" || {
        echo "ERROR: ${BRAND_MASTER} missing or not 1254x1254." >&2
        exit 1
    }
"${IM}" identify -format "%wx%h" "${PROFILE_DIR}/${PROFILE_MASTER}" 2>/dev/null \
    | grep -q "^896x1195$" || {
        echo "ERROR: ${PROFILE_MASTER} missing or not 896x1195." >&2
        exit 1
    }
"${IM}" identify -format "%wx%h" "${PROFILE_DIR}/${HOMEPAGE_PORTRAIT_MASTER}" 2>/dev/null \
    | grep -q "^1385x1136$" || {
        echo "ERROR: ${HOMEPAGE_PORTRAIT_MASTER} missing or not 1385x1136." >&2
        exit 1
    }
"${IM}" identify -format "%wx%h" "${BACKGROUND_DIR}/${HOMEPAGE_BACKGROUND_MASTER}" 2>/dev/null \
    | grep -q "^933x1686$" || {
        echo "ERROR: ${HOMEPAGE_BACKGROUND_MASTER} missing or not 933x1686." >&2
        exit 1
    }

# --- Project screenshot WebP delivery derivatives ----------------------------
# Screenshots are full-page captures taller than their display container
# (SPEC-003-REQ-006); width-only resize preserves the full-page composition.

for entry in "${PROJECT_MASTERS[@]}"; do
    master="${entry%%:*}"
    expected="${entry##*:}"
    if ! "${IM}" identify -format "%wx%h" "${PROJECTS_DIR}/${master}" 2>/dev/null \
        | grep -q "^${expected}$"; then
        echo "ERROR: ${master} missing or not ${expected}." >&2
        exit 1
    fi
    for size in 900 450; do
        "${IM}" "${PROJECTS_DIR}/${master}" \
            -filter Lanczos -resize "${size}x" \
            -quality 82 "${PROJECTS_DIR}/${master%.png}-${size}.webp"
    done
done

# --- Logo WebP delivery derivatives -----------------------------------------
# Derived from the 1254x1254 master; never upscaled beyond master resolution.

for size in 1254 600 300; do
    "${IM}" "${BRAND_DIR}/${BRAND_MASTER}" \
        -filter Lanczos -resize "${size}x${size}" \
        -quality 90 "${BRAND_DIR}/${BRAND_MASTER%.png}-${size}.webp"
done

# --- Profile photograph WebP delivery derivatives ---------------------------
# Width-only resize preserves the native aspect ratio at every size.

for size in 896 640 400; do
    "${IM}" "${PROFILE_DIR}/${PROFILE_MASTER}" \
        -filter Lanczos -resize "${size}x" \
        -quality 82 "${PROFILE_DIR}/${PROFILE_MASTER%.png}-${size}.webp"
done

# --- Homepage portrait WebP delivery derivatives ----------------------------
# The approved -02 RGBA master remains the PNG fallback. Width-only WebP
# derivatives retain transparency and cover measured reference-state demand.

for size in 1024 768 480; do
    "${IM}" "${PROFILE_DIR}/${HOMEPAGE_PORTRAIT_MASTER}" \
        -filter Lanczos -resize "${size}x" \
        -quality 88 "${PROFILE_DIR}/${HOMEPAGE_PORTRAIT_MASTER%.png}-${size}.webp"
done

# --- Favicon candidates (deterministic crop of the approved logo master) ----
#
# The LF brand mark occupies x=217..1115, y=286..802 within the 1254x1254
# master. The mark is first cropped to its exact bounds (original pixels
# preserved; no redraw, no distortion) and then padded with the logo's black
# background on a centered 1019x1019 square canvas. The padding is added
# outside the crop so that the "INFORMATION SYSTEM" and tagline text bands
# (y>=829) can never enter the favicon.
#
# STATUS: candidates require manual visual validation before adoption
# (see frontend/static/images/README.md).

FAVICON_CROP="899x517+217+286"

# png:exclude-chunks keeps PNG output byte-deterministic by omitting the
# timestamp chunks (tIME/tEXt/zTXt/iTXt) that ImageMagick would otherwise embed.

"${IM}" "${BRAND_DIR}/${BRAND_MASTER}" -crop "${FAVICON_CROP}" +repage \
    -background black -gravity center -extent 1019x1019 \
    -define png:exclude-chunks=tIME,tEXt,zTXt,iTXt "${FAVICON_DIR}/lf-mark-master.png"

"${IM}" "${FAVICON_DIR}/lf-mark-master.png" -filter Lanczos -resize 16x16 \
    -define png:exclude-chunks=tIME,tEXt,zTXt,iTXt "${FAVICON_DIR}/favicon-16x16.png"
"${IM}" "${FAVICON_DIR}/lf-mark-master.png" -filter Lanczos -resize 32x32 \
    -define png:exclude-chunks=tIME,tEXt,zTXt,iTXt "${FAVICON_DIR}/favicon-32x32.png"
"${IM}" "${FAVICON_DIR}/lf-mark-master.png" -filter Lanczos -resize 180x180 \
    -define png:exclude-chunks=tIME,tEXt,zTXt,iTXt "${FAVICON_DIR}/apple-touch-icon.png"
"${IM}" "${FAVICON_DIR}/lf-mark-master.png" \
    -define icon:auto-resize=16,32,48 "${FAVICON_DIR}/favicon.ico"

echo "Asset generation complete:"
find "${BRAND_DIR}" "${PROFILE_DIR}" "${PROJECTS_DIR}" "${FAVICON_DIR}" -type f \( -name '*.webp' -o -name '*.png' -o -name '*.ico' \) | sort
