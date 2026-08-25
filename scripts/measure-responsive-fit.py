#!/usr/bin/env python3
# ruff: noqa: E501
"""Measure SDD-RWD-001 FIT transitions with Chromium's DevTools protocol."""

from __future__ import annotations

import argparse
import base64
import http.client
import json
import os
import platform
import socket
import struct
import subprocess
import tempfile
import time
from pathlib import Path
from typing import Any

FIT_DEFINITIONS = {
    "FIT-HDR-001": ("header", 769, 1024, ".site-header"),
    "FIT-HERO-001": ("hero", 769, 1024, ".home-hero"),
    "FIT-ENG-001": ("engineering", 361, 768, ".home-engineering"),
    "FIT-ENG-002": ("engineering", 1025, 1440, ".home-engineering"),
    "FIT-PRJ-001": ("projects", 769, 1024, ".home-projects"),
    "FIT-PRJ-002": ("projects", 1025, 1440, ".home-projects"),
    "FIT-PRC-001": ("process", 361, 768, ".home-process"),
    "FIT-PRC-002": ("process", 769, 1024, ".home-process"),
    "FIT-PRC-003": ("process", 1025, 1440, ".home-process"),
    "FIT-EVD-001": ("evidence", 361, 768, ".home-evidence"),
    "FIT-EVD-002": ("evidence", 1025, 1440, ".home-evidence"),
    "FIT-EVD-003": ("evidence-contact", 1025, 1440, ".home-evidence-contact"),
    "FIT-FTR-001": ("footer", 361, 768, ".site-footer--homepage"),
}

EXPECTED_TRANSITIONS = {
    "FIT-HDR-001": 848,
    "FIT-HERO-001": 967,
    "FIT-ENG-001": 640,
    "FIT-ENG-002": 1200,
    "FIT-PRJ-001": 896,
    "FIT-PRJ-002": 1200,
    "FIT-PRC-001": 640,
    "FIT-PRC-002": 896,
    "FIT-PRC-003": 1200,
    "FIT-EVD-001": 640,
    "FIT-EVD-002": 1200,
    "FIT-EVD-003": 1200,
    "FIT-FTR-001": 640,
}

