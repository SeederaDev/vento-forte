import time
from pathlib import Path
from playwright.sync_api import sync_playwright
OUT = Path("docs/clone-shots/ventoforte"); OUT.mkdir(parents=True, exist_ok=True)
URL = "http://localhost:8777/index.html"
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width":1440,"height":900}, device_scale_factor=1)
    pg.add_init_script("try{sessionStorage.setItem('cp_popup_closed','1')}catch(e){}")
    errs=[]
    pg.on("console", lambda m: errs.append(m.text) if m.type=="error" else None)
    pg.on("pageerror", lambda e: errs.append("PAGEERR: "+str(e)))
    pg.goto(URL, wait_until="networkidle", timeout=60000)
    time.sleep(1)
    h=pg.evaluate("document.body.scrollHeight"); y=0
    while y<h:
        pg.evaluate(f"window.scrollTo(0,{y})"); time.sleep(0.18); y+=600
        h=pg.evaluate("document.body.scrollHeight")
    pg.evaluate("window.scrollTo(0,0)"); time.sleep(0.5)
    pg.evaluate("document.querySelector('.visit').scrollIntoView()"); time.sleep(0.5)
    pg.query_selector(".visit").screenshot(path=str(OUT/"visit-3col.png"))
    # top for azure header/topbar
    pg.evaluate("window.scrollTo(0,0)"); time.sleep(0.4)
    pg.screenshot(path=str(OUT/"top-azure.png"), clip={"x":0,"y":0,"width":1440,"height":420})
    print("CONSOLE:", errs if errs else "none")
    b.close()
