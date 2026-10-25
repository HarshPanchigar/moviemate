// =========================================================
// MOVIEMATE CLIENT BASE JS
// Global Search Popup & Navigation Interactions
// =========================================================

let popupSearchTimer = null;

function openSearchModalPopup() {
    const modal = document.getElementById('searchModalPopup');
    const input = document.getElementById('popupSearchInput');
    if (modal) {
        modal.style.display = 'flex';
        setTimeout(() => input && input.focus(), 100);
    }
}

function closeSearchPopup() {
    const modal = document.getElementById('searchModalPopup');
    if (modal) {
        modal.style.display = 'none';
    }
}

function handlePopupSearch(e) {
    const input = document.getElementById('popupSearchInput');
    const resultsContainer = document.getElementById('popupSearchResults');
    if (!input || !resultsContainer) return;

    const query = input.value.trim();
    if (!query) {
        resultsContainer.innerHTML = '<div style="text-align: center; color: var(--text-muted); padding: 48px 20px; font-size: 14px;"><i class="fa-solid fa-film" style="display: block; font-size: 32px; margin-bottom: 12px; color: #cbd5e1;"></i>Type any movie title or genre above to explore available shows in Ahmedabad...</div>';
        return;
    }

    clearTimeout(popupSearchTimer);
    popupSearchTimer = setTimeout(() => {
        fetch(`/search-api/?q=${encodeURIComponent(query)}`)
            .then(res => res.json())
            .then(data => {
                if (data.movies && data.movies.length > 0) {
                    resultsContainer.innerHTML = `
                        <div class="popup-movies-grid">
                            ${data.movies.map(m => `
                                <div class="popup-movie-card">
                                    <div class="popup-card-poster">
                                        <img src="${m.poster_url}" alt="${m.title}">
                                        <span class="popup-card-rating"><i class="fa-solid fa-star" style="font-size: 11px;"></i> ${m.rating}</span>
                                    </div>
                                    <div class="popup-movie-info">
                                        <div class="popup-movie-title">${m.title}</div>
                                        <div class="popup-movie-meta">${m.genre}</div>
                                        <a href="/movie/${m.id}/theaters/" class="btn btn-emerald btn-block" style="margin-top: 10px; font-size: 13px; padding: 9px; border-radius: 8px;">Book Tickets</a>
                                    </div>
                                </div>
                            `).join('')}
                        </div>
                    `;
                } else {
                    resultsContainer.innerHTML = `<div style="text-align: center; color: var(--text-muted); padding: 50px 20px; font-size: 15px;">No movies found matching "<b style="color: var(--text-primary);">${query}</b>"</div>`;
                }
            })
            .catch(() => {
                resultsContainer.innerHTML = '<div style="text-align: center; color: var(--text-muted); padding: 40px 20px; font-size: 14px;">Error fetching search results.</div>';
            });
    }, 150);
}

// Theme Management (Apple Dark Mode & Light Mode)
function updateThemeToggleState(theme) {
    const toggleBtn = document.getElementById('themeToggleBtn');
    if (!toggleBtn) return;
    const isDark = theme === 'dark';
    toggleBtn.setAttribute('title', isDark ? 'Switch to Light mode' : 'Switch to Dark mode (Apple Black)');
    toggleBtn.setAttribute('aria-label', isDark ? 'Switch to Light mode' : 'Switch to Dark mode');
    toggleBtn.setAttribute('aria-checked', isDark ? 'true' : 'false');
}

function syncThemeState() {
    try {
        const savedTheme = localStorage.getItem('moviemate-theme');
        const prefersDark = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
        const targetTheme = (savedTheme === 'dark' || (!savedTheme && prefersDark)) ? 'dark' : 'light';

        if (document.documentElement.getAttribute('data-theme') !== targetTheme) {
            document.documentElement.setAttribute('data-theme', targetTheme);
        }
        updateThemeToggleState(targetTheme);
    } catch (err) {
        console.warn('Unable to sync theme from storage', err);
    }
}

function initThemeToggle() {
    const toggleBtn = document.getElementById('themeToggleBtn');
    if (!toggleBtn) return;

    syncThemeState();

    if (!toggleBtn.dataset.themeBound) {
        toggleBtn.dataset.themeBound = 'true';
        toggleBtn.addEventListener('click', () => {
            const activeTheme = document.documentElement.getAttribute('data-theme') || 'light';
            const nextTheme = activeTheme === 'dark' ? 'light' : 'dark';

            document.documentElement.classList.add('theme-transition');
            document.documentElement.setAttribute('data-theme', nextTheme);

            try {
                localStorage.setItem('moviemate-theme', nextTheme);
            } catch (err) {
                console.warn('Unable to persist theme in localStorage', err);
            }

            updateThemeToggleState(nextTheme);

            setTimeout(() => {
                document.documentElement.classList.remove('theme-transition');
            }, 300);
        });
    }

    // Listen to OS preference changes if no manual override is saved
    if (window.matchMedia && !window._moviematePrefersThemeBound) {
        window._moviematePrefersThemeBound = true;
        window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
            if (!localStorage.getItem('moviemate-theme')) {
                const autoTheme = e.matches ? 'dark' : 'light';
                document.documentElement.setAttribute('data-theme', autoTheme);
                updateThemeToggleState(autoTheme);
            }
        });
    }
}

// Sync theme on pageshow (e.g. Back/Forward cache navigation) and across tabs via storage event
window.addEventListener('pageshow', () => {
    syncThemeState();
});

window.addEventListener('storage', (e) => {
    if (e.key === 'moviemate-theme') {
        syncThemeState();
    }
});

// Global keyboard & backdrop event listeners
document.addEventListener('DOMContentLoaded', () => {
    initThemeToggle();

    // Close search modal on Escape key press
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
            closeSearchPopup();
        }
    });

    // Close search modal when clicking outside backdrop
    document.addEventListener('click', (e) => {
        const modal = document.getElementById('searchModalPopup');
        if (e.target === modal) {
            closeSearchPopup();
        }
    });
});

