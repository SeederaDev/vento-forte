import time
from pathlib import Path
from playwright.sync_api import sync_playwright
OUT = Path("docs/clone-shots/ventoforte"); OUT.mkdir(parents=True, exist_ok=True)
URL = "http://localhost:8777/contatti.html"
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width":1440,"height":1000}, device_scale_factor=1)
    errs=[]
    pg.on("console", lambda m: errs.append(m.text) if m.type=="error" else None)
    pg.on("pageerror", lambda e: errs.append("PAGEERR: "+str(e)))
    pg.goto(URL, wait_until="networkidle", timeout=60000)
    time.sleep(1.2)
    pg.screenshot(path=str(OUT/"contatti-page.png"), full_page=True)
    # mobile
    m = b.new_page(viewport={"width":390,"height":844})
    m.goto(URL, wait_until="networkidle", timeout=60000)
    time.sleep(1)
    m.screenshot(path=str(OUT/"contatti-mobile.png"), full_page=True)
    print("CONSOLE:", errs if errs else "none")
    b.close()
