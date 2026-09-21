(() => {
  const app = document.querySelector('[data-flashcard-app]');
  if (!app) return;

  const source = '../../assets/data/flashcards-tema1.csv';
  const sectionRanges = [
    [1,19,'Representación'],
    [20,44,'Unidades funcionales'],
    [45,49,'Tipos de computadores'],
    [50,54,'Software'],
    [55,61,'Ejercicios'],
    [62,78,'Repaso']
  ];
  const extensions = new Set([63,64]);

  const parseCsv = (text) => {
    const rows=[]; let row=[], cell='', quoted=false;
    for (let i=0;i<text.length;i++) {
      const ch=text[i], next=text[i+1];
      if (quoted) {
        if (ch==='"' && next==='"') { cell+='"'; i++; }
        else if (ch==='"') quoted=false;
        else cell+=ch;
      } else {
        if (ch==='"') quoted=true;
        else if (ch===',') { row.push(cell); cell=''; }
        else if (ch==='\n') { row.push(cell.replace(/\r$/,'')); if(row.some(x=>x.trim())) rows.push(row); row=[]; cell=''; }
        else cell+=ch;
      }
    }
    if (cell.length || row.length) { row.push(cell); if(row.some(x=>x.trim())) rows.push(row); }
    return rows;
  };

  const pretty = (s='') => s
    .replace(/\$/g,'')
    .replace(/\\lceil/g,'⌈').replace(/\\rceil/g,'⌉')
    .replace(/\\log_\{2\}/g,'log₂')
    .replace(/\\ge/g,'≥').replace(/\\div/g,'÷').replace(/\\cdot/g,'·')
    .replace(/\\times/g,'×').replace(/\\mu/g,'μ')
    .replace(/\^\{([0-9]+)\}/g,'^$1')
    .replace(/_\{([0-9]+)\}/g,'_$1');

  const sectionFor = (id) => sectionRanges.find(([a,b])=>id>=a&&id<=b)?.[2] || 'Tema 1';

  const q = app.querySelector('[data-card-question]');
  const aBox = app.querySelector('[data-card-answer]');
  const aText = app.querySelector('[data-card-answer-text]');
  const progress = app.querySelector('[data-card-progress]');
  const bar = app.querySelector('[data-card-progress-bar]');
  const sectionLabel = app.querySelector('[data-card-section-label]');
  const kindLabel = app.querySelector('[data-card-kind]');
  const selector = app.querySelector('[data-card-section]');
  const reveal = app.querySelector('[data-card-reveal]');
  const prev = app.querySelector('[data-card-prev]');
  const next = app.querySelector('[data-card-next]');
  const shuffle = app.querySelector('[data-card-shuffle]');
  const status = app.querySelector('[data-card-status]');
  const cardEl = app.querySelector('[data-study-card]');

  let all=[], cards=[], index=0, answerVisible=false;

  const setAnswer = (visible) => {
    answerVisible=visible;
    aBox.hidden=!visible;
    reveal.textContent=visible ? 'Ocultar respuesta' : 'Mostrar respuesta';
  };

  const render = () => {
    if (!cards.length) {
      q.textContent='No hay tarjetas en este bloque.';
      aBox.hidden=true; progress.textContent='0 / 0'; bar.style.width='0%'; return;
    }
    const c=cards[index];
    q.textContent=pretty(c.q);
    aText.textContent=pretty(c.a);
    sectionLabel.textContent=c.section;
    kindLabel.textContent=c.kind;
    kindLabel.classList.toggle('is-extension',c.kind==='Ampliación');
    progress.textContent=`${index+1} / ${cards.length}`;
    bar.style.width=`${((index+1)/cards.length)*100}%`;
    setAnswer(false);
    status.textContent=`Tarjeta ${index+1} de ${cards.length}: ${c.q}`;
  };

  const move = (delta) => {
    if(!cards.length) return;
    index=(index+delta+cards.length)%cards.length;
    render();
  };

  selector.addEventListener('change',()=>{
    cards=selector.value==='all' ? [...all] : all.filter(c=>c.section===selector.value);
    index=0; render();
  });
  reveal.addEventListener('click',()=>setAnswer(!answerVisible));
  prev.addEventListener('click',()=>move(-1));
  next.addEventListener('click',()=>move(1));
  shuffle.addEventListener('click',()=>{
    if(cards.length<2) return;
    for(let i=cards.length-1;i>0;i--){const j=Math.floor(Math.random()*(i+1));[cards[i],cards[j]]=[cards[j],cards[i]];}
    index=0; render();
  });
  cardEl.addEventListener('click',(e)=>{if(!e.target.closest('button,select,a')) setAnswer(!answerVisible);});
  document.addEventListener('keydown',(e)=>{
    if(!app.contains(document.activeElement) && document.activeElement!==document.body) return;
    if(['SELECT','BUTTON','A','INPUT','TEXTAREA'].includes(document.activeElement?.tagName)) return;
    if(e.key==='ArrowLeft'){e.preventDefault();move(-1);}
    if(e.key==='ArrowRight'){e.preventDefault();move(1);}
    if(e.key===' '){e.preventDefault();setAnswer(!answerVisible);}
  });

  fetch(source)
    .then(r=>{if(!r.ok) throw new Error('No se pudo cargar el CSV'); return r.text();})
    .then(text=>{
      all=parseCsv(text).map((row,i)=>({
        id:i+1,
        q:(row[0]||'').trim(),
        a:(row.slice(1).join(',')||'').trim(),
        section:sectionFor(i+1),
        kind:extensions.has(i+1) ? 'Ampliación' : 'Tema 1'
      })).filter(c=>c.q&&c.a);
      cards=[...all];
      render();
    })
    .catch(()=>{
      q.textContent='No se han podido cargar las tarjetas.';
      status.textContent='Error al cargar el recurso de tarjetas.';
    });
})();