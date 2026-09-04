/* Progressive enhancement for the homepage IA Jujuju panel.
 *
 * Keeps assistant-specific behavior isolated from site-wide navigation logic.
 */

(function () {
    "use strict";

    if (window.IAJujuju) {
        return;
    }

    const reducedMotionQuery = window.matchMedia("(prefers-reduced-motion: reduce)");

    function getContainer() {
        return document.getElementById("assistant-container");
    }

    function getLauncher() {
        return document.querySelector(".home-ai-rag");
    }

    function setOpenState(isOpen) {
        const launcher = getLauncher();
        if (launcher) {
            launcher.setAttribute("aria-expanded", isOpen ? "true" : "false");
        }
        document.body.classList.toggle("assistant-open", isOpen);
    }

    function scrollMessages(panel) {
        if (!panel) {
            return;
        }
        const messages = panel.querySelector(".assistant-panel__messages");
        if (!messages) {
            return;
        }
        window.requestAnimationFrame(function () {
            messages.scrollTop = messages.scrollHeight;
        });
    }

    function revealAssistantContent(root) {
        if (reducedMotionQuery.matches) {
            root.querySelectorAll("[data-assistant-reveal='pending']").forEach(function (node) {
                node.dataset.assistantReveal = "done";
            });
            return;
        }

        root.querySelectorAll("[data-assistant-reveal='pending']").forEach(function (node) {
            node.dataset.assistantReveal = "running";
            const words = [];
            wrapWords(node, words);
            const maxDelay = 360;
            const delayStep = words.length > 0 ? Math.min(18, maxDelay / words.length) : 0;

            words.forEach(function (word, index) {
                word.style.setProperty(
                    "--assistant-word-delay",
                    Math.min(Math.round(index * delayStep), maxDelay) + "ms"
                );
            });
            node.dataset.assistantReveal = "done";
        });
    }

    function wrapWords(root, words) {
        Array.from(root.childNodes).forEach(function (child) {
            if (child.nodeType === Node.TEXT_NODE) {
                const fragment = document.createDocumentFragment();
                const parts = child.textContent.split(/(\s+)/);

                parts.forEach(function (part) {
                    if (!part) {
                        return;
                    }
                    if (/^\s+$/.test(part)) {
                        fragment.appendChild(document.createTextNode(part));
                        return;
                    }
                    const span = document.createElement("span");
                    span.className = "assistant-message__word";
                    span.textContent = part;
                    words.push(span);
                    fragment.appendChild(span);
                });

                child.replaceWith(fragment);
                return;
            }

            if (child.nodeType === Node.ELEMENT_NODE) {
                wrapWords(child, words);
            }
        });
    }

    function enhancePanel(root) {
        const panel = root.matches(".assistant-panel") ? root : root.querySelector(".assistant-panel");
        if (!panel) {
            setOpenState(false);
            return;
        }

        setOpenState(true);
        revealAssistantContent(panel);
        scrollMessages(panel);
    }

    function closePanel(closeButton) {
        const panel = closeButton.closest(".assistant-panel");
        if (panel) {
            panel.remove();
        }
        const container = getContainer();
        if (container) {
            container.innerHTML = "";
        }
        setOpenState(false);
    }

    document.addEventListener("DOMContentLoaded", function () {
        enhancePanel(document);
    });

    document.body.addEventListener("htmx:afterSwap", function (event) {
        const target = event.detail && event.detail.target;
        if (!target) {
            return;
        }

        if (target.id === "assistant-container" || target.id === "assistant-messages") {
            enhancePanel(target);
        }
    });

    document.body.addEventListener("htmx:beforeRequest", function (event) {
        const element = event.detail && event.detail.elt;
        if (element && element.classList && element.classList.contains("assistant-panel__form")) {
            const panel = element.closest(".assistant-panel");
            scrollMessages(panel);
        }
    });

    window.IAJujuju = {
        closePanel: closePanel,
    };
})();
