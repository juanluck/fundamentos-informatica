<script>
(() => {
  const initSolutions = () => {
    document.querySelectorAll('.ejercicio, .tarea').forEach((container) => {
      const solution = container.querySelector(':scope > .solucion');
      if (!solution || solution.dataset.enhanced === 'true') return;
      solution.dataset.enhanced = 'true';
      solution.dataset.collapsed = 'true';
      const button = document.createElement('button');
      button.type = 'button';
      button.className = 'solution-toggle';
      button.textContent = 'Mostrar solución';
      button.setAttribute('aria-expanded', 'false');
      const id = solution.id || `solution-${Math.random().toString(36).slice(2, 10)}`;
      solution.id = id;
      button.setAttribute('aria-controls', id);
      button.addEventListener('click', () => {
        const collapsed = solution.dataset.collapsed === 'true';
        solution.dataset.collapsed = collapsed ? 'false' : 'true';
        button.setAttribute('aria-expanded', String(collapsed));
        button.textContent = collapsed ? 'Ocultar solución' : 'Mostrar solución';
      });
      container.insertBefore(button, solution);
    });
  };

  const renderBitExplorer = (root) => {
    const slider = root.querySelector('input[type="range"]');
    const value = root.querySelector('[data-bit-value]');
    const count = root.querySelector('[data-combination-count]');
    const patterns = root.querySelector('[data-bit-patterns]');
    if (!slider || !value || !count || !patterns) return;
    const draw = () => {
      const bits = Number(slider.value);
      const total = 2 ** bits;
      value.textContent = String(bits);
      count.textContent = String(total);
      patterns.replaceChildren();
      for (let i = 0; i < total; i += 1) {
        const token = document.createElement('span');
        token.className = 'bit-pattern';
        token.textContent = i.toString(2).padStart(bits, '0');
        patterns.appendChild(token);
      }
    };
    slider.addEventListener('input', draw);
    draw();
  };

  const init = () => {
    initSolutions();
    document.querySelectorAll('[data-bit-explorer]').forEach(renderBitExplorer);
  };
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init, { once: true });
  } else {
    init();
  }
})();
</script>
