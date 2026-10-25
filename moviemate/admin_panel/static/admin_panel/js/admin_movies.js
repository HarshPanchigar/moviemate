/**
 * MovieMate Admin - Movie Management Scripts
 * Handles modal population, table search/filter, and OMDb API importing
 */

function formatDuration(minutes) {
    const total = parseInt(minutes, 10) || 0;
    const hours = Math.floor(total / 60);
    const mins = total % 60;
    if (hours > 0 && mins > 0) return `${hours}h ${mins}m`;
    if (hours > 0) return `${hours}h`;
    return `${mins}m`;
}

function openViewFullMovieModal(title, genre, duration, rating, year, tag, poster, backdrop, plot, shows, bookings) {
    const titleEl = document.getElementById('vfmTitle');
    if (titleEl) titleEl.innerText = title + ' (' + year + ')';

    const genreEl = document.getElementById('vfmGenre');
    if (genreEl) genreEl.innerText = genre;

    const durEl = document.getElementById('vfmDuration');
    if (durEl) durEl.innerText = formatDuration(duration);

    const rateEl = document.getElementById('vfmRating');
    if (rateEl) rateEl.innerText = rating;

    const tagEl = document.getElementById('vfmTag');
    if (tagEl) tagEl.innerText = tag.toUpperCase();

    const plotEl = document.getElementById('vfmPlot');
    if (plotEl) plotEl.innerText = plot || 'No synopsis provided.';

    const showsEl = document.getElementById('vfmShows');
    if (showsEl) showsEl.innerText = shows + ' Shows';

    const bookEl = document.getElementById('vfmBookings');
    if (bookEl) bookEl.innerText = bookings + ' Tickets';

    const posterEl = document.getElementById('vfmPoster');
    if (posterEl) posterEl.src = poster || 'https://images.unsplash.com/photo-1489599849927-2ee91cede3ba';

    const backdropEl = document.getElementById('vfmBackdrop');
    if (backdropEl) backdropEl.style.backgroundImage = `url('${backdrop || poster || ""}')`;

    const modal = document.getElementById('viewFullMovieModal');
    if (modal) modal.style.display = 'flex';
}

function openEditMovieModal(id, title, genre, duration, year, rating, tag, poster, backdrop, plot, status, isHero) {
    const form = document.getElementById('editMovieForm');
    if (form) form.action = `/admin-panel/movies/edit/${id}/`;

    const titleEl = document.getElementById('editTitle');
    if (titleEl) titleEl.value = title;

    const genreEl = document.getElementById('editGenre');
    if (genreEl) genreEl.value = genre;

    const durEl = document.getElementById('editDuration');
    if (durEl) durEl.value = duration;

    const yrEl = document.getElementById('editYear');
    if (yrEl) yrEl.value = year;

    const rateEl = document.getElementById('editRating');
    if (rateEl) rateEl.value = rating;

    const tagEl = document.getElementById('editDisplayTag');
    if (tagEl) tagEl.value = tag;

    const postEl = document.getElementById('editPoster');
    if (postEl) postEl.value = poster;

    const backEl = document.getElementById('editBackdrop');
    if (backEl) backEl.value = backdrop;

    const plotEl = document.getElementById('editPlot');
    if (plotEl) plotEl.value = plot;

    const isHeroEl = document.getElementById('editIsHero');
    if (isHeroEl) {
        isHeroEl.checked = (isHero === true || isHero === 'true' || isHero === 'True' || isHero === '1');
    }

    const modal = document.getElementById('editMovieModal');
    if (modal) modal.style.display = 'flex';
}

function filterMoviesTable() {
    const input = document.getElementById('movieSearchInput');
    const select = document.getElementById('movieTagFilter');
    const q = input ? input.value.toLowerCase().trim() : '';
    const filterVal = select ? select.value : '';
    const rows = document.querySelectorAll('#moviesTable tbody tr');

    rows.forEach(row => {
        const title = (row.getAttribute('data-title') || '').toLowerCase();
        const genre = (row.getAttribute('data-genre') || '').toLowerCase();
        const rowTag = row.getAttribute('data-tag') || '';
        const isHero = row.getAttribute('data-hero') === 'true';

        const matchesQuery = !q || title.includes(q) || genre.includes(q);
        let matchesFilter = true;
        if (filterVal === 'hero') {
            matchesFilter = isHero;
        } else if (filterVal) {
            matchesFilter = (rowTag === filterVal);
        }

        row.style.display = (matchesQuery && matchesFilter) ? '' : 'none';
    });
}

