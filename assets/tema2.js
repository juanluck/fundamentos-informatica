// Keep Markdown tables semantic and horizontally scrollable on small screens.
(() => {
  document.querySelectorAll('.tema2-sheet table').forEach((table) => {
    const wrapper = document.createElement('div');
    wrapper.className = 'table-scroll';
    wrapper.tabIndex = 0;
    wrapper.setAttribute('role', 'region');
    wrapper.setAttribute('aria-label', 'Tabla; desplaza horizontalmente si no cabe completa');
    table.parentNode.insertBefore(wrapper, table);
    wrapper.appendChild(table);
  });
})();
