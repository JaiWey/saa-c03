import asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--no-sandbox'])
        pg = await b.new_page(viewport={'width':430,'height':900})
        errs=[]
        pg.on('pageerror', lambda e: errs.append(str(e)))
        pg.on('console', lambda m: errs.append(m.text) if m.type=='error' else None)
        await pg.goto('file:///home/claude/work/dist/index.html')
        await pg.screenshot(path='s_home.png', full_page=False)
        # sequential practice: click first mode
        await pg.click('.mode >> nth=0')
        await pg.wait_for_selector('.opt')
        await pg.screenshot(path='s_q1.png')
        await pg.click('.opt[data-l="B"]')   # wrong (answer A)
        await pg.wait_for_selector('.verdict')
        await pg.screenshot(path='s_q1_ans.png', full_page=True)
        # go to Q477 (image options) via search
        await pg.click('#brand')
        await pg.fill('input[type=search]','477')
        await pg.click('.res')
        await pg.wait_for_selector('.opt img')
        await pg.screenshot(path='s_q477.png', full_page=True)
        # multi-select test: search 500
        await pg.click('#brand'); await pg.fill('input[type=search]','500'); await pg.click('.res')
        await pg.click('.opt[data-l="A"]'); await pg.click('.opt[data-l="D"]'); await pg.click('#btnSubmit')
        await pg.wait_for_selector('.verdict.ok')
        # exam
        await pg.click('#brand'); await pg.click('.mode >> nth=5')
        await pg.wait_for_selector('#timer')
        await pg.click('.opt[data-l="A"]')
        await pg.screenshot(path='s_exam.png')
        await pg.click('.navbar .btn >> text=答题卡')
        await pg.screenshot(path='s_nav.png')
        await pg.click('#drClose')
        pg.on('dialog', lambda d: asyncio.ensure_future(d.accept()))
        await pg.click('.navbar .btn >> text=交卷')
        await pg.wait_for_selector('.score')
        await pg.screenshot(path='s_result.png')
        print('errors:', errs)
        # persistence
        n = await pg.evaluate("Object.keys(JSON.parse(localStorage.getItem('saa-c03-practice-v1')).prog).length")
        print('progress entries', n)
        await b.close()
asyncio.run(main())
