/**
 * MovieMate Admin Panel - Base Global Utilities
 * Modal handling, responsive sidebar, toast system, and dual theme engine
 */

// ---------------------------------------------------------
// Theme Management (Light Mode & Apple Dark Mode)
// Shared with Client via 'moviemate-theme' in localStorage
// ---------------------------------------------------------
function updateAdminThemeToggleState(theme) {
    const toggleBtn = document.getElementById('themeToggleBtn');
    if (!toggleBtn) return;
    const isDark = theme === 'dark';
    toggleBtn.setAttribute('title', isDark ? 'Switch to Light mode' : 'Switch to Dark mode');
    toggleBtn.setAttribute('aria-label', isDark ? 'Switch to Light mode' : 'Switch to Dark mode');
    toggleBtn.setAttribute('aria-checked', isDark ? 'true' : 'false');
}

function syncAdminThemeState() {
    try {
        const savedTheme = localStorage.getItem('moviemate-theme');
        const prefersDark = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
        const targetTheme = (savedTheme === 'dark' || (!savedTheme && prefersDark)) ? 'dark' : 'light';

        if (document.documentElement.getAttribute('data-theme') !== targetTheme) {
            document.documentElement.setAttribute('data-theme', targetTheme);
        }
        updateAdminThemeToggleState(targetTheme);
    } catch (err) {
        console.warn('Unable to sync theme from storage', err);
    }
}

function initAdminThemeToggle() {
    const toggleBtn = document.getElementById('themeToggleBtn');
    if (!toggleBtn) return;

    syncAdminThemeState();

    if (!toggleBtn.dataset.themeBound) {
        toggleBtn.dataset.themeBound = 'true';
        toggleBtn.addEventListener('click', () => {
            const activeTheme = document.documentElement.getAttribute('data-theme') || 'light';
            const nextTheme = activeTheme === 'dark' ? 'light' : 'dark';

            document.documentElement.classList.add('theme-transition');
            document.documentElement.setAttribute('data-theme', nextTheme);

            try {
                localStorage.setItem('moviemate-theme', nextTheme);
            } catch (err) {
                console.warn('Unable to persist theme in localStorage', err);
            }

            updateAdminThemeToggleState(nextTheme);

            // Dispatch themechange event for charts and reactive components
            document.dispatchEvent(new CustomEvent('themechange', { detail: { theme: nextTheme } }));

            setTimeout(() => {
                document.documentElement.classList.remove('theme-transition');
            }, 300);
        });
    }

    // Sync across tabs / back navigation
    window.addEventListener('storage', (e) => {
        if (e.key === 'moviemate-theme') {
            syncAdminThemeState();
            const currentTheme = document.documentElement.getAttribute('data-theme') || 'light';
            document.dispatchEvent(new CustomEvent('themechange', { detail: { theme: currentTheme } }));
        }
    });

    window.addEventListener('pageshow', () => {
        syncAdminThemeState();
    });
}

// ---------------------------------------------------------
// Modal Open/Close Utilities
// ---------------------------------------------------------
function openAdminModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.style.display = 'flex';
        document.body.style.overflow = 'hidden';
    }
}

function closeAdminModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.style.display = 'none';
        document.body.style.overflow = '';
    }
}

// Global modal backdrop click & Escape key listener
document.addEventListener('DOMContentLoaded', () => {
    // Initialize Theme Toggle
    initAdminThemeToggle();

    // Backdrop click close
    document.querySelectorAll('.modal-overlay').forEach(modal => {
        modal.addEventListener('click', (e) => {
            if (e.target === modal) {
                modal.style.display = 'none';
                document.body.style.overflow = '';
            }
        });
    });

    // Escape key close
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
            document.querySelectorAll('.modal-overlay').forEach(modal => {
                if (modal.style.display === 'flex') {
                    modal.style.display = 'none';
                    document.body.style.overflow = '';
                }
            });
        }
    });
});

// ---------------------------------------------------------
// Global Admin Toast System (Dual Theme Adaptive)
// ---------------------------------------------------------
function showAdminToast(message, type = 'success') {
    let container = document.getElementById('adminToastContainer');
    if (!container) {
        container = document.createElement('div');
        container.id = 'adminToastContainer';
        container.style.cssText = `
            position: fixed;
            top: 24px;
            right: 24px;
            z-index: 999999;
            display: flex;
            flex-direction: column;
            gap: 10px;
            max-width: 440px;
            pointer-events: none;
        `;
        document.body.appendChild(container);
    }

    const toast = document.createElement('div');
    const isError = type === 'error';
    const isDark = document.documentElement.getAttribute('data-theme') === 'dark';

    toast.style.cssText = `
        pointer-events: auto;
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 13px 18px;
        background: ${isError ? (isDark ? '#261214' : '#fef2f2') : (isDark ? '#121214' : '#ffffff')};
        border: 1px solid ${isError ? (isDark ? '#7f1d1d' : '#fecaca') : (isDark ? '#27272a' : '#e2e8f0')};
        border-left: 4px solid ${isError ? '#ef4444' : (isDark ? '#7c5cdb' : '#059669')};
        border-radius: 8px;
        color: ${isError ? (isDark ? '#fecaca' : '#991b1b') : (isDark ? '#ffffff' : '#0f172a')};
        font-size: 13px;
        font-weight: 600;
        box-shadow: 0 10px 25px -5px rgba(0,0,0,0.18), 0 8px 10px -6px rgba(0,0,0,0.1);
        transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
        transform: translateY(-8px);
        opacity: 0;
    `;
    toast.innerHTML = `
        <i class="fa-solid ${isError ? 'fa-triangle-exclamation' : 'fa-circle-check'}" style="color: ${isError ? '#ef4444' : (isDark ? '#7c5cdb' : '#059669')}; font-size: 16px; flex-shrink: 0;"></i>
        <span style="flex: 1; line-height: 1.4;">${message}</span>
        <button type="button" style="background: none; border: none; color: inherit; cursor: pointer; font-size: 16px; opacity: 0.6; line-height: 1; padding: 0 4px;" onclick="this.parentElement.remove()">&times;</button>
    `;

    container.appendChild(toast);

    // Animate in
    requestAnimationFrame(() => {
        toast.style.transform = 'translateY(0)';
        toast.style.opacity = '1';
    });

    // Auto dismiss after 3.5s
    setTimeout(() => {
        toast.style.opacity = '0';
        toast.style.transform = 'translateX(20px)';
        setTimeout(() => toast.remove(), 250);
    }, 3500);
}
