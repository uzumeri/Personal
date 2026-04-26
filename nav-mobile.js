/* Copyright (c) 2026 Mustafa Uzumeri. All rights reserved. */

/**
 * Mobile hamburger navigation toggle.
 * Controls the hamburger button and mobile nav overlay for screens ≤ 768px.
 */
(function initMobileNav() {
    const toggle = document.getElementById('nav-toggle');
    const links = document.querySelector('.nav__links');
    const nav = document.getElementById('nav');

    if (!toggle || !links) return;

    /** Toggle the mobile menu open/closed. */
    function toggleMenu() {
        const isOpen = toggle.getAttribute('aria-expanded') === 'true';
        toggle.setAttribute('aria-expanded', String(!isOpen));
        links.classList.toggle('nav__links--open');
        document.body.classList.toggle('nav-open');
    }

    /** Close the mobile menu. */
    function closeMenu() {
        toggle.setAttribute('aria-expanded', 'false');
        links.classList.remove('nav__links--open');
        document.body.classList.remove('nav-open');
    }

    toggle.addEventListener('click', toggleMenu);

    // Close menu when a nav link is clicked
    links.querySelectorAll('.nav__link').forEach(function (link) {
        link.addEventListener('click', closeMenu);
    });

    // Close menu when clicking outside the nav
    document.addEventListener('click', function (e) {
        if (!nav.contains(e.target) && links.classList.contains('nav__links--open')) {
            closeMenu();
        }
    });

    // Close menu on Escape key
    document.addEventListener('keydown', function (e) {
        if (e.key === 'Escape' && links.classList.contains('nav__links--open')) {
            closeMenu();
            toggle.focus();
        }
    });
})();
