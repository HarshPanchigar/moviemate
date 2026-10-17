// =========================================================
// MOVIEMATE SELECT THEATER JS
// Horizontal Date Strip Navigation
// =========================================================

function scrollDates(offset) {
    const track = document.getElementById("dateScrollTrack");
    if (!track) return;
    track.scrollBy({
        left: offset,
        behavior: "smooth"
    });
}

function togglePlotExpand() {
    const textEl = document.getElementById("moviePlotText");
    const btn = document.getElementById("plotToggleBtn");
    const label = document.getElementById("plotToggleText");
    const icon = document.getElementById("plotToggleIcon");
    if (!textEl || !btn) return;

    const isClamped = textEl.classList.contains("clamped");
    if (isClamped) {
        textEl.classList.remove("clamped");
        btn.setAttribute("aria-expanded", "true");
        if (label) label.textContent = "Show less";
        if (icon) {
            icon.classList.remove("fa-chevron-down");
            icon.classList.add("fa-chevron-up");
        }
    } else {
        textEl.classList.add("clamped");
        btn.setAttribute("aria-expanded", "false");
        if (label) label.textContent = "Read synopsis";
        if (icon) {
            icon.classList.remove("fa-chevron-up");
            icon.classList.add("fa-chevron-down");
        }
    }
}
