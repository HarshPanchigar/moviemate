document.addEventListener('DOMContentLoaded', function () {

  // Highlight the active nav link on click
  var navLinks = document.querySelectorAll('.mm-links .nav-link');
  navLinks.forEach(function (link) {
    link.addEventListener('click', function () {
      navLinks.forEach(function (l) { l.classList.remove('active'); });
      link.classList.add('active');
    });
  });

  // Close the mobile collapse menu after a link/button is tapped
  var collapseEl = document.getElementById('mmNavCollapse');
  if (collapseEl && window.bootstrap) {
    var bsCollapse = new bootstrap.Collapse(collapseEl, { toggle: false });
    var closers = collapseEl.querySelectorAll('.nav-link, .mm-btn');
    closers.forEach(function (el) {
      el.addEventListener('click', function () {
        if (collapseEl.classList.contains('show')) {
          bsCollapse.hide();
        }
      });
    });
  }

});