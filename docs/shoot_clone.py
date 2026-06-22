import time
from pathlib import Path
from playwright.sync_api import sync_playwright

OUT = Path("docs/clone-shots"); OUT.mkdir(parents=True, exist_ok=True)
URL = "http://localhost:8777/index.html"

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width":1440,"height":900}, device_scale_factor=1)
    pg.add_init_script("try{sessionStorage.setItem('cp_popup_closed','1')}catch(e){}")
    errors=[]
    pg.on("console", lambda m: errors.append(m.text) if m.type=="error" else None)
    pg.on("pageerror", lambda e: errors.append("PAGEERROR: "+str(e)))
    pg.goto(URL, wait_until="networkidle", timeout=60000)
    time.sleep(1.5)
    # reveal everything: scroll through
    h=pg.evaluate("document.body.scrollHeight"); y=0
    while y<h:
        pg.evaluate(f"window.scrollTo(0,{y})"); time.sleep(0.25); y+=600
        h=pg.evaluate("document.body.scrollHeight")
    pg.evaluate("window.scrollTo(0,0)"); time.sleep(0.8)
    pg.screenshot(path=str(OUT/"clone-full.png"), full_page=True)
    # tiles
    fh=pg.evaluate("document.body.scrollHeight"); vh=900; n=fh//vh+1
    for i in range(n):
        pg.evaluate(f"window.scrollTo(0,{i*vh})"); time.sleep(0.4)
        pg.screenshot(path=str(OUT/f"c-{i:02d}.png"))
    print("tiles",n,"docH",fh)
    print("CONSOLE ERRORS:", errors if errors else "none")
    b.close()
