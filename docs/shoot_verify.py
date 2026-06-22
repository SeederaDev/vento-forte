import time
from pathlib import Path
from playwright.sync_api import sync_playwright
OUT = Path("docs/clone-shots"); OUT.mkdir(parents=True, exist_ok=True)
URL = "http://localhost:8777/index.html"
def scroll(pg):
    h=pg.evaluate("document.body.scrollHeight"); y=0
    while y<h:
        pg.evaluate(f"window.scrollTo(0,{y})"); time.sleep(0.2); y+=600
        h=pg.evaluate("document.body.scrollHeight")
    pg.evaluate("window.scrollTo(0,0)"); time.sleep(0.6)
with sync_playwright() as p:
    b=p.chromium.launch()
    # desktop services + access detail
    pg=b.new_page(viewport={"width":1440,"height":900})
    pg.add_init_script("try{sessionStorage.setItem('cp_popup_closed','1')}catch(e){}")
    pg.goto(URL, wait_until="networkidle", timeout=60000); scroll(pg)
    pg.evaluate("document.querySelector('.services').scrollIntoView()"); time.sleep(0.6)
    pg.screenshot(path=str(OUT/"v-services.png"))
    pg.evaluate("document.querySelector('.access').scrollIntoView()"); time.sleep(0.6)
    pg.screenshot(path=str(OUT/"v-access.png"))
    pg.close()
    # mobile full
    m=b.new_page(viewport={"width":390,"height":844}, device_scale_factor=1)
    m.add_init_script("try{sessionStorage.setItem('cp_popup_closed','1')}catch(e){}")
    m.goto(URL, wait_until="networkidle", timeout=60000); scroll(m)
    m.screenshot(path=str(OUT/"mobile-full.png"), full_page=True)
    print("done")
    b.close()
