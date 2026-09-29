import asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path="/opt/pw-browsers/chromium-1194/chrome-linux/chrome")
        for sc,name in ((1,'capa-facebook-1640x624.png'),(2,'capa-facebook-3280x1248.png')):
            pg=await b.new_page(viewport={'width':1640,'height':624},device_scale_factor=sc)
            await pg.goto('file:///home/user/Designerpacheco/marca/capa-facebook/capa.html',wait_until='networkidle')
            print(await pg.evaluate("document.fonts.ready.then(()=>[...document.fonts].filter(f=>f.status=='loaded').map(f=>f.family+f.weight).join(','))"))
            await pg.screenshot(path=name)
        await b.close()
asyncio.run(main())
