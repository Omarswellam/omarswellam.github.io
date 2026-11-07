// mobile menu
const menuBtn = document.querySelector('.menu-btn');
const links = document.querySelector('.links');
menuBtn.addEventListener('click', () => {
  const open = links.classList.toggle('open');
  menuBtn.setAttribute('aria-expanded', open);
});
links.querySelectorAll('a').forEach(a => a.addEventListener('click', () => links.classList.remove('open')));

// project filters
document.querySelectorAll('.chip').forEach(chip => chip.addEventListener('click', () => {
  document.querySelectorAll('.chip').forEach(c => c.classList.toggle('on', c === chip));
  const f = chip.dataset.f;
  document.querySelectorAll('.card').forEach(card => {
    card.hidden = f !== 'all' && card.dataset.cat !== f;
  });
}));

// before / after slider
document.querySelectorAll('.compare').forEach(cmp => {
  const range = cmp.querySelector('input');
  const top = cmp.querySelector('.compare-top');
  const handle = document.createElement('span');
  handle.className = 'handle';
  handle.textContent = '↔';
  cmp.appendChild(handle);
  const set = () => {
    cmp.style.setProperty('--pos', range.value + '%');
    top.style.clipPath = `inset(0 0 0 ${range.value}%)`;
  };
  range.addEventListener('input', set);
  set();
});

// lightbox for project images
const box = document.querySelector('.lightbox');
const boxImg = box.querySelector('img');
document.querySelectorAll('.card-media > img, .thumbs img').forEach(img => {
  img.addEventListener('click', () => {
    boxImg.src = img.src;
    boxImg.alt = img.alt;
    box.hidden = false;
  });
});
box.addEventListener('click', e => { if (e.target !== boxImg) box.hidden = true; });
document.addEventListener('keydown', e => { if (e.key === 'Escape') box.hidden = true; });

// hide optional images that are missing
document.querySelectorAll('img[data-optional]').forEach(img => {
  img.addEventListener('error', () => img.closest('.card-media').remove());
});
