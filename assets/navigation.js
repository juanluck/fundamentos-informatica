(() => {
  const root = document.querySelector('[data-book-navigation]');
  if (!root) return;

  const marker = '/book/';
  const path = window.location.pathname;
  const markerIndex = path.indexOf(marker);
  const bookRoot = markerIndex >= 0 ? path.slice(0, markerIndex + marker.length) : '/fundamentos-informatica/book/';
  const relativePath = markerIndex >= 0 ? path.slice(markerIndex + marker.length) || 'index.html' : 'index.html';
  const urlFor = (rel = '') => `${bookRoot}${rel}`;

  const pages = {
    'index.html': { part: 'Inicio', roman: '•', location: 'Portada' },
    'teoria/tema1/01-que-es-computador.html': { part: 'Teoría', roman: 'I', location: 'Tema 1 · 1.1', panel: 'theory' },
    'teoria/tema1/02-representacion.html': { part: 'Teoría', roman: 'I', location: 'Tema 1 · 1.2', panel: 'theory' },
    'teoria/tema1/03-componentes.html': { part: 'Teoría', roman: 'I', location: 'Tema 1 · 1.3', panel: 'theory' },
    'teoria/tema1/04-comunicacion.html': { part: 'Teoría', roman: 'I', location: 'Tema 1 · 1.4', panel: 'theory' },
    'teoria/tema1/05-ejecucion.html': { part: 'Teoría', roman: 'I', location: 'Tema 1 · 1.5', panel: 'theory' },
    'teoria/tema1/06-tipos.html': { part: 'Teoría', roman: 'I', location: 'Tema 1 · 1.6', panel: 'theory' },
    'teoria/tema1/07-software.html': { part: 'Teoría', roman: 'I', location: 'Tema 1 · 1.7', panel: 'theory' },
    'teoria/tema1/ejercicios.html': { part: 'Teoría', roman: 'I', location: 'Tema 1 · Ejercicios', panel: 'theory' },
    'practicas/index.html': { part: 'Prácticas', roman: 'II', location: 'Portada de prácticas', panel: 'practice' }
  };

  const current = pages[relativePath] || { part: 'Libro', roman: '•', location: 'Fundamentos de Informática', panel: 'theory' };
  const drawer = root.querySelector('#book-drawer');
  const backdrop = root.querySelector('[data-nav-backdrop]');
  const openButtons = root.querySelectorAll('[data-nav-open], [data-nav-part-button]');
  const menuButton = root.querySelector('[data-nav-open]');
  const partButton = root.querySelector('[data-nav-part-button]');
  const closeButton = root.querySelector('[data-nav-close]');
  const tabs = [...root.querySelectorAll('[data-part-tab]')];
  const panels = [...root.querySelectorAll('[data-part-panel]')];
  let lastFocus = null;

  root.querySelectorAll('[data-book-home]').forEach((link) => { link.href = urlFor('index.html'); });
  root.querySelectorAll('[data-book-path]').forEach((link) => {
    const rel = link.getAttribute('data-book-path');
    link.href = urlFor(rel);
    if (rel === relativePath) {
      link.classList.add('is-current');
      link.setAttribute('aria-current', 'page');
      const theme = link.closest('details');
      if (theme) theme.open = true;
    }
  });

  const partText = root.querySelector('[data-nav-part]');
  const locationText = root.querySelector('[data-nav-location]');
  const partRoman = root.querySelector('[data-nav-part-roman]');
  const partButtonLabel = root.querySelector('[data-nav-part-button-label]');
  if (partText) partText.textContent = current.part;
  if (locationText) locationText.textContent = current.location;
  if (partRoman) partRoman.textContent = current.roman;
  if (partButtonLabel) partButtonLabel.textContent = current.part === 'Inicio' ? 'Explorar' : current.part;

  const activatePanel = (name) => {
    tabs.forEach((tab) => {
      const active = tab.dataset.partTab === name;
      tab.classList.toggle('is-active', active);
      tab.setAttribute('aria-selected', String(active));
    });
    panels.forEach((panel) => {
      const active = panel.dataset.partPanel === name;
      panel.classList.toggle('is-active', active);
      panel.hidden = !active;
    });
  };

  activatePanel(current.panel || 'theory');

  tabs.forEach((tab) => {
    tab.addEventListener('click', () => activatePanel(tab.dataset.partTab));
  });

  const setExpanded = (expanded) => {
    openButtons.forEach((button) => button.setAttribute('aria-expanded', String(expanded)));
  };

  const openDrawer = (preferredPanel) => {
    lastFocus = document.activeElement;
    if (preferredPanel) activatePanel(preferredPanel);
    drawer.classList.add('is-open');
    drawer.setAttribute('aria-hidden', 'false');
    if ('inert' in drawer) drawer.inert = false;
    backdrop.hidden = false;
    requestAnimationFrame(() => backdrop.classList.add('is-visible'));
    document.documentElement.classList.add('nav-open');
    setExpanded(true);
    closeButton.focus();
  };

  const closeDrawer = () => {
    drawer.classList.remove('is-open');
    drawer.setAttribute('aria-hidden', 'true');
    if ('inert' in drawer) drawer.inert = true;
    backdrop.classList.remove('is-visible');
    window.setTimeout(() => { backdrop.hidden = true; }, 180);
    document.documentElement.classList.remove('nav-open');
    setExpanded(false);
    if (lastFocus && typeof lastFocus.focus === 'function') lastFocus.focus();
  };

  if ('inert' in drawer) drawer.inert = true;
  menuButton.addEventListener('click', () => openDrawer(current.panel || 'theory'));
  partButton.addEventListener('click', () => openDrawer(current.panel || 'theory'));
  closeButton.addEventListener('click', closeDrawer);
  backdrop.addEventListener('click', closeDrawer);

  drawer.addEventListener('keydown', (event) => {
    if (event.key !== 'Tab') return;
    const focusable = [...drawer.querySelectorAll('a[href], button:not([disabled]), summary')].filter((el) => !el.closest('[hidden]'));
    if (!focusable.length) return;
    const first = focusable[0];
    const last = focusable[focusable.length - 1];
    if (event.shiftKey && document.activeElement === first) { event.preventDefault(); last.focus(); }
    else if (!event.shiftKey && document.activeElement === last) { event.preventDefault(); first.focus(); }
  });

  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape' && drawer.classList.contains('is-open')) closeDrawer();
  });
})();
