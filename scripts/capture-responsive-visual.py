#!/usr/bin/env python3
# ruff: noqa: E501
"""Capture deterministic Block 14 full-page Chromium visual evidence."""

from __future__ import annotations

import argparse
import base64
import importlib.util
import json
import platform
import subprocess
import tempfile
import time
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
FIT_HARNESS = REPO_ROOT / "scripts/measure-responsive-fit.py"
REFERENCE_WIDTHS = (360, 768, 1024, 1440)
INTERPOLATION_WIDTHS = (390, 480, 640, 820, 900, 1100, 1280)


def _fit_module() -> Any:
    spec = importlib.util.spec_from_file_location("responsive_fit_harness", FIT_HARNESS)
    if spec is None or spec.loader is None:
        raise RuntimeError("Unable to load responsive FIT harness")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def capture_locale(
    locale: str, url: str, output: Path, chromium: str, harness: Any
) -> dict[str, Any]:
    port = harness.available_port()
    with tempfile.TemporaryDirectory(prefix="responsive-visual-") as profile:
        process = subprocess.Popen(
            [
                chromium,
                "--headless",
                "--no-sandbox",
                "--disable-gpu",
                "--no-proxy-server",
                "--remote-allow-origins=*",
                f"--remote-debugging-port={port}",
                f"--user-data-dir={profile}",
                f"--accept-lang={locale}",
                url,
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        try:
            devtools = harness.DevTools(harness.page_websocket(port, url))
            devtools.call("Page.enable")
            devtools.call("Runtime.enable")
            devtools.call(
                "Network.setExtraHTTPHeaders",
                {"headers": {"Accept-Language": locale}},
            )
            deadline = time.monotonic() + 15
            while time.monotonic() < deadline:
                ready = devtools.call(
                    "Runtime.evaluate",
                    {
                        "expression": "document.readyState === 'complete'",
                        "returnByValue": True,
                    },
                )
                if ready["result"].get("value") is True:
                    break
                time.sleep(0.05)

            widths: dict[str, Any] = {}
            for width in (*REFERENCE_WIDTHS, *INTERPOLATION_WIDTHS):
                devtools.call(
                    "Emulation.setDeviceMetricsOverride",
                    {
                        "width": width,
                        "height": 900,
                        "deviceScaleFactor": 1,
                        "mobile": False,
                    },
                )
                measured = devtools.call(
                    "Runtime.evaluate",
                    {"expression": harness.MEASURE_JS, "returnByValue": True},
                )["result"]["value"]
                collision = devtools.call(
                    "Runtime.evaluate",
                    {
                        "expression": """
                        (() => {
                          const ai=document.querySelector('.home-ai-rag');
                          const hit=(selector) => {const node=document.querySelector(selector); if (!ai || !node) return false; const a=ai.getBoundingClientRect(),b=node.getBoundingClientRect(); return a.left<b.right&&a.right>b.left&&a.top<b.bottom&&a.bottom>b.top;};
                          scrollTo(0, document.documentElement.scrollHeight);
                          return {projects:hit('.homepage-footer__nav a[href="#projects"]'),contact:hit('.homepage-footer__nav a[href="#contact"]'),linkedin:hit('.homepage-footer__social a[href*="linkedin"]'),github:hit('.homepage-footer__social a[href*="github"]'),cta:hit('.home-contact__action')};
                        })()
                        """,
                        "returnByValue": True,
                    },
                )["result"]["value"]
                devtools.call(
                    "Runtime.evaluate",
                    {"expression": "scrollTo(0,0)", "returnByValue": True},
                )
                technology = devtools.call(
                    "Runtime.evaluate",
                    {
                        "expression": """
                        (() => {
                          const rect=(selector)=>{const n=document.querySelector(selector);if(!n)return null;const r=n.getBoundingClientRect();return {x:r.x,y:r.y,width:r.width,height:r.height,right:r.right,bottom:r.bottom}};
                          const style=(selector)=>{const n=document.querySelector(selector);if(!n)return null;const s=getComputedStyle(n);return {position:s.position,zIndex:s.zIndex,overflow:s.overflow,display:s.display,opacity:s.opacity,backgroundImage:s.backgroundImage,backgroundSize:s.backgroundSize,backgroundPosition:s.backgroundPosition,backgroundRepeat:s.backgroundRepeat,fontSize:s.fontSize,lineHeight:s.lineHeight}};
                          const visual=rect('.home-hero__visual'),ide=rect('.home-hero__ide'),gutter=rect('.home-hero__gutter'),explorer=rect('.home-hero__explorer'),portrait=rect('.home-hero__visual picture');
                          const overlap=(a,b)=>a&&b?Math.max(0,Math.min(a.right,b.right)-Math.max(a.x,b.x))*Math.max(0,Math.min(a.bottom,b.bottom)-Math.max(a.y,b.y)):null;
                          return {
                            rects:{visual,ide,gutter,explorer,portrait,background:rect('.homepage__technology-background')},
                            styles:{visual:style('.home-hero__visual'),ide:style('.home-hero__ide'),gutter:style('.home-hero__gutter'),explorer:style('.home-hero__explorer'),portrait:style('.home-hero__visual picture'),rim:style('.home-hero__portrait-rim'),background:style('.homepage__technology-background')},
                            relationships:{gutterIdeOverlap:overlap(gutter,ide),ideExplorerOverlap:overlap(ide,explorer),portraitIdeOverlap:overlap(portrait,ide),portraitExplorerOverlap:overlap(portrait,explorer)}
                          };
                        })()
                        """,
                        "returnByValue": True,
                    },
                )["result"]["value"]
                bg_rect = technology["rects"]["background"]
                scale = max(bg_rect["width"] / 933, bg_rect["height"] / 1686)
                technology["background_render"] = {
                    "source": {"width": 933, "height": 1686},
                    "scale": scale,
                    "rendered": {"width": 933 * scale, "height": 1686 * scale},
                    "center_crop": {
                        "x": max(0, (933 * scale - bg_rect["width"]) / 2),
                        "y": max(0, (1686 * scale - bg_rect["height"]) / 2),
                    },
                }
                widths[str(width)] = {
                    "reference": width in REFERENCE_WIDTHS,
                    "mode": measured["mode"],
                    "overflow": measured["overflow"],
                    "broken_words": measured["brokenWords"],
                    "component_collisions": measured["collisions"],
                    "trace_rects": measured["traceRects"],
                    "footer_target_collisions": collision,
                    "background": measured["background"],
                    "technology": technology,
                }
                if width in REFERENCE_WIDTHS:
                    devtools.call(
                        "Runtime.evaluate",
                        {"expression": "scrollTo(0,0);document.documentElement.style.scrollBehavior='auto'"},
                    )
                    metrics = devtools.call("Page.getLayoutMetrics")
                    size = metrics["cssContentSize"]
                    shot = devtools.call(
                        "Page.captureScreenshot",
                        {
                            "format": "png",
                            "optimizeForSpeed": True,
                            "captureBeyondViewport": True,
                            "clip": {
                                "x": 0,
                                "y": 0,
                                "width": width,
                                "height": size["height"],
                                "scale": 1,
                            },
                        },
                    )
                    screenshot = output / f"homepage-{locale.lower()}-{width}.png"
                    screenshot.write_bytes(base64.b64decode(shot["data"]))
                    widths[str(width)]["screenshot"] = str(
                        screenshot.relative_to(REPO_ROOT)
                    )
                    hero_rect = technology["rects"]["visual"]
                    hero_shot = devtools.call(
                        "Page.captureScreenshot",
                        {
                            "format": "png",
                            "optimizeForSpeed": True,
                            "captureBeyondViewport": True,
                            "clip": {
                                "x": 0,
                                "y": max(0, hero_rect["y"] - 24),
                                "width": width,
                                "height": max(hero_rect["height"], technology["rects"]["portrait"]["bottom"] - hero_rect["y"]) + 48,
                                "scale": 1,
                            },
                        },
                    )
                    hero_screenshot = output / f"hero-technology-{locale.lower()}-{width}.png"
                    hero_screenshot.write_bytes(base64.b64decode(hero_shot["data"]))
                    widths[str(width)]["hero_screenshot"] = str(hero_screenshot.relative_to(REPO_ROOT))
            return {"locale": locale, "widths": widths}
        finally:
            process.terminate()
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", default="http://127.0.0.1:8000/")
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("artifacts/responsive-visual/block14"),
    )
    parser.add_argument("--chromium", default="chromium")
    parser.add_argument("--evidence-name", default="block14-visual-validation.json")
    args = parser.parse_args()
    args.output = args.output.resolve()
    args.output.mkdir(parents=True, exist_ok=True)
    harness = _fit_module()
    locales = [
        capture_locale(locale, args.url, args.output, args.chromium, harness)
        for locale in ("en-US", "pt-BR")
    ]
    evidence = {
        "schema_version": 1,
        "environment": {
            "browser": subprocess.check_output(
                [args.chromium, "--version"], text=True
            ).strip(),
            "os": platform.platform(),
            "device_pixel_ratio": 1,
            "zoom": "100%",
            "viewport_height": 900,
        },
        "reference_widths": REFERENCE_WIDTHS,
        "interpolation_widths": INTERPOLATION_WIDTHS,
        "locales": locales,
    }
    destination = args.output / args.evidence_name
    destination.write_text(
        json.dumps(evidence, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(destination)


if __name__ == "__main__":
    main()