MEASURE_JS = r"""
(() => {
  const rect = (selector) => {
    const node = document.querySelector(selector);
    if (!node) return null;
    const r = node.getBoundingClientRect();
    return {x:r.x, y:r.y, width:r.width, height:r.height,
      scrollWidth:node.scrollWidth, clientWidth:node.clientWidth,
      overflowX:node.scrollWidth > node.clientWidth + 1};
  };
  const columns = (selector) => {
    const node = document.querySelector(selector);
    if (!node) return 0;
    const value = getComputedStyle(node).gridTemplateColumns;
    return value === 'none' ? 0 : value.split(' ').filter(Boolean).length;
  };
  const traceRects = Object.fromEntries(
    [...document.querySelectorAll('[data-trace-id]')].map((node) => {
      const r = node.getBoundingClientRect();
      return [node.dataset.traceId, {x:r.x, y:r.y, width:r.width, height:r.height}];
    })
  );
  const visible = (selector) => {
    const node = document.querySelector(selector);
    return !!node && getComputedStyle(node).display !== 'none';
  };
  const intersects = (a, b) => {
    const x = document.querySelector(a), y = document.querySelector(b);
    if (!x || !y || getComputedStyle(x).display === 'none' || getComputedStyle(y).display === 'none') return false;
    const r=x.getBoundingClientRect(), s=y.getBoundingClientRect();
    return r.left < s.right && r.right > s.left && r.top < s.bottom && r.bottom > s.top;
  };
  const brokenWords = (selector) => {
    const failures = [];
    document.querySelectorAll(selector).forEach((node) => {
      const walker = document.createTreeWalker(node, NodeFilter.SHOW_TEXT);
      while (walker.nextNode()) {
        const text = walker.currentNode.textContent || '';
        for (const match of text.matchAll(/\S+/g)) {
          if (match[0].includes('-')) continue;
          const range = document.createRange();
          range.setStart(walker.currentNode, match.index);
          range.setEnd(walker.currentNode, match.index + match[0].length);
          if (range.getClientRects().length > 1) failures.push(match[0]);
        }
      }
    });
    return failures;
  };
  const ai = '.home-ai-rag';
  const aiCollisions = ['.home-contact__action','.homepage-footer__nav','.homepage-footer__social','.site-nav__menu'].filter(s => intersects(ai,s));
  return {
    viewport: {width:innerWidth,height:innerHeight,dpr:devicePixelRatio,scrollWidth:document.documentElement.scrollWidth},
    language: document.documentElement.lang,
    mode: {
      header: visible('.site-nav__toggle') ? 'compact' : 'full',
      hero: columns('.home-hero') === 1 ? 'stacked' : 'split',
      engineering: columns('.home-engineering__list'),
      projects: columns('.home-projects__list') === 4 ? 2 : columns('.home-projects__list'),
      process: columns('.home-process__list'),
      evidence: columns('.home-evidence__list'),
      evidenceContact: columns('.home-evidence-contact') === 1 ? 'stacked' : 'side',
      footer: columns('.homepage-footer') === 1 ? 'stacked' : 'horizontal'
    },
    geometry: {
      header: rect('.site-nav'), headerMenu: rect('.site-nav__menu'), hero: rect('.home-hero'), heroCopy: rect('.home-hero__copy'), engineeringCard: rect('.home-engineering__item'),
      projectCard: rect('.home-project'), processStep: rect('.home-process__step'),
      evidenceCard: rect('.home-evidence__item'), contact: rect('.home-contact'), footer: rect('.homepage-footer')
    },
    traceRects,
    overflow: {
      page: document.documentElement.scrollWidth > innerWidth + 1,
      selectors: ['.site-nav','.home-hero','.home-engineering','.home-projects','.home-process','.home-evidence-contact','.homepage-footer']
        .filter(s => {const n=document.querySelector(s); return n && n.scrollWidth > n.clientWidth + 1;})
    },
    collisions: {
      header: [
        ['.site-nav__brand','.site-nav__menu'],['.site-nav__menu','.language-selector'],
        ['.site-nav__brand','.site-nav__toggle'],['.site-nav__toggle','.language-selector']
      ].filter(pair => intersects(pair[0],pair[1])),
      hero: intersects('.home-hero__copy','.home-hero__visual'),
      ai: aiCollisions
    },
    brokenWords: {
      header: brokenWords('.site-nav'), hero: brokenWords('.home-hero__copy'),
      engineering: brokenWords('.home-engineering__item'), projects: brokenWords('.home-project'),
      process: brokenWords('.home-process__step'), evidence: brokenWords('.home-evidence-contact'),
      footer: brokenWords('.homepage-footer')
    },
    background: document.querySelector('.homepage') ? getComputedStyle(document.querySelector('.homepage')).backgroundImage : null,
    content: {
      h1: document.querySelectorAll('h1').length,
      sections: ['engineering','projects','process','evidence','contact'].every(id => !!document.getElementById(id)),
      portuguese: document.body.innerText.includes('Engenheiro de Software') && document.body.innerText.includes('O que eu desenvolvo')
    }
  };
})()
"""


