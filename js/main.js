(() => {
  'use strict';
  document.documentElement.classList.replace('no-js', 'js');
  const toggle = document.querySelector('.nav-toggle');
  const nav = document.querySelector('#nav-links');
  const closeMenu = (restoreFocus = false) => {
    if (!toggle || !nav) return;
    toggle.setAttribute('aria-expanded', 'false');
    toggle.innerHTML = 'Menu <span aria-hidden="true">+</span>';
    nav.classList.remove('is-open');
    if (restoreFocus) toggle.focus();
  };
  toggle?.addEventListener('click', () => {
    const opening = toggle.getAttribute('aria-expanded') !== 'true';
    toggle.setAttribute('aria-expanded', String(opening));
    toggle.innerHTML = opening ? 'Close <span aria-hidden="true">−</span>' : 'Menu <span aria-hidden="true">+</span>';
    nav.classList.toggle('is-open', opening);
  });
  nav?.addEventListener('click', event => {
    const link = event.target.closest('a');
    if (!link) return;
    closeMenu();
    if (link.hash && link.pathname === location.pathname) {
      const target = document.getElementById(link.hash.slice(1));
      if (target) { target.setAttribute('tabindex', '-1'); target.focus({ preventScroll: true }); }
    }
  });
  document.addEventListener('keydown', event => {
    if (event.key === 'Escape' && toggle?.getAttribute('aria-expanded') === 'true') closeMenu(true);
  });
  document.addEventListener('click', event => {
    if (!event.target.closest('.site-header')) closeMenu();
  });
  const desktop = matchMedia('(min-width: 1051px)');
  desktop.addEventListener('change', event => { if (event.matches) closeMenu(); });

  const tabs = [...document.querySelectorAll('.feature-tab')];
  const panels = [...document.querySelectorAll('.feature-panel')];
  const activateTab = (tab, focus = false) => {
    tabs.forEach(item => {
      const selected = item === tab;
      item.setAttribute('aria-selected', String(selected));
      item.tabIndex = selected ? 0 : -1;
    });
    panels.forEach(panel => { panel.hidden = panel.id !== tab.getAttribute('aria-controls'); });
    if (focus) tab.focus();
  };
  if (tabs.length) {
    document.querySelector('.feature-nav').setAttribute('role', 'tablist');
    tabs.forEach((tab, index) => {
      tab.setAttribute('role', 'tab');
      tab.addEventListener('click', () => activateTab(tab));
      tab.addEventListener('keydown', event => {
        let next;
        if (event.key === 'ArrowRight') next = (index + 1) % tabs.length;
        if (event.key === 'ArrowLeft') next = (index - 1 + tabs.length) % tabs.length;
        if (event.key === 'Home') next = 0;
        if (event.key === 'End') next = tabs.length - 1;
        if (next !== undefined) { event.preventDefault(); activateTab(tabs[next], true); }
      });
    });
    panels.forEach(panel => {
      panel.setAttribute('role', 'tabpanel');
      panel.tabIndex = 0;
    });
    activateTab(tabs[0]);
  }
  document.querySelectorAll('img[data-product-image]').forEach(img => {
    const failed = () => {
      if (img.parentElement.querySelector('.image-error')) return;
      const message = document.createElement('p');
      message.className = 'image-error';
      message.setAttribute('role', 'status');
      message.append('This product image could not load. ');
      const link = document.createElement('a');
      link.href = img.src;
      link.textContent = 'Open image';
      message.append(link);
      img.hidden = true;
      img.parentElement.style.aspectRatio = 'auto';
      img.parentElement.append(message);
    };
    img.addEventListener('error', failed);
    if (img.complete && img.naturalWidth === 0) failed();
  });
})();