function searchOMDb() {
    const input = document.getElementById('omdbQuery');
    const container = document.getElementById('omdbResults');
    const btn = document.getElementById('omdbSearchBtn');
    if (!input || !container) return;

    const query = input.value.trim();
    if (!query) return;

    const searchUrl = btn ? btn.getAttribute('data-search-url') : '/admin-panel/api/omdb-search/';
    const importUrl = btn ? btn.getAttribute('data-import-url') : '/admin-panel/movies/import-omdb/';
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]') ? document.querySelector('[name=csrfmiddlewaretoken]').value : '';

    container.innerHTML = '<div style="text-align: center; color: var(--text-muted); padding: 25px;"><i class="fa-solid fa-spinner fa-spin" style="margin-right: 8px;"></i>Searching OMDb API...</div>';

    fetch(`${searchUrl}?q=${encodeURIComponent(query)}`)
        .then(res => res.json())
        .then(data => {
            if (data.movies && data.movies.length > 0) {
                container.innerHTML = data.movies.map(m => `
                    <div style="display: flex; justify-content: space-between; align-items: center; background: #f8fafc; border: 1px solid var(--border-color); padding: 12px 16px; border-radius: 10px; margin-bottom: 10px; gap: 14px;">
                        <div style="display: flex; align-items: center; gap: 12px; min-width: 0; flex: 1;">
                            <img src="${m.Poster !== 'N/A' ? m.Poster : 'https://images.unsplash.com/photo-1489599849927-2ee91cede3ba'}" style="width: 40px; height: 56px; object-fit: cover; border-radius: 6px; border: 1px solid var(--border-color); flex-shrink: 0;">
                            <div style="min-width: 0; flex: 1;">
                                <div style="font-weight: 700; font-size: 13.5px; color: var(--text-primary); line-height: 1.4; word-break: break-word;">${m.Title} <span style="font-size: 11.5px; color: var(--text-muted); font-weight: 600;">(${m.Year})</span></div>
                                <div style="font-size: 11px; color: var(--text-muted); margin-top: 3px; font-family: monospace;">${m.imdbID}</div>
                            </div>
                        </div>
                        <form action="${importUrl}" method="POST" style="display: flex; gap: 10px; align-items: center; flex-shrink: 0; margin: 0;">
                            <input type="hidden" name="csrfmiddlewaretoken" value="${csrfToken}">
                            <input type="hidden" name="imdb_id" value="${m.imdbID}">
                            <select name="display_tag" class="form-control" style="min-height: 36px; padding: 4px 10px; font-size: 12px; width: 125px; border-radius: 6px;">
                                <option value="trending" selected>Trending</option>
                                <option value="hot">Hot</option>
                                <option value="top_rated">Top Rated</option>
                                <option value="new_release">New Release</option>
                            </select>
                            <button type="submit" class="btn-blue" style="min-height: 36px; padding: 0 14px; font-size: 12.5px; white-space: nowrap; border-radius: 6px;">
                                <i class="fa-solid fa-cloud-arrow-down"></i> Import
                            </button>
                        </form>
                    </div>
                `).join('');
            } else {
                container.innerHTML = '<div style="text-align: center; color: var(--text-muted); padding: 25px;">No movies found on OMDb.</div>';
            }
        })
        .catch(err => {
            console.error('OMDb API error:', err);
            container.innerHTML = '<div style="text-align: center; color: #dc2626; padding: 25px;">Error searching OMDb API. Please check network connection.</div>';
        });
}

function toggleHeroAjax(e, el, movieId) {
    if (e) e.preventDefault();

    fetch(`/admin-panel/movies/toggle-hero/${movieId}/`, {
        headers: {
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
    .then(res => res.json())
    .then(data => {
        if (data.success) {
            const row = document.getElementById(`movie-row-${movieId}`);
            if (row) {
                row.setAttribute('data-hero', data.is_hero ? 'true' : 'false');
            }

            const badge = document.getElementById(`hero-badge-${movieId}`);
            if (badge) {
                if (data.is_hero) {
                    badge.className = 'hero-status-pill active';
                    badge.title = 'Featured in Hero Banner — Click to remove from Hero';
                    badge.innerHTML = '<i class="fa-solid fa-star" style="color: #f59e0b;"></i><span>Hero Active</span>';
                } else {
                    badge.className = 'hero-status-pill inactive';
                    badge.title = 'Not in Hero Banner — Click to set as Hero';
                    badge.innerHTML = '<i class="fa-regular fa-star"></i><span>Set Hero</span>';
                }
            }

            const actionBtn = document.getElementById(`hero-action-btn-${movieId}`);
            if (actionBtn) {
                if (data.is_hero) {
                    actionBtn.className = 'action-icon-btn hero-action-active';
                    actionBtn.title = 'Remove from Hero Banner';
                    actionBtn.innerHTML = '<i class="fa-solid fa-star"></i>';
                } else {
                    actionBtn.className = 'action-icon-btn';
                    actionBtn.title = 'Feature in Hero Banner';
                    actionBtn.innerHTML = '<i class="fa-regular fa-star"></i>';
                }
            }

            if (data.message && typeof showAdminToast === 'function') {
                showAdminToast(data.message, 'success');
            }
        } else {
            window.location.reload();
        }
    })
    .catch(err => {
        // Fallback to regular navigation
        window.location.href = el.href;
    });
}

// Enable Enter key search on OMDb input
document.addEventListener('DOMContentLoaded', () => {
    const omdbInput = document.getElementById('omdbQuery');
    if (omdbInput) {
        omdbInput.addEventListener('keydown', (e) => {
            if (e.key === 'Enter') {
                e.preventDefault();
                searchOMDb();
            }
        });
    }
});
