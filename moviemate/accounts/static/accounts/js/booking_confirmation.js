// =========================================================
// MOVIEMATE BOOKING CONFIRMATION & PDF PASS GENERATOR JS
// =========================================================

function downloadPdfTicket() {
    const btn = document.getElementById('downloadPdfBtn');
    const bookingId = (btn && btn.dataset.bookingId) ? btn.dataset.bookingId : 'Pass';

    if (btn) {
        btn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Generating High-Res PDF...';
        btn.disabled = true;
    }

    const element = document.getElementById('printablePdfArea');

    if (!element) {
        if (btn) {
            btn.innerHTML = '<i class="fa-solid fa-file-pdf"></i> Download Official PDF Pass';
            btn.disabled = false;
        }
        return;
    }

    html2canvas(element, {
        scale: 2.5,
        backgroundColor: '#ffffff',
        useCORS: true,
        logging: false
    }).then(canvas => {
        const { jsPDF } = window.jspdf;
        const imgData = canvas.toDataURL('image/png');

        // Create A4 PDF Document
        const pdf = new jsPDF({
            orientation: 'portrait',
            unit: 'mm',
            format: 'a4'
        });

        const imgWidth = 190;
        const imgHeight = (canvas.height * imgWidth) / canvas.width;

        pdf.addImage(imgData, 'PNG', 10, 10, imgWidth, imgHeight);
        pdf.save(`MovieMate_Pass_${bookingId}.pdf`);

        if (btn) {
            btn.innerHTML = '<i class="fa-solid fa-file-pdf"></i> Download Official PDF Pass';
            btn.disabled = false;
        }
    }).catch(err => {
        console.error('PDF error:', err);
        window.print();
        if (btn) {
            btn.innerHTML = '<i class="fa-solid fa-file-pdf"></i> Download Official PDF Pass';
            btn.disabled = false;
        }
    });
}
