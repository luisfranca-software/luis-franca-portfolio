#!/usr/bin/env python3
"""Validate localized HERO-02 fit with real Chromium rendering."""

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

ROOT = Path(__file__).resolve().parents[1]
HARNESS = ROOT / "scripts/measure-responsive-fit.py"
CHECKPOINTS = (965, 966, 967, 968, 980, 1024, 1060, 1100, 1140, 1180,
               1190, 1198, 1199, 1200, 1201, 1301, 1302)
SCREENSHOTS = (967, 1024, 1100, 1199, 1200)

MEASURE = """
(() => {
  const title=document.querySelector('.home-hero__titles');
  const spans=[...title.querySelectorAll('.home-hero__title')];
  const rect=title.getBoundingClientRect(), style=getComputedStyle(title);
  const box=selector=>{const r=document.querySelector(selector).getBoundingClientRect();
    return {left:r.left,right:r.right,top:r.top,bottom:r.bottom,width:r.width,height:r.height};};
  const hero=box('.home-hero'),copy=box('.home-hero__copy'),visual=box('.home-hero__visual');
  const lines=spans.map(span => {
    const range=document.createRange(); range.selectNodeContents(span);
    const fragments=[...range.getClientRects()];
    const clone=span.cloneNode(true);
    clone.style.cssText='position:fixed;left:-10000px;top:0;display:inline-block;white-space:nowrap;width:max-content';
    title.appendChild(clone);
    const requiredWidth=clone.getBoundingClientRect().width;
    clone.remove();
    const box=span.getBoundingClientRect();
    return {text:span.textContent.trim(),requiredWidth,renderedWidth:box.width,
      renderedHeight:box.height,visualLines:fragments.length,
      overflow:requiredWidth-rect.width};
  });
  return {viewportWidth:innerWidth,availableWidth:rect.width,height:rect.height,
    layout:{hero,copy,visual,gap:visual.left-copy.right,overlap:copy.right>visual.left},
    fontSize:parseFloat(style.fontSize),lineHeight:parseFloat(style.lineHeight),
    fontFamily:style.fontFamily,fontWeight:style.fontWeight,letterSpacing:style.letterSpacing,lines,
    totalVisualLines:lines.reduce((total,line)=>total+line.visualLines,0),
    pageOverflow:document.documentElement.scrollWidth>innerWidth};
})()
"""

SEARCH = """
(() => {
  const title=document.querySelector('.home-hero__titles');
  const original=title.style.fontSize;
  const records=[];
  for (let tenth=200;tenth<=480;tenth++) {
    const size=tenth/10; title.style.fontSize=`${size}px`;
    const available=title.getBoundingClientRect().width;
    const widths=[...title.querySelectorAll('.home-hero__title')].map(span=>{
      const clone=span.cloneNode(true);
      clone.style.cssText='position:fixed;left:-10000px;top:0;display:inline-block;white-space:nowrap;width:max-content';
      title.appendChild(clone); const width=clone.getBoundingClientRect().width; clone.remove();
      return {text:span.textContent.trim(),requiredWidth:width};
    });
    const critical=widths.reduce((a,b)=>a.requiredWidth>b.requiredWidth?a:b);
    records.push({fontSize:size,availableWidth:available,criticalTitle:critical.text,
      requiredWidth:critical.requiredWidth,overflow:critical.requiredWidth-available,
      fits:critical.requiredWidth<=available});
  }
  title.style.fontSize=original;
  return {records,selected:[...records].reverse().find(record=>record.fits)};
})()
"""


def module() -> Any:
    spec = importlib.util.spec_from_file_location("fit_harness", HARNESS)
    if spec is None or spec.loader is None:
        raise RuntimeError("Unable to load Chromium harness")
    value = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(value)
    return value


