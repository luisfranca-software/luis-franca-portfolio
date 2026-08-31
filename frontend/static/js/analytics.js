/* Minimal privacy-preserving analytics event transport for Release 1.1.
 *
 * Governing documents: ADR-001 (Release 1.1 analytics), ARCH-001 (15.7 PII).
 * Events are sent to the server-side analytics endpoint via navigator.sendBeacon
 * when available, with a fetch fallback. No personal data is captured.
 *
 * The server records the request path and language automatically; only
 * approved event types and allowlisted metadata keys are persisted.
 */

(function () {
    "use strict";

    var endpoint = "/analytics/event/";
    var csrfValue = "";
    var csrfMeta = document.querySelector('meta[name="csrf-token"]');
    if (csrfMeta) {
        csrfValue = csrfMeta.getAttribute("content") || "";
    }

    function sendEvent(eventType, metadata) {
        var data = new FormData();
        data.append("event_type", eventType);
        data.append("csrfmiddlewaretoken", csrfValue);
        if (metadata && typeof metadata === "object") {
            data.append("metadata", JSON.stringify(metadata));
        }

        if (navigator.sendBeacon) {
            try {
                navigator.sendBeacon(endpoint, data);
                return;
            } catch (e) {
                // Fall through to fetch fallback.
            }
        }

        if (window.fetch) {
            fetch(endpoint, {
                method: "POST",
                body: data,
                credentials: "same-origin",
                keepalive: true,
            }).catch(function () {
                // Analytics transport failures are non-critical.
            });
        }
    }

    function attachClickEvents() {
        document.querySelectorAll("[data-analytics]").forEach(function (element) {
            element.addEventListener("click", function () {
                var eventType = element.getAttribute("data-analytics");
                var metadata = {};
                var metaAttr = element.getAttribute("data-analytics-meta");
                if (metaAttr) {
                    try {
                        metadata = JSON.parse(metaAttr);
                    } catch (e) {
                        metadata = { value: metaAttr };
                    }
                }
                sendEvent(eventType, metadata);
            });
        });
    }

    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", attachClickEvents);
    } else {
        attachClickEvents();
    }
})();
