// =========================================================
// MOVIEMATE PAYMENT CHECKOUT JS
// Form Submission & Button Processing Feedback
// =========================================================

document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('checkoutForm');
    const btn = document.getElementById('payBtn');

    if (form && btn) {
        form.addEventListener('submit', () => {
            btn.disabled = true;
            btn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Verifying Payment & Issuing Pass...';
            btn.style.opacity = '0.75';
        });
    }
});

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
