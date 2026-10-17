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

// Global keyboard & backdrop event listeners
document.addEventListener('DOMContentLoaded', () => {
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
