/**
 * MovieMate Admin - Show Allocations Scripts
 */

function openViewFullAllocModal(movie, cinema, city, startDate, endDate, totalDays, totalShows, plat, gold, silv, bookings, revenue, poster) {
    const movieEl = document.getElementById('vfaMovieTitle');
    if (movieEl) movieEl.innerText = movie;

    const cinemaEl = document.getElementById('vfaCinemaName');
    if (cinemaEl) cinemaEl.innerText = cinema + ' (' + city + ')';

    const datesEl = document.getElementById('vfaDates');
    if (datesEl) datesEl.innerText = 'Active: ' + startDate + ' — ' + endDate + ' (' + totalDays + ' Days)';

    const showsEl = document.getElementById('vfaTotalShows');
    if (showsEl) showsEl.innerText = totalShows;

    const bookEl = document.getElementById('vfaBookings');
    if (bookEl) bookEl.innerText = bookings;

    const revEl = document.getElementById('vfaRevenue');
    if (revEl) revEl.innerText = '₹' + revenue;

    const platEl = document.getElementById('vfaPlat');
    if (platEl) platEl.innerText = '₹' + plat;

    const goldEl = document.getElementById('vfaGold');
    if (goldEl) goldEl.innerText = '₹' + gold;

    const silvEl = document.getElementById('vfaSilv');
    if (silvEl) silvEl.innerText = '₹' + silv;

    const posterEl = document.getElementById('vfaPoster');
    if (posterEl) posterEl.src = poster || 'https://images.unsplash.com/photo-1489599849927-2ee91cede3ba';

    const modal = document.getElementById('viewFullAllocModal');
    if (modal) modal.style.display = 'flex';
}

function openEditAllocModal(movieId, cinemaId, movieTitle, cinemaName, startDate, endDate, rawTimesStr, plat, gold, silv) {
    const form = document.getElementById('editAllocForm');
    if (form) form.action = `/admin-panel/allocations/edit-group/${movieId}/${cinemaId}/`;

    const subEl = document.getElementById('editAllocSubtitle');
    if (subEl) subEl.innerText = `${movieTitle} at ${cinemaName}`;

    const sDateEl = document.getElementById('editStartDate');
    if (sDateEl) sDateEl.value = startDate;

    const eDateEl = document.getElementById('editEndDate');
    if (eDateEl) eDateEl.value = endDate;

    const platEl = document.getElementById('editPlat');
    if (platEl) platEl.value = plat;

    const goldEl = document.getElementById('editGold');
    if (goldEl) goldEl.value = gold;

    const silvEl = document.getElementById('editSilv');
    if (silvEl) silvEl.value = silv;

    const timesArray = rawTimesStr ? rawTimesStr.split(',') : ['10:00', '14:30', '18:00', '21:30'];
    const t1 = document.getElementById('editTime1');
    if (t1) t1.value = timesArray[0] || '10:00';

    const t2 = document.getElementById('editTime2');
    if (t2) t2.value = timesArray[1] || '';

    const t3 = document.getElementById('editTime3');
    if (t3) t3.value = timesArray[2] || '';

    const t4 = document.getElementById('editTime4');
    if (t4) t4.value = timesArray[3] || '';

    const modal = document.getElementById('editAllocModal');
    if (modal) modal.style.display = 'flex';
}

function filterAllocations() {
    const input = document.getElementById('allocSearchInput');
    const select = document.getElementById('allocCinemaFilter');
    const q = input ? input.value.toLowerCase().trim() : '';
    const cinemaFilter = select ? select.value : '';
    const cards = document.querySelectorAll('.allocation-card');

    cards.forEach(card => {
        const movie = (card.getAttribute('data-movie') || '').toLowerCase();
        const cinema = card.getAttribute('data-cinema') || '';
        const city = (card.getAttribute('data-city') || '').toLowerCase();

        const matchesSearch = !q || movie.includes(q) || cinema.toLowerCase().includes(q) || city.includes(q);
        const matchesCinema = !cinemaFilter || cinema === cinemaFilter;

        card.style.display = (matchesSearch && matchesCinema) ? 'grid' : 'none';
    });
}
