// =========================================================
// MOVIEMATE MY BOOKINGS JS
// Horizontal Past Bookings Slider Navigation
// =========================================================

function slideHistory(offset) {
    const slider = document.getElementById('historySlider');
    if (slider) {
        slider.scrollBy({ left: offset, behavior: 'smooth' });
    }
}
