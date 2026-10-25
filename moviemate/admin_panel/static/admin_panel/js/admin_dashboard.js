/**
 * MovieMate Admin Dashboard - Chart.js & Metrics Initialization
 * Dual Theme Adaptive (Light: Emerald/Slate, Dark: Soft Purple/Apple Slate)
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

    function getChartThemeOptions() {
        const isDark = document.documentElement.getAttribute('data-theme') === 'dark';
        return {
            barColor: isDark ? '#7c5cdb' : '#059669',
            barHover: isDark ? '#8b6ee8' : '#047857',
            borderColor: isDark ? '#a78bfa' : '#10b981',
            tooltipBg: isDark ? '#18181b' : '#0f172a',
            tooltipTitle: '#ffffff',
            tooltipBody: isDark ? '#a1a1a6' : '#cbd5e1',
            tooltipBorder: isDark ? '#27272a' : '#334155',
            xTicks: isDark ? '#71717a' : '#64748b',
            xGrid: isDark ? '#1e1e21' : '#f1f5f9',
            yTicks: isDark ? '#ffffff' : '#0f172a',
        };
    }

    const t = getChartThemeOptions();
    const ctx = canvas.getContext('2d');
    const chart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: cinemaLabels,
            datasets: [{
                label: 'Showtimes',
                data: cinemaShows,
                backgroundColor: t.barColor,
                borderColor: t.borderColor,
                borderWidth: 1,
                borderRadius: 6,
                borderSkipped: false,
                barThickness: 20,
                hoverBackgroundColor: t.barHover
            }]
        },
        options: {
            indexAxis: 'y',
            responsive: true,
            maintainAspectRatio: false,
            animation: {
                duration: 500,
                easing: 'easeOutQuart'
            },
            plugins: {
                legend: { display: false },
                tooltip: {
                    backgroundColor: t.tooltipBg,
                    titleColor: t.tooltipTitle,
                    bodyColor: t.tooltipBody,
                    borderColor: t.tooltipBorder,
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
                        color: t.xTicks,
                        font: { size: 11, weight: '600' },
                        precision: 0
                    },
                    grid: {
                        color: t.xGrid,
                        drawBorder: false
                    }
                },
                y: {
                    ticks: {
                        color: t.yTicks,
                        font: { size: 12, weight: '700' }
                    },
                    grid: { display: false }
                }
            }
        }
    });

    // Listen for themechange event to update Chart dynamically!
    document.addEventListener('themechange', function () {
        const next = getChartThemeOptions();
        chart.data.datasets[0].backgroundColor = next.barColor;
        chart.data.datasets[0].hoverBackgroundColor = next.barHover;
        chart.data.datasets[0].borderColor = next.borderColor;
        chart.options.plugins.tooltip.backgroundColor = next.tooltipBg;
        chart.options.plugins.tooltip.bodyColor = next.tooltipBody;
        chart.options.plugins.tooltip.borderColor = next.tooltipBorder;
        chart.options.scales.x.ticks.color = next.xTicks;
        chart.options.scales.x.grid.color = next.xGrid;
        chart.options.scales.y.ticks.color = next.yTicks;
        chart.update('none');
    });
});