class DevTools:
    def __init__(self, websocket_url: str) -> None:
        target = websocket_url.removeprefix("ws://")
        host_port, path = target.split("/", 1)
        host, port = host_port.split(":")
        self.sock = socket.create_connection((host, int(port)), timeout=10)
        self.sock.settimeout(60)
        key = base64.b64encode(os.urandom(16)).decode()
        request = (
            f"GET /{path} HTTP/1.1\r\nHost: {host_port}\r\nUpgrade: websocket\r\n"
            f"Connection: Upgrade\r\nSec-WebSocket-Key: {key}\r\nSec-WebSocket-Version: 13\r\n\r\n"
        )
        self.sock.sendall(request.encode())
        response = self.sock.recv(4096)
        if b" 101 " not in response:
            raise RuntimeError(f"WebSocket upgrade failed: {response[:120]!r}")
        self.next_id = 0

    def _send(self, payload: bytes) -> None:
        mask = os.urandom(4)
        length = len(payload)
        header = bytearray([0x81])
        if length < 126:
            header.append(0x80 | length)
        elif length < 65536:
            header.append(0x80 | 126)
            header.extend(struct.pack("!H", length))
        else:
            header.append(0x80 | 127)
            header.extend(struct.pack("!Q", length))
        header.extend(mask)
        header.extend(bytes(value ^ mask[index % 4] for index, value in enumerate(payload)))
        self.sock.sendall(header)

    def _recv(self) -> dict[str, Any]:
        first = self.sock.recv(2)
        if len(first) < 2:
            raise RuntimeError("WebSocket closed")
        opcode = first[0] & 0x0F
        length = first[1] & 0x7F
        if length == 126:
            length = struct.unpack("!H", self._read(2))[0]
        elif length == 127:
            length = struct.unpack("!Q", self._read(8))[0]
        payload = self._read(length)
        if opcode == 8:
            raise RuntimeError("WebSocket closed by Chromium")
        if opcode == 9:
            self._send(payload)
            return self._recv()
        return json.loads(payload)

    def _read(self, length: int) -> bytes:
        chunks = bytearray()
        while len(chunks) < length:
            chunks.extend(self.sock.recv(length - len(chunks)))
        return bytes(chunks)

    def call(self, method: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        self.next_id += 1
        command_id = self.next_id
        self._send(json.dumps({"id": command_id, "method": method, "params": params or {}}).encode())
        while True:
            message = self._recv()
            if message.get("id") == command_id:
                if "error" in message:
                    raise RuntimeError(message["error"])
                return message.get("result", {})


def available_port() -> int:
    with socket.socket() as probe:
        probe.bind(("127.0.0.1", 0))
        return int(probe.getsockname()[1])


def page_websocket(port: int, expected_url: str) -> str:
    deadline = time.monotonic() + 15
    while time.monotonic() < deadline:
        try:
            connection = http.client.HTTPConnection("127.0.0.1", port, timeout=1)
            connection.request("GET", "/json/list")
            payload = json.loads(connection.getresponse().read())
            connection.close()
            for target in payload:
                if target.get("type") == "page" and target.get("url") == expected_url:
                    return str(target["webSocketDebuggerUrl"])
        except (ConnectionError, OSError, json.JSONDecodeError):
            time.sleep(0.1)
    raise RuntimeError("Chromium DevTools endpoint did not become ready")


def mode_for(fit_id: str, result: dict[str, Any]) -> Any:
    modes = result["mode"]
    return {
        "FIT-HDR-001": modes["header"], "FIT-HERO-001": modes["hero"],
        "FIT-ENG-001": modes["engineering"], "FIT-ENG-002": modes["engineering"],
        "FIT-PRJ-001": modes["projects"], "FIT-PRJ-002": modes["projects"],
        "FIT-PRC-001": modes["process"], "FIT-PRC-002": modes["process"], "FIT-PRC-003": modes["process"],
        "FIT-EVD-001": modes["evidence"], "FIT-EVD-002": modes["evidence"],
        "FIT-EVD-003": modes["evidenceContact"], "FIT-FTR-001": modes["footer"],
    }[fit_id]


def healthy_for(fit_id: str, result: dict[str, Any]) -> bool:
    component = FIT_DEFINITIONS[fit_id][0]
    selector_overflow = result["overflow"]["selectors"]
    if fit_id == "FIT-HERO-001":
        # The approved Hero intentionally layers portrait/code inside a clipped
        # local composition; only page-level overflow is a FIT failure.
        selector_overflow = [
            selector for selector in selector_overflow if selector != ".home-hero"
        ]
    general = (
        not result["overflow"]["page"]
        and not selector_overflow
        and not result["collisions"]["header"]
        and not result["collisions"]["hero"]
    )
    if not general or result["brokenWords"][component.split("-")[0]]:
        return False
    if fit_id == "FIT-HDR-001":
        # Full Header authority is 80px at 848+; Compact remains 72px.
        return result["geometry"]["header"]["height"] <= 80
    return True


def run_locale(
    locale: str,
    url: str,
    output: Path,
    chromium: str,
    validation_state: str,
    screenshot_subdir: str,
) -> dict[str, Any]:
    port = available_port()
    with tempfile.TemporaryDirectory(prefix="responsive-fit-") as profile:
        process = subprocess.Popen(
            [chromium, "--headless", "--no-sandbox", "--disable-gpu", "--no-proxy-server", "--remote-allow-origins=*",
             f"--remote-debugging-port={port}", f"--user-data-dir={profile}", f"--accept-lang={locale}", url],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        )
        try:
            devtools = DevTools(page_websocket(port, url))
            devtools.call("Page.enable")
            devtools.call("Runtime.enable")
            devtools.call("Network.enable")
            devtools.call("Network.setExtraHTTPHeaders", {"headers": {"Accept-Language": locale}})
            devtools.call("Emulation.setDeviceMetricsOverride", {"width": 1440, "height": 900, "deviceScaleFactor": 1, "mobile": False})
            deadline = time.monotonic() + 15
            while time.monotonic() < deadline:
                readiness = devtools.call("Runtime.evaluate", {"expression": "({ready:document.readyState,url:location.href})", "returnByValue": True})
                value = readiness["result"].get("value", {})
                if value.get("ready") == "complete" and value.get("url") == url:
                    break
                time.sleep(0.05)
            page = devtools.call("Runtime.evaluate", {"expression": "({homepage:!!document.querySelector('.homepage'),title:document.title,text:document.body.innerText.slice(0,200)})", "returnByValue": True})
            if not page["result"].get("value", {}).get("homepage"):
                raise RuntimeError(f"Chromium did not render the Homepage: {page}")
            measurements: dict[str, Any] = {}
            for width in range(360, 1441):
                devtools.call("Emulation.setDeviceMetricsOverride", {"width": width, "height": 900, "deviceScaleFactor": 1, "mobile": False})
                result = devtools.call("Runtime.evaluate", {"expression": MEASURE_JS, "returnByValue": True})
                if "value" not in result["result"]:
                    raise RuntimeError(f"Measurement failed at {locale} {width}px: {result}")
                measurements[str(width)] = result["result"]["value"]

            transitions: dict[str, Any] = {}
            screenshot_dir = output.parent / screenshot_subdir
            screenshot_dir.mkdir(parents=True, exist_ok=True)
            for fit_id, (_component, low, high, selector) in FIT_DEFINITIONS.items():
                expected = EXPECTED_TRANSITIONS[fit_id]
                baseline_width = low - 1 if low > 360 else low
                baseline_mode = mode_for(fit_id, measurements[str(baseline_width)])
                observed_switch = next(
                    (width for width in range(low, high + 1)
                     if mode_for(fit_id, measurements[str(width)]) != baseline_mode),
                    None,
                )
                if observed_switch is None:
                    raise RuntimeError(
                        f"No transition for {fit_id} in {locale} interval {low}-{high}; "
                        f"mode remained {baseline_mode!r}; baseline={measurements[str(baseline_width)]}"
                    )
                observed = next(
                    (width for width in range(observed_switch, high + 1)
                     if healthy_for(fit_id, measurements[str(width)])),
                    None,
                )
                if observed is None:
                    raise RuntimeError(
                        f"No healthy larger mode for {fit_id} in {locale} through {high}px"
                    )
                probes = {}
                for width in (observed - 1, observed, observed + 1):
                    value = measurements[str(width)]
                    probes[str(width)] = {
                        "mode": mode_for(fit_id, value), "overflow": value["overflow"],
                        "collisions": value["collisions"], "geometry": value["geometry"],
                        "broken_words": value["brokenWords"],
                        "healthy": healthy_for(fit_id, value),
                    }
                devtools.call("Emulation.setDeviceMetricsOverride", {"width": observed, "height": 900, "deviceScaleFactor": 1, "mobile": False})
                devtools.call("Runtime.evaluate", {"expression": f"document.documentElement.style.scrollBehavior='auto';document.querySelector({json.dumps(selector)}).scrollIntoView({{behavior:'instant',block:'center'}})"})
                shot = devtools.call("Page.captureScreenshot", {"format": "png", "captureBeyondViewport": False})
                screenshot = screenshot_dir / f"{fit_id}-{locale.lower()}-{observed}.png"
                screenshot.write_bytes(base64.b64decode(shot["data"]))
                transitions[fit_id] = {
                    "candidate_interval": [low, high], "implemented_threshold": expected,
                    "mode_switch": observed_switch,
                    "measured_transition": observed,
                    "last_healthy_smaller_mode_width": observed_switch - 1,
                    "first_healthy_larger_mode_width": observed, "probes": probes,
                    "screenshot": str(screenshot.relative_to(output.parent.parent)), "state": validation_state,
                }
            diagnostic_widths = (360, 390, 480, 640, 768, 769, 820, 896, 900, 1024, 1100, 1200, 1280, 1440)
            diagnostics = {str(width): measurements[str(width)] for width in diagnostic_widths}
            ai_observations: dict[str, Any] = {}
            for width in diagnostic_widths:
                devtools.call("Emulation.setDeviceMetricsOverride", {"width": width, "height": 900, "deviceScaleFactor": 1, "mobile": False})
                script = r"""
                (() => {
                  const ai=document.querySelector('.home-ai-rag');
                  const hit=(selector) => {const n=document.querySelector(selector); if(!n)return false; const a=ai.getBoundingClientRect(),b=n.getBoundingClientRect(); return a.left<b.right&&a.right>b.left&&a.top<b.bottom&&a.bottom>b.top;};
                  const result={};
                  document.querySelector('.home-contact__action').scrollIntoView({block:'center'});
                  result.contact=hit('.home-contact__action');
                  scrollTo(0, document.documentElement.scrollHeight);
                  result.footerNavigation=hit('.homepage-footer__nav');
                  result.footerSocial=hit('.homepage-footer__social');
                  return result;
                })()
                """
                observed_ai = devtools.call("Runtime.evaluate", {"expression": script, "returnByValue": True})
                ai_observations[str(width)] = observed_ai["result"]["value"]
            return {
                "locale": locale,
                "sweep": {
                    "from": 360, "through": 1440, "step_css_px": 1,
                    "page_overflow_widths": [int(width) for width, value in measurements.items() if value["overflow"]["page"]],
                },
                "diagnostics": diagnostics,
                "ai_rag_collision_observations": ai_observations,
                "transitions": transitions,
            }
        finally:
            process.terminate()
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", default="http://127.0.0.1:8000/")
    parser.add_argument("--output", type=Path, default=Path("artifacts/responsive-fit/block12-fit-measurements.json"))
    parser.add_argument("--chromium", default="chromium")
    parser.add_argument("--state", choices=("FIT-TESTED", "FIT-VALIDATED"), default="FIT-TESTED")
    parser.add_argument("--screenshot-subdir", default="screenshots")
    args = parser.parse_args()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    locales = [
        run_locale(
            locale,
            args.url,
            args.output,
            args.chromium,
            args.state,
            args.screenshot_subdir,
        )
        for locale in ("en-US", "pt-BR")
    ]
    document = {
        "schema_version": 1,
        "environment": {"browser": subprocess.check_output([args.chromium, "--version"], text=True).strip(),
                        "headless": True, "os": platform.platform(), "device_pixel_ratio": 1,
                        "zoom": "100%", "viewport_height": 900, "css_pixels_authoritative": True},
        "method": "Progressive 1 CSS-pixel sweep across 360–1440 for both locales; N-1/N/N+1 geometry probes.",
        "fit_inventory": list(FIT_DEFINITIONS), "locales": locales,
    }
    args.output.write_text(json.dumps(document, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(args.output)


if __name__ == "__main__":
    main()
