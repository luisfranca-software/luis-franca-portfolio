#!/usr/bin/env python3
"""Capture HERO-07 continuous responsive geometry evidence in Chromium."""

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
CHECKPOINTS = (768, 769, 800, 820, 850, 880, 900, 920, 940, 960, 966, 967)
REGRESSIONS = (360, 420, 650, 1024, 1440)
SCREENSHOTS = (768, 820, 900, 940, 966, 967)

MEASURE = """
(() => {
  const box = selector => {
    const r = document.querySelector(selector).getBoundingClientRect();
    return {left:r.left, right:r.right, top:r.top, bottom:r.bottom,
            width:r.width, height:r.height, centerX:(r.left+r.right)/2};
  };
  const parent=box('.home-hero__visual'), portrait=box('.home-hero__visual picture'),
        ide=box('.home-hero__ide'), gutter=box('.home-hero__gutter'),
        explorer=box('.home-hero__explorer');
  const visualNode=document.querySelector('.home-hero__visual');
  const computed=getComputedStyle(visualNode);
  const variables={group:{x:computed.getPropertyValue('--tech-group-x').trim()}};
  const consumers={
    portrait:visualNode.querySelector('picture'),
    ide:visualNode.querySelector('.home-hero__ide'),
    gutter:visualNode.querySelector('.home-hero__gutter'),
    explorer:visualNode.querySelector('.home-hero__explorer')
  };
  for (const component of ['portrait','ide','gutter','explorer']) {
    variables[component]={};
    for (const [property,cssProperty] of [['x','left'],['y','top'],['w','width']]) {
      const name=`--tech-${component}-${property}`;
      variables[component][property]={declared:computed.getPropertyValue(name).trim(),
        resolved:getComputedStyle(consumers[component]).getPropertyValue(cssProperty)};
    }
  }
  const ownership={
    portrait:{element:'picture',position:getComputedStyle(visualNode.querySelector('picture')).position},
    portraitImage:{element:'img',position:getComputedStyle(visualNode.querySelector('img')).position},
    ide:{element:'.home-hero__ide',position:getComputedStyle(visualNode.querySelector('.home-hero__ide')).position},
    gutter:{element:'.home-hero__gutter',position:getComputedStyle(visualNode.querySelector('.home-hero__gutter')).position},
    explorer:{element:'.home-hero__explorer',position:getComputedStyle(visualNode.querySelector('.home-hero__explorer')).position}
  };
  const children=[portrait,ide,gutter,explorer];
  const left=Math.min(...children.map(r=>r.left));
  const right=Math.max(...children.map(r=>r.right));
  const viewportCenterX=innerWidth/2;
  return {viewportWidth:innerWidth, viewportCenterX,variables,ownership,
    parent:{...parent,centerDelta:viewportCenterX-parent.centerX},
    portrait,ide,gutter,explorer,
    visualGroup:{left,right,width:right-left,centerX:(left+right)/2,
      centerDelta:viewportCenterX-(left+right)/2},
    horizontalOverflow:document.documentElement.scrollWidth>innerWidth};
})()
"""


def harness() -> Any:
    spec = importlib.util.spec_from_file_location("fit_harness", HARNESS)
    if spec is None or spec.loader is None:
        raise RuntimeError("Unable to load Chromium harness")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", default="http://127.0.0.1:8000/")
    parser.add_argument("--chromium", default="chromium")
    parser.add_argument("--output", type=Path,
                        default=Path("artifacts/responsive-visual/r2-hero07"))
    args = parser.parse_args()
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=True)
    fit = harness()
    widths = sorted(set(range(769, 967, 5)) | set(CHECKPOINTS) | set(REGRESSIONS))
    port = fit.available_port()
    with tempfile.TemporaryDirectory(prefix="hero07-") as profile:
        process = subprocess.Popen([
            args.chromium, "--headless", "--no-sandbox", "--disable-gpu", "--hide-scrollbars",
            "--no-proxy-server", "--remote-allow-origins=*",
            f"--remote-debugging-port={port}", f"--user-data-dir={profile}", args.url,
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        try:
            devtools = fit.DevTools(fit.page_websocket(port, args.url))
            devtools.call("Page.enable")
            devtools.call("Runtime.enable")
            deadline = time.monotonic() + 15
            while time.monotonic() < deadline:
                ready = devtools.call("Runtime.evaluate", {
                    "expression": "document.readyState === 'complete'", "returnByValue": True,
                })["result"].get("value")
                if ready:
                    break
                time.sleep(.05)
            results = []
            for width in widths:
                devtools.call("Emulation.setDeviceMetricsOverride", {
                    "width": width, "height": 900, "deviceScaleFactor": 1, "mobile": False,
                })
                evaluation = devtools.call("Runtime.evaluate", {
                    "expression": MEASURE, "returnByValue": True,
                })
                if "value" not in evaluation["result"]:
                    raise RuntimeError(evaluation)
                value = evaluation["result"]["value"]
                results.append(value)
                if width in SCREENSHOTS:
                    visual = value["parent"]
                    shot = devtools.call("Page.captureScreenshot", {
                        "format": "png", "captureBeyondViewport": True,
                        "clip": {"x": 0, "y": max(0, visual["top"] - 24),
                                 "width": width, "height": visual["height"] + 48, "scale": 1},
                    })
                    path = output / f"hero07-{width}.png"
                    path.write_bytes(base64.b64decode(shot["data"]))
                    value["screenshot"] = str(path.relative_to(ROOT))
            sweep = [r for r in results if 769 <= r["viewportWidth"] <= 966]
            fields = (("portrait", "left"), ("portrait", "width"), ("ide", "left"),
                      ("ide", "width"), ("gutter", "left"), ("gutter", "width"),
                      ("explorer", "left"), ("explorer", "width"))
            jumps = []
            maximum_step_deltas = {f"{node}.{field}": 0.0 for node, field in fields}
            for previous, current in zip(sweep, sweep[1:], strict=False):
                span = current["viewportWidth"] - previous["viewportWidth"]
                for node, field in fields:
                    delta = current[node][field] - previous[node][field]
                    key = f"{node}.{field}"
                    maximum_step_deltas[key] = max(
                        maximum_step_deltas[key], abs(delta)
                    )
                    if abs(delta) > span:
                        jumps.append({
                            "from": previous["viewportWidth"],
                            "to": current["viewportWidth"],
                            "property": f"{node}.{field}",
                            "delta": delta,
                        })
            evidence = {
                "browser": subprocess.check_output([args.chromium, "--version"], text=True).strip(),
                "sampling_interval_max_px": 5,
                "checkpoints": [r for r in results if r["viewportWidth"] in CHECKPOINTS],
                "regressions": [r for r in results if r["viewportWidth"] in REGRESSIONS],
                "sweep": sweep,
                "analysis": {
                    "abrupt_jumps": jumps,
                    "maximum_step_deltas": maximum_step_deltas,
                    "horizontal_overflow_widths": [
                        r["viewportWidth"]
                        for r in results
                        if r["horizontalOverflow"]
                    ],
                },
            }
            destination = output / "hero07-continuity-validation.json"
            destination.write_text(json.dumps(evidence, indent=2) + "\n", encoding="utf-8")
            print(destination)
        finally:
            process.terminate()
            process.wait(timeout=5)


if __name__ == "__main__":
    main()
