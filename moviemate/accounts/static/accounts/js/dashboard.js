// ---------- HERO SLIDER & FILTERS ----------
let heroIndex = 0;
let heroSlides = [];
let heroDots = [];
let heroTimer = null;

function heroRender() {
  heroSlides.forEach((s, i) => s.classList.toggle('active', i === heroIndex));
  heroDots.forEach((d, i) => d.classList.toggle('active', i === heroIndex));
}

function heroGoto(i) {
  heroIndex = i;
  heroRender();
  heroRestart();
}

function heroNav(dir) {
  if (!heroSlides.length) return;
  heroIndex = (heroIndex + dir + heroSlides.length) % heroSlides.length;
  heroRender();
  heroRestart();
}

function heroRestart() {
  clearInterval(heroTimer);
  heroTimer = setInterval(() => heroNav(1), 6000);
}

document.addEventListener('DOMContentLoaded', () => {
  heroSlides = document.querySelectorAll('.hero-slide');
  heroDots = document.querySelectorAll('.hero-dot');

  if (heroSlides.length) {
    heroRestart();
  }

  document.querySelectorAll('.filters .chip').forEach(chip => {
    chip.addEventListener('click', () => {
      document.querySelectorAll('.filters .chip').forEach(c => c.classList.remove('active'));
      chip.classList.add('active');
    });
  });
});
