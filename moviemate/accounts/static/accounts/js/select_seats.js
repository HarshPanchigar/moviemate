// =========================================================
// MOVIEMATE SELECT SEATS JS
// Seating Matrix Selection, Live Dynamic Price Calculation
// & Real-Time Concurrency Seat Guard Polling
// =========================================================

let selectedSeatObjects = []; // Array of { code: 'C3', tier: 'gold' }
let currentTier = 'gold';
let seatPrices = {
    platinum: 350,
    gold: 250,
    silver: 180
};

function initSeatPrices() {
    const form = document.getElementById('bookingForm');
    if (form) {
        seatPrices.platinum = parseFloat(form.dataset.platinumPrice || '350') || 350;
        seatPrices.gold = parseFloat(form.dataset.goldPrice || '250') || 250;
        seatPrices.silver = parseFloat(form.dataset.silverPrice || '180') || 180;
    }
}

function setTier(tier) {
    currentTier = tier;
    const input = document.getElementById('selectedTierInput');
    const label = document.getElementById('selectedTierLabel');
    if (input) input.value = tier;
    if (label) label.innerText = tier.toUpperCase();
}

function toggleSeat(btn, seatCode, seatTier) {
    if (btn.classList.contains('booked') || btn.disabled) {
        showToast(`Seat ${seatCode} is already booked or reserved by another customer.`, 'warning');
        return;
    }

    const existingIndex = selectedSeatObjects.findIndex(s => s.code === seatCode);

    if (existingIndex > -1) {
        selectedSeatObjects.splice(existingIndex, 1);
        btn.classList.remove('selected');
    } else {
        selectedSeatObjects.push({ code: seatCode, tier: seatTier });
        btn.classList.add('selected');

        setTier(seatTier);
        const radio = document.querySelector(`input[name="seat_tier_radio"][value="${seatTier}"]`);
        if (radio) radio.checked = true;
    }

    updateSummary();
}

function updateSummary() {
    const seatsLabel = document.getElementById('selectedSeatsLabel');
    const priceLabel = document.getElementById('totalPriceLabel');
    const proceedBtn = document.getElementById('proceedBtn');
    const seatsInput = document.getElementById('selectedSeatsInput');

    if (selectedSeatObjects.length > 0) {
        const seatCodes = selectedSeatObjects.map(s => s.code);
        const totalPrice = selectedSeatObjects.reduce((sum, s) => sum + (seatPrices[s.tier] || seatPrices['gold']), 0);

        if (seatsLabel) seatsLabel.innerText = seatCodes.join(', ');
        if (priceLabel) priceLabel.innerText = Math.round(totalPrice);
        if (seatsInput) seatsInput.value = seatCodes.join(', ');
        if (proceedBtn) proceedBtn.disabled = false;
    } else {
        if (seatsLabel) seatsLabel.innerText = 'None';
        if (priceLabel) priceLabel.innerText = '0';
        if (seatsInput) seatsInput.value = '';
        if (proceedBtn) proceedBtn.disabled = true;
    }
}

// =========================================================
// REAL-TIME SEAT AVAILABILITY SYNC & COLLISION PREVENTION
// =========================================================

function showToast(message, type = 'info') {
    let toast = document.getElementById('seatCollisionToast');
    if (!toast) {
        toast = document.createElement('div');
        toast.id = 'seatCollisionToast';
        toast.className = 'seat-collision-toast';
        document.body.appendChild(toast);
    }
    toast.innerHTML = `<i class="fa-solid fa-circle-exclamation"></i> <span>${message}</span>`;
    toast.className = `seat-collision-toast toast-${type} show`;
    toast.style.display = 'flex';

    if (window._toastTimeout) clearTimeout(window._toastTimeout);
    window._toastTimeout = setTimeout(() => {
        toast.className = 'seat-collision-toast';
        setTimeout(() => { toast.style.display = 'none'; }, 300);
    }, 4500);
}

function initLiveSeatSync() {
    const form = document.getElementById('bookingForm');
    if (!form || !form.dataset.statusUrl) return;

    const statusUrl = form.dataset.statusUrl;

    async function fetchSeatStatus() {
        try {
            const response = await fetch(statusUrl, {
                headers: { 'X-Requested-With': 'XMLHttpRequest' }
            });
            if (!response.ok) return;
            const data = await response.json();
            if (data.status !== 'success') return;

            const unavailable = new Set((data.unavailable_seats || []).map(s => s.toUpperCase()));
            let deselectedCodes = [];

            // Check every seat button on the grid
            const allSeatBtns = document.querySelectorAll('.seat-btn');
            allSeatBtns.forEach(btn => {
                const code = (btn.dataset.seat || '').trim().toUpperCase();
                if (!code) return;

                if (unavailable.has(code)) {
                    // Mark as booked/locked
                    if (!btn.classList.contains('booked')) {
                        btn.classList.add('booked');
                        btn.disabled = true;
                    }
                    // If the user had selected this seat, deselect immediately to prevent conflict
                    const idx = selectedSeatObjects.findIndex(s => s.code.toUpperCase() === code);
                    if (idx > -1) {
                        selectedSeatObjects.splice(idx, 1);
                        btn.classList.remove('selected');
                        deselectedCodes.push(code);
                    }
                } else {
                    // Seat is available (e.g. previous hold expired or released)
                    if (btn.classList.contains('booked')) {
                        btn.classList.remove('booked');
                        btn.disabled = false;
                    }
                }
            });

            if (deselectedCodes.length > 0) {
                updateSummary();
                showToast(`Notice: Seat(s) ${deselectedCodes.join(', ')} were just selected by another customer and have been unselected.`, 'error');
            }
        } catch (err) {
            console.warn('Real-time seat polling skipped:', err);
        }
    }

    // Fast initial check after 1.5s, then poll every 3.5 seconds
    setTimeout(fetchSeatStatus, 1500);
    setInterval(fetchSeatStatus, 3500);
}

document.addEventListener('DOMContentLoaded', () => {
    initSeatPrices();
    initLiveSeatSync();

    const form = document.getElementById('bookingForm');
    if (form) {
        form.addEventListener('submit', () => {
            const btn = document.getElementById('proceedBtn');
            if (btn) {
                btn.disabled = true;
                btn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Locking Seats...';
            }
        });
    }
});
