// =========================================================
// MOVIEMATE DASHBOARD JS
// Hero Carousel & Movie Filter Chips & Interactive FAQs
// =========================================================

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

function filterGenre(category, btn) {
    document.querySelectorAll('.filters .chip').forEach(c => c.classList.remove('active'));
    if (btn) btn.classList.add('active');

    const cards = document.querySelectorAll('#allMoviesGrid .stub');
    const cat = (category || 'all').toLowerCase();

    cards.forEach(card => {
        const genre = (card.getAttribute('data-genre') || '').toLowerCase();
        const tag = (card.getAttribute('data-tag') || '').toLowerCase();

        if (cat === 'all' || genre.includes(cat) || tag === cat) {
            card.style.display = 'flex';
        } else {
            card.style.display = 'none';
        }
    });
}

function toggleFaq(btn) {
    const item = btn.parentElement;
    const isActive = item.classList.contains('active');
    document.querySelectorAll('.faq-item').forEach(i => i.classList.remove('active'));
    if (!isActive) {
        item.classList.add('active');
    }
}

document.addEventListener('DOMContentLoaded', () => {
    heroSlides = document.querySelectorAll('.hero-slide');
    heroDots = document.querySelectorAll('.hero-dot');

    if (heroSlides.length) {
        heroRestart();
    }
});
