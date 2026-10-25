// =========================================================
// MOVIEMATE PAYMENT CHECKOUT JS
// Form Submission, UPI Copy & Real-Time Seat Reservation Timer
// =========================================================

document.addEventListener('DOMContentLoaded', () => {
    // 1. Payment Form Submission State
    const form = document.getElementById('checkoutForm');
    const btn = document.getElementById('payBtn');

    if (form && btn) {
        form.addEventListener('submit', (e) => {
            if (btn.disabled) {
                e.preventDefault();
                return;
            }
            btn.disabled = true;
            btn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Securing Seats & Issuing Pass...';
            btn.style.opacity = '0.8';
        });
    }

    // 2. Active Seat Hold Countdown Timer
    initSeatHoldTimer();
});

function initSeatHoldTimer() {
    const alertBox = document.getElementById('seatHoldAlert');
    const timerBadge = document.getElementById('holdTimerBadge');
    const payBtn = document.getElementById('payBtn');

    if (!alertBox || !timerBadge) return;

    let remaining = parseInt(alertBox.dataset.remaining, 10);
    if (isNaN(remaining)) remaining = 480;

    const releaseUrl = alertBox.dataset.releaseUrl || window.location.href;

    function formatTime(secs) {
        const m = Math.floor(secs / 60);
        const s = secs % 60;
        return `${m < 10 ? '0' : ''}${m}:${s < 10 ? '0' : ''}${s}`;
    }

    function handleExpired() {
        timerBadge.textContent = '00:00';
        timerBadge.classList.add('expired');
        alertBox.classList.add('expired');

        if (payBtn) {
            payBtn.disabled = true;
            payBtn.style.opacity = '0.5';
            payBtn.style.cursor = 'not-allowed';
            payBtn.innerHTML = '<i class="fa-solid fa-clock"></i> Reservation Expired';
        }

        setTimeout(() => {
            alert('Your 8-minute seat reservation has expired. Please choose your seats again.');
            window.location.href = releaseUrl;
        }, 150);
    }

    if (remaining <= 0) {
        handleExpired();
        return;
    }

    // Set initial text and urgent styling immediately
    timerBadge.textContent = formatTime(remaining);
    if (remaining <= 60) {
        timerBadge.classList.add('urgent');
        alertBox.classList.add('urgent');
    }

    // Use absolute end timestamp to prevent background tab drift
    const endTime = Date.now() + (remaining * 1000);

    const interval = setInterval(() => {
        const now = Date.now();
        const secondsLeft = Math.max(0, Math.round((endTime - now) / 1000));

        if (secondsLeft <= 0) {
            clearInterval(interval);
            handleExpired();
            return;
        }

        timerBadge.textContent = formatTime(secondsLeft);

        // Turn orange/red when under 60 seconds
        if (secondsLeft <= 60) {
            timerBadge.classList.add('urgent');
            alertBox.classList.add('urgent');
        }
    }, 1000);
}

function copyUPI(text) {
    if (navigator.clipboard) {
        navigator.clipboard.writeText(text).then(() => {
            const fb = document.getElementById('copyFeedback');
            if (fb) {
                fb.textContent = 'Copied!';
                setTimeout(() => { fb.textContent = 'Copy'; }, 2000);
            }
        });
    }
}
