/* Copyright (c) 2026 Mustafa Uzumeri. All rights reserved. */

/**
 * Scroll reveal animation script.
 * Observes elements with class 'reveal' and adds 'reveal--visible' when they enter viewport.
 */
(function initReveal() {
  const reveals = document.querySelectorAll('.reveal');

  if (!reveals.length) return;

  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add('reveal--visible');
          observer.unobserve(entry.target);
        }
      });
    },
    {
      threshold: 0.15,
      rootMargin: '0px 0px -40px 0px',
    }
  );

  reveals.forEach((el, index) => {
    el.style.transitionDelay = `${index * 80}ms`;
    observer.observe(el);
  });
})();
