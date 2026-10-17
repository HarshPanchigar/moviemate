// =========================================================
// MOVIEMATE SELECT SEATS JS
// Seating Matrix Selection & Live Dynamic Price Calculation
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
    if (btn.classList.contains('booked')) return;

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

document.addEventListener('DOMContentLoaded', () => {
    initSeatPrices();
});
