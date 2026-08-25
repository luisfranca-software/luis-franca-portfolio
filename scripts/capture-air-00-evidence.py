#!/usr/bin/env python3
# ruff: noqa: E501
"""Capture deterministic AIR-00 position, content, and collision evidence."""

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
HARNESS_PATH = REPO_ROOT / "scripts/measure-responsive-fit.py"
REFERENCE_WIDTHS = (360, 768, 1024, 1440)
INTERPOLATION_WIDTHS = (390, 480, 640, 820, 900, 1100, 1280)


def _harness() -> Any:
    spec = importlib.util.spec_from_file_location("responsive_fit_harness", HARNESS_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("Unable to load responsive FIT harness")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


AIR_MEASURE_JS = r"""
(() => {
  const air=document.querySelector('[data-trace-id="AIR-00"]');
  if(!air) return {missing:true};
  const r=air.getBoundingClientRect(),s=getComputedStyle(air);
  const rect=n=>{if(!n)return null;const x=n.getBoundingClientRect();return {x:x.x,y:x.y,width:x.width,height:x.height,right:x.right,bottom:x.bottom}};
  const hit=n=>{if(!n)return false;const b=n.getBoundingClientRect();return r.left<b.right&&r.right>b.left&&r.top<b.bottom&&r.bottom>b.top};
  const footerNavLinks=[...document.querySelectorAll('.homepage-footer__nav a')];
  const footerSocialLinks=[...document.querySelectorAll('.homepage-footer__social a')];
  return {
    missing:false,text:air.innerText.trim(),rect:rect(air),scrollY,
    viewport:{width:innerWidth,height:innerHeight},
    edge:{right:innerWidth-r.right,bottom:innerHeight-r.bottom},
    style:{position:s.position,right:s.right,bottom:s.bottom,zIndex:s.zIndex,pointerEvents:s.pointerEvents,transform:s.transform,display:s.display},
    semantics:{tag:air.tagName,tabindex:air.getAttribute('tabindex'),role:air.getAttribute('role'),ariaHidden:air.getAttribute('aria-hidden'),links:air.querySelectorAll('a').length,buttons:air.querySelectorAll('button').length},
    overflow:{page:document.documentElement.scrollWidth>innerWidth+1,text:air.scrollWidth>air.clientWidth+1},
    targets:{contact:rect(document.querySelector('.home-contact__action')),footerNav:footerNavLinks.map(rect),footerSocial:footerSocialLinks.map(rect)},
    collisions:{contact:hit(document.querySelector('.home-contact__action')),footerNav:footerNavLinks.some(n=>hit(n)),footerSocial:footerSocialLinks.some(n=>hit(n)),linkedin:hit(document.querySelector('.home-hero__social[href*="linkedin"]')),github:hit(document.querySelector('.home-hero__social[href*="github"]'))}
  };
})()
"""


def capture_locale(locale: str, url: str, output: Path, chromium: str, harness: Any) -> dict[str, Any]:
    port = harness.available_port()
    with tempfile.TemporaryDirectory(prefix="air-00-evidence-") as profile:
        process = subprocess.Popen(
            [chromium, "--headless", "--no-sandbox", "--disable-gpu", "--no-proxy-server", "--remote-allow-origins=*", f"--remote-debugging-port={port}", f"--user-data-dir={profile}", f"--accept-lang={locale}", url],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        try:
            devtools = harness.DevTools(harness.page_websocket(port, url))
            devtools.call("Page.enable")
            devtools.call("Runtime.enable")
            devtools.call("Network.setExtraHTTPHeaders", {"headers": {"Accept-Language": locale}})
            deadline = time.monotonic() + 15
            while time.monotonic() < deadline:
                ready = devtools.call("Runtime.evaluate", {"expression": "document.readyState==='complete'", "returnByValue": True})
                if ready["result"].get("value") is True:
                    break
                time.sleep(0.05)
            devtools.call("Runtime.evaluate", {"expression": "document.documentElement.style.overflowAnchor='none';document.documentElement.style.scrollBehavior='auto'", "returnByValue": True})

            widths: dict[str, Any] = {}
            for width in (*REFERENCE_WIDTHS, *INTERPOLATION_WIDTHS):
                devtools.call("Emulation.setDeviceMetricsOverride", {"width": width, "height": 900, "deviceScaleFactor": 1, "mobile": False})
                positions = {
                    "top": "scrollTo(0,0)",
                    "middle": "scrollTo(0,document.documentElement.scrollHeight/2)",
                    "contact": "document.querySelector('.home-contact').scrollIntoView({block:'center'})",
                    "footer": "scrollTo(0,document.documentElement.scrollHeight)",
                }
                observations: dict[str, Any] = {}
                for name, expression in positions.items():
                    settled = f"(async()=>{{{expression};await new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r)));{expression};await new Promise(r=>requestAnimationFrame(r));return scrollY}})()"
                    devtools.call("Runtime.evaluate", {"expression": settled, "returnByValue": True, "awaitPromise": True})
                    observations[name] = devtools.call("Runtime.evaluate", {"expression": AIR_MEASURE_JS, "returnByValue": True})["result"]["value"]
                widths[str(width)] = {"reference": width in REFERENCE_WIDTHS, "positions": observations}
                if width in REFERENCE_WIDTHS:
                    shot = devtools.call("Page.captureScreenshot", {"format": "png", "captureBeyondViewport": False})
                    path = output / f"air-00-{locale.lower()}-{width}-footer.png"
                    path.write_bytes(base64.b64decode(shot["data"]))
                    widths[str(width)]["screenshot"] = str(path.relative_to(REPO_ROOT))
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
    parser.add_argument("--output", type=Path, default=Path("artifacts/responsive-visual/air-00-jujuju"))
    parser.add_argument("--chromium", default="chromium")
    args = parser.parse_args()
    args.output = args.output.resolve()
    args.output.mkdir(parents=True, exist_ok=True)
    harness = _harness()
    evidence = {
        "schema_version": 1,
        "environment": {"browser": subprocess.check_output([args.chromium, "--version"], text=True).strip(), "os": platform.platform(), "device_pixel_ratio": 1, "viewport_height": 900},
        "reference_widths": REFERENCE_WIDTHS,
        "interpolation_widths": INTERPOLATION_WIDTHS,
        "before_evidence": "artifacts/responsive-visual/hero-tech-refactor/hero-tech-refactor-visual-validation.json",
        "locales": [capture_locale(locale, args.url, args.output, args.chromium, harness) for locale in ("en-US", "pt-BR")],
    }
    destination = args.output / "air-00-position-validation.json"
    destination.write_text(json.dumps(evidence, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(destination)


if __name__ == "__main__":
    main()
