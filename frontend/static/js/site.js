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

    toggle.addEventListener("click", function () {
        const isOpen = menu.classList.toggle("is-open");
        toggle.setAttribute("aria-expanded", isOpen ? "true" : "false");
    });

    menu.querySelectorAll(".site-nav__link").forEach(function (link) {
        link.addEventListener("click", function () {
            menu.classList.remove("is-open");
            toggle.setAttribute("aria-expanded", "false");
        });
    });
})();
