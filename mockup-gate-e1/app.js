(() => {
  const range = document.querySelector('#bit-range');
  const bitCount = document.querySelector('#bit-count');
  const grid = document.querySelector('#combination-grid');
  const total = document.querySelector('#combination-total');
  const exponent = document.querySelector('#combination-exponent');

  if (!range || !bitCount || !grid || !total || !exponent) return;

  const render = () => {
    const n = Number(range.value);
    const count = 2 ** n;
    const min = Number(range.min);
    const max = Number(range.max);
    const pct = ((n - min) / (max - min)) * 100;

    bitCount.textContent = String(n);
    total.textContent = String(count);
    exponent.textContent = String(n);
    range.style.setProperty('--slider-pct', `${pct}%`);
    range.setAttribute('aria-valuetext', `${n} ${n === 1 ? 'bit' : 'bits'}, ${count} combinaciones`);

    grid.replaceChildren();
    grid.style.gridTemplateColumns = `repeat(${Math.min(4, count)}, 1fr)`;

    const fragment = document.createDocumentFragment();
    for (let i = 0; i < count; i += 1) {
      const cell = document.createElement('b');
      cell.textContent = i.toString(2).padStart(n, '0');
      fragment.appendChild(cell);
    }
    grid.appendChild(fragment);
    grid.setAttribute('aria-label', `${count} combinaciones de ${n} ${n === 1 ? 'bit' : 'bits'}`);
  };

  range.addEventListener('input', render);
  render();
})();
