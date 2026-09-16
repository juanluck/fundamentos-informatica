(() => {
  const range = document.querySelector('#bitsRange');
  const value = document.querySelector('#bitsValue');
  const count = document.querySelector('#patternCount');
  const field = document.querySelector('#patternField');

  function renderPatterns() {
    const bits = Number(range.value);
    const total = 2 ** bits;
    value.value = bits;
    value.textContent = bits;
    count.textContent = total;
    field.replaceChildren();

    for (let i = 0; i < total; i += 1) {
      const token = document.createElement('span');
      token.className = 'pattern-token';
      token.textContent = i.toString(2).padStart(bits, '0');
      field.appendChild(token);
    }
  }

  range.addEventListener('input', renderPatterns);
  renderPatterns();

  const toggle = document.querySelector('.solution-toggle');
  const solution = document.querySelector('#solution');
  toggle.addEventListener('click', () => {
    const isOpen = toggle.getAttribute('aria-expanded') === 'true';
    toggle.setAttribute('aria-expanded', String(!isOpen));
    toggle.textContent = isOpen ? 'Ver solución' : 'Ocultar solución';
    solution.hidden = isOpen;
  });
})();
