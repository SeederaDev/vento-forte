import time
from pathlib import Path
from playwright.sync_api import sync_playwright
OUT = Path("docs/clone-shots/ventoforte"); OUT.mkdir(parents=True, exist_ok=True)
URL = "http://localhost:8777/index.html"
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width":1440,"height":600}, device_scale_factor=1)
    pg.add_init_script("try{sessionStorage.setItem('cp_popup_closed','1')}catch(e){}")
    pg.goto(URL, wait_until="networkidle", timeout=60000)
    time.sleep(1.2)
    pg.evaluate("window.scrollTo(0,0)"); time.sleep(0.4)
    pg.screenshot(path=str(OUT/"top-v3.png"))
    print("done")
    b.close()
