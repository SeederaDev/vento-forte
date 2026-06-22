"""Recon v3: hard-remove popups from DOM, capture clean tiles + key sections."""
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

URL = "https://city-plaza.cmsmasters.studio/main/"
OUT = Path("docs/design-references")
tiles = OUT / "clean-tiles"; tiles.mkdir(parents=True, exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 1440, "height": 900}, device_scale_factor=1)
    page.goto(URL, wait_until="networkidle", timeout=90000)
    time.sleep(4)  # let popup appear

    nuke = """
      document.querySelectorAll('.dialog-widget, .elementor-popup-modal, .dialog-lightbox-widget, .cmsmasters-demos-preview, [class*="popup"]').forEach(e=>e.remove());
      document.body.style.overflow='auto';
      document.documentElement.style.overflow='auto';
      document.body.classList.remove('elementor-popup-modal-open');
    """
    page.evaluate(nuke)
    time.sleep(0.5)

    # slow scroll to load, nuking popups each step
    h = page.evaluate("document.body.scrollHeight"); y = 0
    while y < h:
        page.evaluate(f"window.scrollTo(0,{y})"); page.evaluate(nuke); time.sleep(0.3)
        y += 600; h = page.evaluate("document.body.scrollHeight")
    page.evaluate("window.scrollTo(0,document.body.scrollHeight)"); time.sleep(1)
    page.evaluate(nuke)
    page.evaluate("window.scrollTo(0,0)"); time.sleep(1)
    page.evaluate(nuke); time.sleep(0.3)

    fh = page.evaluate("document.body.scrollHeight")
    page.screenshot(path=str(OUT / "clean-full-desktop.png"), full_page=True)

    vh = 900; n = fh//vh + 1
    for i in range(n):
        page.evaluate(f"window.scrollTo(0,{i*vh})"); page.evaluate(nuke); time.sleep(0.45)
        page.screenshot(path=str(tiles / f"t-{i:02d}.png"))
    print("tiles:", n, "docH:", fh)
    browser.close()
print("DONE")
