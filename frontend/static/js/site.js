/* Minimal progressive enhancement for the responsive navigation toggle.
 *
 * Governing documents: SPEC-001 (SPEC-001-REQ-002), ARCH-001 (AR-007).
 * The menu remains accessible without JavaScript via the language fallback
 * and keyboard focus behavior; this script only adds the mobile toggle
 * interaction.
 */

(function () {
    "use strict";

    const toggle = document.querySelector(".site-nav__toggle");
    const menu = document.getElementById("site-nav-menu");

    if (!toggle || !menu) {
        return;
    }

    function closeMenu(returnFocus) {
        menu.classList.remove("is-open");
        toggle.setAttribute("aria-expanded", "false");
        if (returnFocus) {
            toggle.focus();
        }
    }

    toggle.addEventListener("click", function () {
        const isOpen = menu.classList.toggle("is-open");
        toggle.setAttribute("aria-expanded", isOpen ? "true" : "false");
    });

    menu.querySelectorAll(".site-nav__link").forEach(function (link) {
        link.addEventListener("click", function () {
            closeMenu(false);
        });
    });

    document.addEventListener("keydown", function (event) {
        if (event.key === "Escape" && menu.classList.contains("is-open")) {
            closeMenu(true);
        }
    });

    // Mirrors FIT-HDR-001's validated 848px / 53rem boundary to clear stale
    // Compact disclosure state when the Full Header becomes active.
    const fullHeaderQuery = window.matchMedia("(min-width: 53rem)");
    function resetCompactState(event) {
        if (event.matches) {
            closeMenu(false);
        }
    }

    if (typeof fullHeaderQuery.addEventListener === "function") {
        fullHeaderQuery.addEventListener("change", resetCompactState);
    } else {
        fullHeaderQuery.addListener(resetCompactState);
    }
})();
