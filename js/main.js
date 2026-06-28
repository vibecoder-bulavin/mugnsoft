(function () {
  var doc = document.documentElement;
  if ('ontouchstart' in window || (window.DocumentTouch && document instanceof window.DocumentTouch)) {
    doc.className += ' is-touch';
  }

  var nav = document.querySelector('.w-nav');
  if (nav) {
    var menuButton = nav.querySelector('.w-nav-button');
    var navMenu = nav.querySelector('.w-nav-menu');
    var closeButton = nav.querySelector('.menu-close-icon-wrap');

    function setMenuOpen(isOpen) {
      if (!menuButton || !navMenu) return;
      menuButton.classList.toggle('w--open', isOpen);
      if (isOpen) {
        navMenu.setAttribute('data-nav-menu-open', '');
        document.body.style.overflow = 'hidden';
      } else {
        navMenu.removeAttribute('data-nav-menu-open');
        document.body.style.overflow = '';
      }
    }

    if (menuButton) {
      menuButton.addEventListener('click', function () {
        setMenuOpen(!menuButton.classList.contains('w--open'));
      });
    }

    if (closeButton) {
      closeButton.addEventListener('click', function () {
        setMenuOpen(false);
      });
    }
  }

  document.querySelectorAll('.w-tabs').forEach(function (tabs) {
    var links = tabs.querySelectorAll('.w-tab-link');
    var panes = tabs.querySelectorAll('.w-tab-pane');

    links.forEach(function (link) {
      link.addEventListener('click', function (event) {
        event.preventDefault();
        var tabId = link.getAttribute('data-tab');
        if (!tabId) return;

        links.forEach(function (item) {
          item.classList.remove('w--current');
        });
        panes.forEach(function (pane) {
          pane.classList.remove('w--tab-active');
        });

        link.classList.add('w--current');
        var activePane = tabs.querySelector('.w-tab-pane[data-tab="' + tabId + '"]');
        if (activePane) {
          activePane.classList.add('w--tab-active');
        }
      });
    });
  });
})();
