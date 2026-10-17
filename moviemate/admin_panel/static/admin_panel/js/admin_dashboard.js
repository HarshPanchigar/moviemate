/**
 * MovieMate Admin Dashboard - Chart.js & Metrics Initialization
 */

document.addEventListener('DOMContentLoaded', function () {
    const canvas = document.getElementById('cinemaDistributionChart');
    if (!canvas) return;

    let cinemaLabels = [];
    let cinemaShows = [];

    try {
        cinemaLabels = JSON.parse(canvas.getAttribute('data-labels') || '[]');
        cinemaShows = JSON.parse(canvas.getAttribute('data-values') || '[]');
    } catch (e) {
        console.error('Failed to parse chart data:', e);
    }

    const ctx = canvas.getContext('2d');
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: cinemaLabels,
            datasets: [{
                label: 'Showtimes',
                data: cinemaShows,
                backgroundColor: '#2563eb',
                borderColor: '#1d4ed8',
                borderWidth: 1,
                borderRadius: 6,
                borderSkipped: false,
                barThickness: 20,
                hoverBackgroundColor: '#1d4ed8'
            }]
        },
        options: {
            indexAxis: 'y',
            responsive: true,
            maintainAspectRatio: false,
            animation: {
                duration: 650,
                easing: 'easeOutQuart'
            },
            plugins: {
                legend: { display: false },
                tooltip: {
                    backgroundColor: '#0f172a',
                    titleColor: '#ffffff',
                    bodyColor: '#e2e8f0',
                    borderColor: '#334155',
                    borderWidth: 1,
                    padding: 10,
                    displayColors: false,
                    callbacks: {
                        label: function(context) {
                            return ' ' + context.raw + ' active showtimes';
                        }
                    }
                }
            },
            scales: {
                x: {
                    beginAtZero: true,
                    ticks: {
                        color: '#64748b',
                        font: { size: 11, weight: '500' },
                        precision: 0
                    },
                    grid: {
                        color: '#f1f5f9',
                        drawBorder: false
                    }
                },
                y: {
                    ticks: {
                        color: '#334155',
                        font: { size: 12, weight: '600' }
                    },
                    grid: { display: false }
                }
            }
        }
    });
});
