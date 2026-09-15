<script>
(() => {
  const init = () => {
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

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init, { once: true });
  } else {
    init();
  }
})();
</script>
