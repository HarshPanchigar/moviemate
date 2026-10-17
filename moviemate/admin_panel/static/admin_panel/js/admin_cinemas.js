/**
 * MovieMate Admin - Cinema Halls Management Scripts
 */

function openViewFullCinemaModal(name, city, address, screens, facilities, shows, bookings, activeMovies) {
    const nameEl = document.getElementById('vfcName');
    if (nameEl) nameEl.innerText = name;

    const cityEl = document.getElementById('vfcCity');
    if (cityEl) cityEl.innerText = city;

    const addrEl = document.getElementById('vfcAddress');
    if (addrEl) addrEl.innerText = address;

    const scrEl = document.getElementById('vfcScreens');
    if (scrEl) scrEl.innerText = screens + ' Screens';

    const showEl = document.getElementById('vfcShows');
    if (showEl) showEl.innerText = shows + ' Shows';

    const bookEl = document.getElementById('vfcBookings');
    if (bookEl) bookEl.innerText = bookings + ' Tickets';

    const facEl = document.getElementById('vfcFacilities');
    if (facEl) facEl.innerText = facilities || '4K Dolby Atmos, Recliners, Food Court';

    const moviesContainer = document.getElementById('vfcMoviesList');
    if (moviesContainer) {
        if (activeMovies && activeMovies.length > 0) {
            moviesContainer.innerHTML = activeMovies.map(m => `
                <span class="cinema-movie-chip">${m}</span>
            `).join('');
        } else {
            moviesContainer.innerHTML = '<span style="color: var(--text-muted); font-size: 12px;">No movies currently scheduled.</span>';
        }
    }

    const modal = document.getElementById('viewFullCinemaModal');
    if (modal) modal.style.display = 'flex';
}

function editCinema(id, name, city, address, screens) {
    const form = document.getElementById('editCinemaForm');
    if (form) form.action = `/admin-panel/cinemas/edit/${id}/`;

    const nameEl = document.getElementById('editName');
    if (nameEl) nameEl.value = name;

    const cityEl = document.getElementById('editCity');
    if (cityEl) cityEl.value = city;

    const addrEl = document.getElementById('editAddress');
    if (addrEl) addrEl.value = address;

    const scrEl = document.getElementById('editScreens');
    if (scrEl) scrEl.value = screens;

    const modal = document.getElementById('editCinemaModal');
    if (modal) modal.style.display = 'flex';
}

function filterCinemasTable() {
    const input = document.getElementById('cinemaSearchInput');
    const q = input ? input.value.toLowerCase().trim() : '';
    const rows = document.querySelectorAll('#cinemasTable tbody tr');

    rows.forEach(row => {
        const name = (row.getAttribute('data-name') || '').toLowerCase();
        const city = (row.getAttribute('data-city') || '').toLowerCase();

        row.style.display = (!q || name.includes(q) || city.includes(q)) ? '' : 'none';
    });
}
