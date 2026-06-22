/* City Plaza clone — interactions */
(function () {
  'use strict';

  /* ---------- sticky header shadow ---------- */
  const header = document.getElementById('header');
  const onScroll = () => {
    header.classList.toggle('is-scrolled', window.scrollY > 10);
    toTop.classList.toggle('is-show', window.scrollY > 600);
  };

  /* ---------- mobile nav ---------- */
  const burger = document.getElementById('burger');
  const nav = document.getElementById('primaryNav');
  burger.addEventListener('click', () => {
    const open = nav.classList.toggle('is-open');
    burger.classList.toggle('is-open', open);
    document.body.style.overflow = open ? 'hidden' : '';
  });
  nav.querySelectorAll('a').forEach((a) =>
    a.addEventListener('click', () => {
      nav.classList.remove('is-open');
      burger.classList.remove('is-open');
      document.body.style.overflow = '';
    })
  );

  /* ---------- reveal on scroll ---------- */
  const reveals = document.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window) {
    const io = new IntersectionObserver(
      (entries) => {
        entries.forEach((e) => {
          if (e.isIntersecting) {
            e.target.classList.add('is-in');
            io.unobserve(e.target);
          }
        });
      },
      { threshold: 0.12, rootMargin: '0px 0px -8% 0px' }
    );
    reveals.forEach((el) => io.observe(el));
  } else {
    reveals.forEach((el) => el.classList.add('is-in'));
  }

  /* ---------- events carousel ---------- */
  const track = document.getElementById('eventsTrack');
  const prev = document.getElementById('evPrev');
  const next = document.getElementById('evNext');
  if (track && prev && next) {
    let index = 0;
    const cards = track.children;
    const perView = () => {
      const w = window.innerWidth;
      if (w <= 760) return 1;
      if (w <= 1100) return 3;
      return 4;
    };
    const maxIndex = () => Math.max(0, cards.length - perView());
    const update = () => {
      const card = cards[0];
      const gap = parseFloat(getComputedStyle(track).gap) || 24;
      const step = card.getBoundingClientRect().width + gap;
      index = Math.min(index, maxIndex());
      track.style.transform = `translateX(${-index * step}px)`;
      prev.style.opacity = index === 0 ? '.4' : '1';
      next.style.opacity = index >= maxIndex() ? '.4' : '1';
    };
    prev.addEventListener('click', () => { index = Math.max(0, index - 1); update(); });
    next.addEventListener('click', () => { index = Math.min(maxIndex(), index + 1); update(); });
    window.addEventListener('resize', update);
    update();
  }

  /* ---------- plan level tabs ---------- */
  const tabs = document.getElementById('planTabs');
  if (tabs) {
    tabs.addEventListener('click', (e) => {
      const btn = e.target.closest('.pill');
      if (!btn) return;
      tabs.querySelectorAll('.pill').forEach((p) => p.classList.remove('is-active'));
      btn.classList.add('is-active');
    });
  }

  /* ---------- back to top ---------- */
  const toTop = document.getElementById('toTop');
  toTop.addEventListener('click', () =>
    window.scrollTo({ top: 0, behavior: 'smooth' })
  );

  /* ---------- invio form via fetch (newsletter + popup) ---------- */
  const ajaxSubmit = (form, onSuccess) => {
    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      const btn = form.querySelector('button[type="submit"]');
      const action = form.getAttribute('action');
      if (!action) return; // niente endpoint: ignora
      const label = btn ? btn.textContent : '';
      if (btn) { btn.disabled = true; btn.textContent = 'Invio…'; }
      try {
        const res = await fetch(action, { method: 'POST', body: new FormData(form) });
        let data = {};
        try { data = await res.json(); } catch (_) {}
        const ok = res.ok && data.ok;
        onSuccess(ok, data.message || (ok ? 'Fatto!' : 'Si è verificato un errore. Riprova.'), form);
      } catch (err) {
        onSuccess(false, 'Connessione non riuscita. Riprova più tardi.', form);
      } finally {
        if (btn) { btn.disabled = false; btn.textContent = label; }
      }
    });
  };

  /* newsletter (sezione + popup): sostituisce il form col messaggio */
  document.querySelectorAll('#newsletterForm, #popupForm').forEach((form) =>
    ajaxSubmit(form, (ok, msg) => {
      if (ok) {
        form.innerHTML =
          '<p style="font-weight:600;padding:8px 0;color:#1a7f4b">' + msg + '</p>';
      } else {
        let s = form.querySelector('.form-status');
        if (!s) {
          s = document.createElement('p');
          s.className = 'form-status';
          s.style.flexBasis = '100%';
          form.appendChild(s);
        }
        s.textContent = msg;
        s.className = 'form-status is-err';
      }
    })
  );

  /* form contatti "apri il tuo negozio" */
  const contactForm = document.getElementById('contactForm');
  if (contactForm) {
    const status = document.getElementById('contactStatus');
    ajaxSubmit(contactForm, (ok, msg) => {
      status.textContent = msg;
      status.className = 'form-status ' + (ok ? 'is-ok' : 'is-err');
      if (ok) contactForm.reset();
    });
  }

  /* ---------- newsletter popup ---------- */
  const popup = document.getElementById('popup');
  const popupClose = document.getElementById('popupClose');
  if (popup && !sessionStorage.getItem('cp_popup_closed')) {
    setTimeout(() => popup.classList.add('is-open'), 5000);
  }
  const closePopup = () => {
    popup.classList.remove('is-open');
    sessionStorage.setItem('cp_popup_closed', '1');
  };
  popupClose && popupClose.addEventListener('click', closePopup);
  popup &&
    popup.addEventListener('click', (e) => {
      if (e.target === popup) closePopup();
    });

  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();
})();