def capture(locale: str, args: argparse.Namespace, fit: Any) -> dict[str, Any]:
    widths = sorted(set(range(967, 1200, 4)) | set(range(1200, 1302, 5)) |
                    set(CHECKPOINTS))
    port = fit.available_port()
    with tempfile.TemporaryDirectory(prefix="hero02-") as profile:
        process = subprocess.Popen([
            args.chromium, "--headless", "--no-sandbox", "--disable-gpu",
            "--hide-scrollbars", "--no-proxy-server", "--remote-allow-origins=*",
            f"--remote-debugging-port={port}", f"--user-data-dir={profile}",
            f"--accept-lang={locale}", args.url,
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        try:
            devtools = fit.DevTools(fit.page_websocket(port, args.url))
            devtools.call("Page.enable")
            devtools.call("Runtime.enable")
            devtools.call("Network.setExtraHTTPHeaders",
                          {"headers": {"Accept-Language": locale}})
            deadline = time.monotonic() + 15
            while time.monotonic() < deadline:
                result = devtools.call("Runtime.evaluate", {
                    "expression": "Boolean(document.querySelector('.home-hero__titles'))",
                    "returnByValue": True,
                })
                if result["result"].get("value"):
                    break
                time.sleep(.05)
            results=[]
            search=None
            for width in widths:
                devtools.call("Emulation.setDeviceMetricsOverride", {
                    "width": width, "height": 900, "deviceScaleFactor": 1,
                    "mobile": False,
                })
                if width == 1024:
                    search = devtools.call("Runtime.evaluate", {
                        "expression": SEARCH, "returnByValue": True,
                    })["result"]["value"]
                value = devtools.call("Runtime.evaluate", {
                    "expression": MEASURE, "returnByValue": True,
                })["result"]["value"]
                results.append(value)
                if width in SCREENSHOTS:
                    shot=devtools.call("Page.captureScreenshot", {
                        "format":"png", "captureBeyondViewport":False,
                        "clip":{"x":0,"y":0,"width":width,"height":700,"scale":1},
                    })
                    path=args.output/f"hero02-{locale.lower()}-{width}.png"
                    path.write_bytes(base64.b64decode(shot["data"]))
                    value["screenshot"]=str(path.relative_to(ROOT))
            return {"locale":locale,"candidateSearch":search,
                    "checkpoints":[r for r in results if r["viewportWidth"] in CHECKPOINTS],
                    "r3aSweep":[r for r in results if 967<=r["viewportWidth"]<=1199],
                    "r3bSweep":[r for r in results if 1200<=r["viewportWidth"]<=1301]}
        finally:
            process.terminate()
            process.wait(timeout=5)


def main() -> None:
    parser=argparse.ArgumentParser()
    parser.add_argument("--url",default="http://127.0.0.1:8000/")
    parser.add_argument("--chromium",default="chromium")
    parser.add_argument("--output",type=Path,
                        default=Path("artifacts/responsive-visual/r3-hero02"))
    args = parser.parse_args()
    args.output = args.output.resolve()
    args.output.mkdir(parents=True, exist_ok=True)
    fit=module()
    evidence = {
        "browser": subprocess.check_output(
            [args.chromium, "--version"], text=True
        ).strip(),
        "samplingIntervalMaxPx": 4,
        "authority": {
            "plateauCause": (
                "The >=967 .home-hero grid fixed its tracks at 416px 480px; "
                "the title inherited the 416px copy track."
            ),
            "r3cScope": "@media (min-width: 967px) and (max-width: 1199px)",
            "safeGap": (
                "32px measured at 967-1024; growth begins only when the protected "
                "480px visual moves right."
            ),
        },
        "model": {
            "leftColumn": (
                "clamp(416px, calc(82.14666193vw - 425.18181818px), "
                "560.578125px)"
            ),
            "enFont": "clamp(33px, calc(6.52314908vw - 33.79704662px), 48px)",
            "ptBrFont": (
                "clamp(30px, calc(5.94013006vw - 30.82693184px), 48px)"
            ),
            "runtimeFont": "Inter declaration resolves to installed Noto Sans fallback",
            "criticalWidthPerPx": {
                "en": 604.46875 / 48,
                "pt-BR": 663.796875 / 48,
            },
        },
        "frozenInvariants": {
            "r1PtBr360FontSize": "23.1px",
            "r2aR2bVisualGeometry": "unchanged",
            "r4DesktopPortraitY": "107.17px",
            "img02": "canonical asset, 100vw auto, repeat-y unchanged",
            "scopeAbove1199": "existing rules unchanged",
        },
        "locales": [capture(locale, args, fit) for locale in ("en-US", "pt-BR")],
    }
    destination=args.output/"hero02-fit-validation.json"
    destination.write_text(json.dumps(evidence,indent=2)+"\n",encoding="utf-8")
    print(destination)


if __name__ == "__main__":
    main()
