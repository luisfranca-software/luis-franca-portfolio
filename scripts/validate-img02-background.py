#!/usr/bin/env python3
"""Capture deterministic IMG-02 geometry and >1440 browser evidence."""

from __future__ import annotations

import argparse
import base64
import importlib.util
import json
import subprocess
import tempfile
import time
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
HARNESS_PATH = REPO_ROOT / "scripts/measure-responsive-fit.py"
WIDTHS = (360, 390, 480, 600, 767, 768, 900, 1023, 1024, 1280, 1439, 1440, 1600, 1920)
SECTIONS = {
    "header": ".site-header",
    "hero": ".home-hero",
    "engineering": ".home-engineering",
    "projects": ".home-projects",
    "process": ".home-process",
    "evidence_contact": ".home-evidence",
    "footer": ".homepage-footer",
    "juju_ai": ".home-ai-rag",
}


def harness() -> Any:
    spec = importlib.util.spec_from_file_location("responsive_fit_harness", HARNESS_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("Unable to load responsive FIT harness")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def capture(locale: str, url: str, output: Path, chromium: str, fit: Any) -> dict[str, Any]:
    port = fit.available_port()
    with tempfile.TemporaryDirectory(prefix="img02-validation-") as profile:
        process = subprocess.Popen(
            [
                chromium, "--headless", "--no-sandbox", "--disable-gpu",
                "--no-proxy-server", "--remote-allow-origins=*",
                f"--remote-debugging-port={port}", f"--user-data-dir={profile}",
                f"--accept-lang={locale}", url,
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        try:
            devtools = fit.DevTools(fit.page_websocket(port, url))
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
                    {"expression": "document.readyState === 'complete'", "returnByValue": True},
                )
                if ready["result"].get("value") is True:
                    break
                time.sleep(0.05)

            results: dict[str, Any] = {}
            for width in WIDTHS:
                devtools.call(
                    "Emulation.setDeviceMetricsOverride",
                    {"width": width, "height": 900, "deviceScaleFactor": 1, "mobile": False},
                )
                expression = f"""
                (() => {{
                  const rect = selector => {{
                    const node = document.querySelector(selector);
                    if (!node) return null;
                    const r = node.getBoundingClientRect();
                    return {{
                      x:r.x,y:r.y,width:r.width,height:r.height,
                      right:r.right,bottom:r.bottom
                    }};
                  }};
                  const bg = document.querySelector('.homepage__technology-background');
                  const style = getComputedStyle(bg);
                  const sections = Object.fromEntries(
                    Object.entries({json.dumps(SECTIONS)}).map(
                      ([key, selector]) => [key, rect(selector)]
                    )
                  );
                  return {{
                    innerWidth,
                    documentWidth: document.documentElement.scrollWidth,
                    clientWidth: document.documentElement.clientWidth,
                    documentHeight: document.documentElement.scrollHeight,
                    backgroundOwner: rect('.homepage__technology-background'),
                    computed: {{
                      image: style.backgroundImage,
                      size: style.backgroundSize,
                      position: style.backgroundPosition,
                      repeat: style.backgroundRepeat,
                      pointerEvents: style.pointerEvents,
                      positionType: style.position,
                    }},
                    horizontalOverflow: document.documentElement.scrollWidth > innerWidth,
                    sections,
                  }};
                }})()
                """
                value = devtools.call(
                    "Runtime.evaluate", {"expression": expression, "returnByValue": True}
                )["result"]["value"]
                scale = width / 1440
                value["scale"] = scale
                value["expectedModule"] = {"width": width, "height": 2604 * scale}
                value["actualCanonicalModule"] = {
                    "width": width,
                    "height": 2604 * scale,
                    "basis": "computed 100vw auto against Figma canonical 1440x2604 geometry",
                }
                results[str(width)] = value

                if locale == "en-US" and width in (1600, 1920):
                    metrics = devtools.call("Page.getLayoutMetrics")["cssContentSize"]
                    shot = devtools.call(
                        "Page.captureScreenshot",
                        {
                            "format": "png", "optimizeForSpeed": True,
                            "captureBeyondViewport": True,
                            "clip": {
                                "x": 0, "y": 0, "width": width,
                                "height": metrics["height"], "scale": 1,
                            },
                        },
                    )
                    screenshot = output / f"homepage-en-us-{width}.png"
                    screenshot.write_bytes(base64.b64decode(shot["data"]))
                    value["screenshot"] = str(screenshot.relative_to(REPO_ROOT))
            return {"locale": locale, "widths": results}
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
        default=Path("artifacts/responsive-visual/img02-continuous"),
    )
    parser.add_argument("--chromium", default="chromium")
    args = parser.parse_args()
    args.output = args.output.resolve()
    args.output.mkdir(parents=True, exist_ok=True)
    fit = harness()
    evidence = {
        "schemaVersion": 1,
        "canonical": {
            "figmaFile": "7XIYTbKZrLk77biI0UhRIb",
            "node": "199:1358",
            "geometry": {"width": 1440, "height": 2604},
            "assetSha1": "b06fb16c56279829bc6adb74058b8d60081e5854",
        },
        "formula": "module_width = viewport_width; module_height = 2604 * viewport_width / 1440",
        "locales": [
            capture(locale, args.url, args.output, args.chromium, fit)
            for locale in ("en-US", "pt-BR")
        ],
    }
    destination = args.output / "img02-geometry.json"
    destination.write_text(json.dumps(evidence, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(destination)


if __name__ == "__main__":
    main()
