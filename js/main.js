(function () {
  var doc = document.documentElement;
  if ('ontouchstart' in window || (window.DocumentTouch && document instanceof window.DocumentTouch)) {
    doc.className += ' is-touch';
  }

  function loadScript(src, type) {
    var script = document.createElement('script');
    script.src = src;
    script.async = true;
    if (type) script.type = type;
    document.body.appendChild(script);
  }

  function observeOnce(target, onVisible, rootMargin) {
    if (!target || !('IntersectionObserver' in window)) {
      onVisible();
      return;
    }

    var observer = new IntersectionObserver(function (entries) {
      if (!entries[0].isIntersecting) return;
      observer.disconnect();
      onVisible();
    }, { rootMargin: rootMargin || '200px 0px' });

    observer.observe(target);
  }

  var nav = document.querySelector('.navbar');
  if (nav) {
    var menuButton = nav.querySelector('.menu-button');
    var navMenu = nav.querySelector('.navbar-menu');
    var closeButton = nav.querySelector('.menu-close-icon-wrap');

    function setMenuOpen(isOpen) {
      if (!menuButton || !navMenu) return;
      menuButton.classList.toggle('is-open', isOpen);
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
        setMenuOpen(!menuButton.classList.contains('is-open'));
      });
    }

    if (closeButton) {
      closeButton.addEventListener('click', function () {
        setMenuOpen(false);
      });
    }
  }

  document.querySelectorAll('.tabs').forEach(function (tabs) {
    var links = tabs.querySelectorAll('.tab-link');
    var panes = tabs.querySelectorAll('.tab-pane');

    links.forEach(function (link) {
      link.addEventListener('click', function (event) {
        event.preventDefault();
        var tabId = link.getAttribute('data-tab');
        if (!tabId) return;

        links.forEach(function (item) {
          item.classList.remove('is-current');
        });
        panes.forEach(function (pane) {
          pane.classList.remove('is-active');
        });

        link.classList.add('is-current');
        var activePane = tabs.querySelector('.tab-pane[data-tab="' + tabId + '"]');
        if (activePane) {
          activePane.classList.add('is-active');
        }
      });
    });
  });

  var videoEmbed = document.querySelector('.video-embed');
  if (videoEmbed) {
    observeOnce(videoEmbed, function () {
      loadScript('https://fast.wistia.com/player.js');
      loadScript('https://fast.wistia.com/embed/22htalunmu.js', 'module');
    });
  }

  observeOnce(document.getElementById('form-section'), function () {
    loadScript('https://app.iclosed.io/assets/widget.js');
  });

  document.addEventListener('play', function (event) {
    if (event.target && event.target.tagName === 'WISTIA-PLAYER') {
      var thumb = document.querySelector('.video-thumb-image');
      if (!thumb) return;
      thumb.style.opacity = '0';
      thumb.style.pointerEvents = 'none';
    }
  }, true);

  document.querySelectorAll('.faq-item-top').forEach(function (top) {
    top.addEventListener('click', function () {
      var answer = top.parentElement.querySelector('.faq-item-answer');
      var vertical = top.querySelector('.faq-icon-line.vertical');
      var lines = top.querySelectorAll('.faq-icon-line');
      var opened = answer.classList.contains('open');

      if (!opened) {
        answer.classList.add('open');
        answer.style.height = answer.scrollHeight + 'px';
        answer.addEventListener('transitionend', function handler() {
          answer.style.height = 'auto';
          answer.removeEventListener('transitionend', handler);
        });
        if (vertical) vertical.style.transform = 'rotate(90deg)';
        lines.forEach(function (line) {
          line.style.backgroundColor = '#028A49';
        });
      } else {
        answer.style.height = answer.scrollHeight + 'px';
        requestAnimationFrame(function () {
          answer.style.height = '0px';
        });
        answer.classList.remove('open');
        if (vertical) vertical.style.transform = 'rotate(0deg)';
        lines.forEach(function (line) {
          line.style.backgroundColor = '';
        });
      }
    });
  });

  window.addEventListener('load', function () {
    var widget = document.querySelector('.iclosed-widget');
    if (!widget || !widget.parentElement) return;

    var originalWidth = 1200;
    var originalHeight = 800;

    function resize() {
      var scale = widget.parentElement.clientWidth / originalWidth;
      widget.style.width = originalWidth + 'px';
      widget.style.height = originalHeight + 'px';
      widget.style.transform = 'scale(' + scale + ')';
      widget.style.transformOrigin = 'top left';
      widget.parentElement.style.height = originalHeight * scale + 'px';
    }

    resize();
    window.addEventListener('resize', resize);
  });
})();
