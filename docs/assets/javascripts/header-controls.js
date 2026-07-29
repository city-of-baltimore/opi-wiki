(() => {
  "use strict";

  const drawerMedia = window.matchMedia("(max-width: 76.234375em)");
  const searchMedia = window.matchMedia("(max-width: 59.984375em)");
  const invokers = { drawer: null, search: null };
  let viewportFocus = null;
  let viewportFocusFrame = 0;
  let viewportRevision = 0;
  let pendingDestinationFocus = false;

  const drawerToggle = document.querySelector("#__drawer");
  const searchToggle = document.querySelector("#__search");
  if (!(drawerToggle instanceof HTMLInputElement)) return;

  const getDrawer = () => document.querySelector(".md-sidebar--primary");
  const getSearch = () => document.querySelector("#opi-search");
  const getControl = (name) => document.querySelector(`[data-opi-${name}-open]`);
  const getBrand = () => document.querySelector(".opi-header__brand");
  const panels = {
    drawer: {
      toggle: drawerToggle,
      media: drawerMedia,
      getSurface: getDrawer,
      label: "Primary navigation",
      initialFocus: "[data-opi-drawer-close]",
    },
    search: {
      toggle: searchToggle,
      media: searchMedia,
      getSurface: getSearch,
      label: "Search",
      initialFocus: ".md-search__input",
    },
  };

  const isRendered = (element) => {
    if (!(element instanceof HTMLElement) || element.closest("[inert]")) return false;
    const style = window.getComputedStyle(element);
    const rect = element.getBoundingClientRect();
    return (
      style.display !== "none" &&
      style.visibility !== "hidden" &&
      Number(style.opacity) !== 0 &&
      rect.width > 0 &&
      rect.height > 0
    );
  };

  const isVisible = (element) => {
    if (!isRendered(element)) return false;
    const rect = element.getBoundingClientRect();
    return (
      rect.right > 0 &&
      rect.bottom > 0 &&
      rect.left < window.innerWidth &&
      rect.top < window.innerHeight
    );
  };

  const focusableElements = (surface) => {
    if (!(surface instanceof HTMLElement)) return [];
    const surfaceRect = surface.getBoundingClientRect();
    const selector = [
      "a[href]",
      "button:not([disabled])",
      "input:not([disabled]):not([type='hidden'])",
      "select:not([disabled])",
      "textarea:not([disabled])",
      "[tabindex]:not([tabindex='-1'])",
    ].join(",");
    return [...surface.querySelectorAll(selector)].filter((element) => {
      if (!isRendered(element) || element.tabIndex < 0) return false;
      const rect = element.getBoundingClientRect();
      return (
        rect.right > surfaceRect.left &&
        rect.left < surfaceRect.right
      );
    });
  };

  const prepareSurfaces = () => {
    const drawer = getDrawer();
    const drawerControl = getControl("drawer");
    if (
      !(drawer instanceof HTMLElement) ||
      !(drawerControl instanceof HTMLButtonElement)
    ) {
      return false;
    }
    drawer.id = "opi-primary-navigation";

    const searchControl = getControl("search");
    if (
      searchControl &&
      (!(searchControl instanceof HTMLButtonElement) ||
        !(searchToggle instanceof HTMLInputElement) ||
        !(getSearch() instanceof HTMLElement))
    ) {
      return false;
    }
    return true;
  };

  const focusDestination = () => {
    const destination =
      document.querySelector(".md-content h1") ||
      document.querySelector("main");
    if (!(destination instanceof HTMLElement)) return;
    const suppliedTabIndex = destination.hasAttribute("tabindex");
    if (!suppliedTabIndex) {
      destination.setAttribute("tabindex", "-1");
      destination.addEventListener(
        "blur",
        () => destination.removeAttribute("tabindex"),
        { once: true },
      );
    }
    destination.focus({ preventScroll: true });
  };

  const restoreInvoker = (name) => {
    const invoker = invokers[name];
    invokers[name] = null;
    if (!(invoker instanceof HTMLElement)) return;
    const fallback = getControl(name);
    const target = isVisible(invoker) ? invoker : fallback;
    if (isVisible(target)) target.focus();
  };

  const syncPanel = (name) => {
    const panel = panels[name];
    const { toggle, media, getSurface, label } = panel;
    if (!(toggle instanceof HTMLInputElement)) return;
    const surface = getSurface();
    const control = getControl(name);
    const modal = media.matches;
    const open = toggle.checked;
    if (control instanceof HTMLElement) {
      control.setAttribute("aria-expanded", String(open));
    }
    if (!(surface instanceof HTMLElement)) return;

    if (modal) {
      if (
        !open &&
        !pendingDestinationFocus &&
        surface.contains(document.activeElement)
      ) {
        const fallback = getControl(name);
        if (isVisible(fallback)) {
          fallback.focus();
        }
      }
      surface.inert = !open;
      surface.setAttribute("role", "dialog");
      surface.setAttribute("aria-label", label);
      surface.setAttribute("aria-modal", "true");
      surface.setAttribute("aria-hidden", String(!open));
    } else {
      surface.inert = false;
      ["role", "aria-label", "aria-modal", "aria-hidden"].forEach((attribute) =>
        surface.removeAttribute(attribute),
      );
    }
  };

  const syncPanels = () => {
    Object.keys(panels).forEach(syncPanel);
  };

  const focusOpenedSurface = (name) => {
    const panel = panels[name];
    const target = panel.getSurface()?.querySelector(panel.initialFocus);
    if (target instanceof HTMLElement && !target.closest("[inert]")) {
      // Keep focus in the originating user gesture. This is required to open
      // mobile keyboards reliably and avoids waiting for the panel animation.
      target.focus();
    }
  };

  const closeSurface = (name, restore = true) => {
    const { toggle } = panels[name];
    if (!(toggle instanceof HTMLInputElement)) return;
    if (!restore) invokers[name] = null;
    if (toggle.checked) {
      toggle.click();
    } else if (restore) {
      restoreInvoker(name);
    }
  };

  const openSurface = (name, invoker) => {
    const panel = panels[name];
    const { toggle } = panel;
    const otherName = name === "drawer" ? "search" : "drawer";
    const otherToggle = panels[otherName].toggle;
    if (!(toggle instanceof HTMLInputElement)) return;

    if (otherToggle instanceof HTMLInputElement && otherToggle.checked) {
      closeSurface(otherName, false);
    }
    invokers[name] = invoker;

    const surface = panel.getSurface();
    if (surface instanceof HTMLElement) {
      surface.inert = false;
      surface.removeAttribute("aria-hidden");
    }
    if (!toggle.checked) {
      toggle.click();
    }
    focusOpenedSurface(name);
  };

  const handleSearchShortcut = (event) => {
    if (
      !(searchToggle instanceof HTMLInputElement) ||
      !searchMedia.matches ||
      searchToggle.checked ||
      event.altKey ||
      event.ctrlKey ||
      event.metaKey ||
      event.defaultPrevented
    ) {
      return false;
    }
    const target = event.target;
    if (
      target instanceof HTMLElement &&
      (target.isContentEditable ||
        target.matches("input, select, textarea, [role='textbox']"))
    ) {
      return false;
    }
    if (!["/", "f", "s"].includes(event.key.toLowerCase())) {
      return false;
    }

    const active = document.activeElement;
    const invoker =
      active instanceof HTMLElement && active !== document.body
        ? active
        : getControl("search");
    openSurface("search", invoker);
    event.preventDefault();
    event.stopPropagation();
    return true;
  };

  const activeModal = () => {
    for (const name of ["search", "drawer"]) {
      const panel = panels[name];
      if (
        panel.toggle instanceof HTMLInputElement &&
        panel.media.matches &&
        panel.toggle.checked
      ) {
        return { name, surface: panel.getSurface() };
      }
    }
    return null;
  };

  document.addEventListener("click", (event) => {
    const target = event.target;
    if (!(target instanceof Element)) return;
    const button = target.closest("button");
    if (!(button instanceof HTMLButtonElement)) return;
    if (button.matches("[data-opi-drawer-open]")) {
      openSurface("drawer", button);
    } else if (button.matches("[data-opi-drawer-close]")) {
      closeSurface("drawer");
    } else if (button.matches("[data-opi-search-open]")) {
      openSurface("search", button);
    } else if (button.matches("[data-opi-search-close]")) {
      closeSurface("search");
    }
  });

  document.addEventListener(
    "click",
    (event) => {
      const target = event.target;
      if (!(target instanceof Element)) {
        return;
      }
      const link = target.closest(
        ".md-sidebar--primary a[href], .md-search-result__link[href]",
      );
      if (!(link instanceof HTMLAnchorElement)) {
        return;
      }
      if (
        event.defaultPrevented ||
        event.button !== 0 ||
        event.altKey ||
        event.ctrlKey ||
        event.metaKey ||
        event.shiftKey ||
        link.target === "_blank" ||
        link.hasAttribute("download")
      ) {
        return;
      }
      const destination = new URL(link.href, window.location.href);
      if (destination.origin !== window.location.origin) {
        return;
      }
      const current = new URL(window.location.href);
      if (
        destination.pathname === current.pathname &&
        destination.search === current.search
      ) {
        return;
      }
      pendingDestinationFocus = true;
      invokers.drawer = null;
      invokers.search = null;
      if (link.closest(".md-search")) {
        closeSurface("search", false);
      } else if (link.closest(".md-sidebar--primary")) {
        closeSurface("drawer", false);
      }
    },
    true,
  );
  document.addEventListener(
    "keydown",
    (event) => {
      if (handleSearchShortcut(event)) return;
      const modal = activeModal();
      if (!modal || !(modal.surface instanceof HTMLElement)) {
        return;
      }
      if (event.key === "Escape") {
        event.preventDefault();
        event.stopPropagation();
        closeSurface(modal.name);
        return;
      }
      if (event.key !== "Tab") {
        return;
      }

      // Own the complete modal Tab ring so Material cannot close search at the
      // window boundary and offscreen drawer links remain sequentially reachable.
      event.preventDefault();
      event.stopPropagation();
      const focusable = focusableElements(modal.surface);
      if (!focusable.length) {
        return;
      }
      const activeIndex = focusable.indexOf(document.activeElement);
      const offset = event.shiftKey ? -1 : 1;
      const nextIndex =
        activeIndex < 0
          ? event.shiftKey
            ? focusable.length - 1
            : 0
          : (activeIndex + offset + focusable.length) % focusable.length;
      focusable[nextIndex].focus();
    },
    true,
  );

  document.addEventListener(
    "focusout",
    (event) => {
      if (event.target === viewportFocus && isVisible(event.target)) {
        viewportFocus = null;
      }
    },
    true,
  );

  document.addEventListener(
    "focusin",
    (event) => {
      if (event.target instanceof HTMLElement && event.target !== document.body) {
        viewportFocus = event.target;
      }
      const modal = activeModal();
      if (
        !modal ||
        !(modal.surface instanceof HTMLElement) ||
        modal.surface.contains(event.target)
      ) {
        return;
      }
      focusableElements(modal.surface)[0]?.focus();
    },
    true,
  );
  Object.entries(panels).forEach(([name, panel]) => {
    if (panel.toggle instanceof HTMLInputElement) {
      panel.toggle.addEventListener("change", () => {
        syncPanel(name);
        if (panel.toggle.checked) {
          return;
        }
        if (pendingDestinationFocus) {
          invokers[name] = null;
        } else {
          restoreInvoker(name);
        }
      });
    }
  });

  const handleViewportChange = () => {
    const revision = ++viewportRevision;
    const active = document.activeElement;
    const focusReference =
      active instanceof HTMLElement && active !== document.body
        ? active
        : viewportFocus;
    const focusWasInDrawer = getDrawer()?.contains(focusReference) === true;
    const focusWasInSearch = getSearch()?.contains(focusReference) === true;
    const drawerContext =
      drawerToggle.checked ||
      focusWasInDrawer ||
      focusReference === getControl("drawer");
    const searchContext =
      focusWasInSearch ||
      focusReference === getControl("search");
    const focusTarget = drawerContext
      ? drawerMedia.matches
        ? getControl("drawer")
        : getBrand()
      : searchContext
        ? searchMedia.matches
          ? getControl("search")
          : getSearch()?.querySelector(".md-search__input")
        : null;
    if (!drawerMedia.matches && drawerToggle.checked) {
      closeSurface("drawer", false);
    }
    syncPanels();
    window.cancelAnimationFrame(viewportFocusFrame);
    viewportFocusFrame = window.requestAnimationFrame(() => {
      viewportFocusFrame = window.requestAnimationFrame(() => {
        viewportFocusFrame = 0;
        if (revision !== viewportRevision) return;
        if (
          active instanceof HTMLElement &&
          active !== document.body &&
          isVisible(active)
        ) {
          return;
        }
        const current = document.activeElement;
        if (
          current instanceof HTMLElement &&
          current !== document.body &&
          isVisible(current)
        ) {
          return;
        }
        if (isVisible(focusTarget)) focusTarget.focus();
      });
    });
  };

  window.addEventListener("resize", () => {
    const active = document.activeElement;
    viewportFocus =
      active instanceof HTMLElement && active !== document.body
        ? active
        : viewportFocus;
  });
  drawerMedia.addEventListener("change", handleViewportChange);
  searchMedia.addEventListener("change", handleViewportChange);

  if (!prepareSurfaces()) {
    return;
  }
  syncPanels();
  document.documentElement.classList.add("opi-header-controls-ready");

  if (window.document$?.subscribe) {
    window.document$.subscribe(() => {
      if (!prepareSurfaces()) {
        document.documentElement.classList.remove(
          "opi-header-controls-ready",
        );
        return;
      }
      syncPanels();
      if (pendingDestinationFocus) {
        window.requestAnimationFrame(() => {
          focusDestination();
          pendingDestinationFocus = false;
        });
      }
      document.documentElement.classList.add("opi-header-controls-ready");
    });
  }
})();
