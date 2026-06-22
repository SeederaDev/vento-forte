"""Full-page recon that scrolls slowly to trigger lazy-load + scroll animations,
then captures section screenshots and extracts real content."""
import json
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

URL = "https://city-plaza.cmsmasters.studio/main/"
OUT = Path("docs/design-references")
OUT.mkdir(parents=True, exist_ok=True)
RES = Path("docs/research")
RES.mkdir(parents=True, exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 1440, "height": 900}, device_scale_factor=1)
    page.goto(URL, wait_until="networkidle", timeout=90000)
    time.sleep(2)

    # Slow scroll to trigger lazy load + scroll-reveal animations
    height = page.evaluate("document.body.scrollHeight")
    step = 600
    y = 0
    while y < height:
        page.evaluate(f"window.scrollTo(0, {y})")
        time.sleep(0.35)
        y += step
        height = page.evaluate("document.body.scrollHeight")  # may grow
    # scroll to very bottom and back to top
    page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
    time.sleep(1.5)
    page.evaluate("window.scrollTo(0, 0)")
    time.sleep(1.5)

    final_height = page.evaluate("document.body.scrollHeight")
    print(f"Final document height: {final_height}")

    # Full page screenshot now that everything is loaded
    page.screenshot(path=str(OUT / "full-loaded-desktop.png"), full_page=True)
    print("Saved full-loaded-desktop.png")

    # Capture viewport-by-viewport tiles for detail
    tiles_dir = OUT / "tiles"
    tiles_dir.mkdir(exist_ok=True)
    vh = 900
    n = (final_height // vh) + 1
    for i in range(n):
        page.evaluate(f"window.scrollTo(0, {i*vh})")
        time.sleep(0.6)
        page.screenshot(path=str(tiles_dir / f"tile-{i:02d}.png"))
    print(f"Saved {n} tiles")

    # Extract section structure: top-level Elementor sections with text + bg
    page.evaluate("window.scrollTo(0, 0)")
    sections = page.evaluate(r"""
    () => {
        const secs = document.querySelectorAll('section.elementor-section.elementor-top-section, .elementor-top-section');
        const out = [];
        secs.forEach((s, i) => {
            const rect = s.getBoundingClientRect();
            const cs = getComputedStyle(s);
            const text = (s.innerText || '').trim().slice(0, 600);
            const imgs = [...s.querySelectorAll('img')].map(im => im.currentSrc || im.src).slice(0, 12);
            const bg = cs.backgroundColor;
            const bgImg = cs.backgroundImage;
            out.push({i, top: Math.round(rect.top + window.scrollY), height: Math.round(rect.height), bg, bgImg: bgImg !== 'none' ? bgImg : '', text, imgs});
        });
        return out;
    }
    """)
    (RES / "sections.json").write_text(json.dumps(sections, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Extracted {len(sections)} top sections -> sections.json")

    # Extract header/nav + all images with alt
    meta = page.evaluate(r"""
    () => {
        const headerText = (document.querySelector('header, .elementor-location-header')?.innerText || '').trim();
        const navLinks = [...document.querySelectorAll('header a, .elementor-location-header a')].map(a => ({t:(a.innerText||'').trim(), href:a.href})).filter(x=>x.t);
        const footerText = (document.querySelector('footer, .elementor-location-footer')?.innerText || '').trim();
        const allImgs = [...document.querySelectorAll('img')].map(im => ({src: im.currentSrc||im.src, alt: im.alt, w: im.naturalWidth, h: im.naturalHeight}));
        const title = document.title;
        return {title, headerText, navLinks, footerText, allImgs};
    }
    """)
    (RES / "page-meta.json").write_text(json.dumps(meta, indent=2, ensure_ascii=False), encoding="utf-8")
    print("Saved page-meta.json")

    browser.close()
print("DONE")
