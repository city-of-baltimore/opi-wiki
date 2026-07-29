(() => {
  "use strict";

  const paletteSelector = "[data-opi-palette-toggle]";

  const isVisible = (element) => {
    if (!(element instanceof HTMLElement) || element.closest("[inert]")) {
      return false;
    }
    const style = window.getComputedStyle(element);
    const rect = element.getBoundingClientRect();
    return (
      style.display !== "none" &&
      style.visibility !== "hidden" &&
      Number(style.opacity) !== 0 &&
      rect.width > 0 &&
      rect.height > 0 &&
      rect.right > 0 &&
      rect.bottom > 0 &&
      rect.left < window.innerWidth &&
      rect.top < window.innerHeight
    );
  };

  const cyclePalette = (button) => {
    const targetId = button.getAttribute("data-opi-palette-target");
    const input = targetId ? document.getElementById(targetId) : null;
    if (!(input instanceof HTMLInputElement)) return;
    input.click();
    window.requestAnimationFrame(() => {
      const next = document.querySelector(`${paletteSelector}:not([hidden])`);
      if (isVisible(next)) next.focus();
    });
  };

  document.addEventListener("click", (event) => {
    const target = event.target;
    if (!(target instanceof Element)) return;
    const button = target.closest(paletteSelector);
    if (button instanceof HTMLButtonElement) cyclePalette(button);
  });

  document.addEventListener(
    "keydown",
    (event) => {
      const target = event.target;
      if (
        event.key !== "Enter" ||
        !(target instanceof HTMLButtonElement) ||
        !target.matches(paletteSelector)
      ) {
        return;
      }
      // Intercept before Material's ancestor-form listener can also cycle.
      event.preventDefault();
      event.stopPropagation();
      cyclePalette(target);
    },
    true,
  );
})();
