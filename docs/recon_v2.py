"""Recon v2: close popup, extract real text content + clean tiles."""
import json, time
from pathlib import Path
from playwright.sync_api import sync_playwright

URL = "https://city-plaza.cmsmasters.studio/main/"
OUT = Path("docs/design-references")
RES = Path("docs/research")

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 1440, "height": 900}, device_scale_factor=1)
    page.goto(URL, wait_until="networkidle", timeout=90000)
    time.sleep(3)

    # Try to close any popup/modal
    for sel in [".dialog-close-button", ".elementor-popup-modal .dialog-close-button",
                "[role=button][aria-label*=close i]", ".cmsmasters-demos-preview__close",
                ".dialog-lightbox-close-button"]:
        try:
            els = page.query_selector_all(sel)
            for e in els:
                if e.is_visible():
                    e.click(timeout=1500)
                    time.sleep(0.5)
        except Exception:
            pass
    page.keyboard.press("Escape")
    time.sleep(1)
    # Hide demo preview bar + any leftover popups via CSS
    page.add_style_tag(content="""
      .cmsmasters-demos-preview, .elementor-popup-modal, .dialog-widget { display:none !important; }
    """)
    time.sleep(0.5)

    # slow scroll to load
    h = page.evaluate("document.body.scrollHeight")
    y = 0
    while y < h:
        page.evaluate(f"window.scrollTo(0,{y})"); time.sleep(0.3); y += 600
        h = page.evaluate("document.body.scrollHeight")
    page.evaluate("window.scrollTo(0,document.body.scrollHeight)"); time.sleep(1)
    page.evaluate("window.scrollTo(0,0)"); time.sleep(1)

    fh = page.evaluate("document.body.scrollHeight")
    page.screenshot(path=str(OUT / "clean-full-desktop.png"), full_page=True)

    # clean tiles
    tiles = OUT / "clean-tiles"; tiles.mkdir(exist_ok=True)
    vh = 900; n = fh//vh + 1
    for i in range(n):
        page.evaluate(f"window.scrollTo(0,{i*vh})"); time.sleep(0.5)
        page.screenshot(path=str(tiles / f"t-{i:02d}.png"))
    page.evaluate("window.scrollTo(0,0)"); time.sleep(0.5)

    # Extract header nav, sections, footer with broad selectors
    data = page.evaluate(r"""
    () => {
      const clean = s => (s||'').replace(/\s+/g,' ').trim();
      // header
      const header = document.querySelector('.elementor-location-header') || document.querySelector('header');
      const nav = header ? [...header.querySelectorAll('a')].map(a=>({t:clean(a.innerText),href:a.href})).filter(x=>x.t) : [];
      const headerText = header ? clean(header.innerText) : '';
      // top sections: use .e-con (containers) and section
      const conts = [...document.querySelectorAll('.elementor-section.elementor-top-section, .e-con.e-parent, section[data-element_type]')];
      const seen = new Set();
      const secs = [];
      conts.forEach(s => {
        const r = s.getBoundingClientRect();
        const top = Math.round(r.top + window.scrollY);
        const key = top + 'x' + Math.round(r.height);
        if (seen.has(key) || r.height < 40) return; seen.add(key);
        const cs = getComputedStyle(s);
        secs.push({
          top, height: Math.round(r.height),
          bg: cs.backgroundColor,
          bgImg: cs.backgroundImage !== 'none' ? cs.backgroundImage.slice(0,200) : '',
          headings: [...s.querySelectorAll('h1,h2,h3,h4')].map(h=>clean(h.innerText)).filter(Boolean).slice(0,15),
          text: clean(s.innerText).slice(0,500),
          imgs: [...s.querySelectorAll('img')].map(im=>im.currentSrc||im.src).slice(0,10),
          buttons: [...s.querySelectorAll('a.elementor-button, .elementor-button, button')].map(b=>clean(b.innerText)).filter(Boolean).slice(0,6)
        });
      });
      secs.sort((a,b)=>a.top-b.top);
      const footer = document.querySelector('.elementor-location-footer') || document.querySelector('footer');
      const footerText = footer ? clean(footer.innerText) : '';
      const footerLinks = footer ? [...footer.querySelectorAll('a')].map(a=>({t:clean(a.innerText),href:a.href})).filter(x=>x.t) : [];
      const bodyText = clean(document.body.innerText);
      return {nav, headerText, sections: secs, footerText, footerLinks, bodyText};
    }
    """)
    (RES / "content.json").write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    print("sections:", len(data["sections"]), "nav:", len(data["nav"]), "tiles:", n, "docH:", fh)
    browser.close()
print("DONE")
