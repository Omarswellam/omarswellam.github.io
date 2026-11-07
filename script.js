// nav: border on scroll, mobile menu
const nav = document.querySelector('.nav');
const onScroll = () => nav.classList.toggle('scrolled', window.scrollY > 8);
window.addEventListener('scroll', onScroll, { passive: true });
onScroll();
const menuBtn = document.querySelector('.menu-btn');
const links = document.querySelector('.links');
if (menuBtn) {
  menuBtn.addEventListener('click', () => {
    const open = links.classList.toggle('open');
    menuBtn.setAttribute('aria-expanded', open);
  });
  links.querySelectorAll('a').forEach(a => a.addEventListener('click', () => links.classList.remove('open')));
}

// project filters
document.querySelectorAll('.chip').forEach(chip => chip.addEventListener('click', () => {
  document.querySelectorAll('.chip').forEach(c => c.classList.toggle('on', c === chip));
  const f = chip.dataset.f;
  document.querySelectorAll('.tile').forEach(t => { t.hidden = f !== 'all' && t.dataset.cat !== f; });
}));

// before / after sliders
document.querySelectorAll('.compare').forEach(cmp => {
  const range = cmp.querySelector('input');
  const top = cmp.querySelector('.compare-top');
  for (const cls of ['bar', 'handle']) {
    const el = document.createElement('span');
    el.className = cls;
    if (cls === 'handle') el.textContent = '↔';
    cmp.appendChild(el);
  }
  const set = () => {
    cmp.style.setProperty('--pos', range.value + '%');
    top.style.clipPath = `inset(0 0 0 ${range.value}%)`;
  };
  range.addEventListener('input', set);
  set();
});

// lightbox for figures
const box = document.querySelector('.lightbox');
if (box) {
  const boxImg = box.querySelector('img');
  document.querySelectorAll('figure img').forEach(img => img.addEventListener('click', () => {
    boxImg.src = img.src; boxImg.alt = img.alt; box.hidden = false;
  }));
  box.addEventListener('click', e => { if (e.target !== boxImg) box.hidden = true; });
  document.addEventListener('keydown', e => { if (e.key === 'Escape') box.hidden = true; });
}

// fade sections in as they scroll into view
const io = 'IntersectionObserver' in window && new IntersectionObserver(entries => {
  entries.forEach(e => { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } });
}, { rootMargin: '0px 0px -8% 0px' });
document.querySelectorAll('.reveal').forEach(el => io ? io.observe(el) : el.classList.add('in'));
