from pathlib import Path
from tempfile import TemporaryDirectory
import xml.etree.ElementTree as ET
from playwright.sync_api import sync_playwright
with sync_playwright() as p, TemporaryDirectory() as tmp:
    browser=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox'])
    page=browser.new_page(accept_downloads=True)
    errors=[]
    page.on('pageerror',lambda e:errors.append(str(e)))
    page.goto('http://127.0.0.1:18765/')
    assert page.locator('#download').is_disabled()
    page.keyboard.press('ArrowRight')
    assert page.locator('.frame').count()==0
    for kind in ['walk','wave','jump']:
        page.locator('[data-kind='+kind+']').click()
        page.locator('#make').click()
        assert page.locator('.frame').count()==8
        assert page.locator('#download').is_enabled()
        page.locator('body').click(position={'x':1,'y':1})
        page.keyboard.press('ArrowLeft')
        assert page.locator('.frame.on').get_attribute('data-i')=='7'
        page.keyboard.press('ArrowRight')
        assert page.locator('.frame.on').get_attribute('data-i')=='0'
        page.keyboard.press('ArrowRight')
        assert page.locator('.frame.on').get_attribute('data-i')=='1'
        expected=page.evaluate('frames[now]')
        with page.expect_download() as info:
            page.locator('#download').click()
        download=info.value
        assert download.suggested_filename=='parapara-frame-2.svg'
        dest=Path(tmp)/download.suggested_filename
        download.save_as(dest)
        assert dest.read_text()==expected
        assert ET.fromstring(dest.read_text()).tag=='{http://www.w3.org/2000/svg}svg'
    page.locator('body').click(position={'x':1,'y':1})
    page.keyboard.press('Space')
    page.wait_for_function('timer !== null && timer !== undefined')
    page.keyboard.press('Space')
    assert page.evaluate('timer === null')
    page.locator('#speed').focus()
    before=page.evaluate('now')
    page.keyboard.press('ArrowRight')
    assert page.evaluate('now')==before
    page.locator('#next').focus()
    before=page.evaluate('now')
    page.keyboard.press('Space')
    assert page.evaluate('now')==(before+1)%8
    assert page.evaluate('timer === null')
    page.locator('body').click(position={'x':1,'y':1})
    before=page.evaluate('now')
    page.keyboard.press('Control+ArrowRight')
    assert page.evaluate('now')==before
    page.locator('#play').click()
    page.wait_for_function('timer !== null')
    page.locator('#make').click()
    assert page.evaluate('timer === null && now === 0')
    assert page.locator('#download').is_enabled()
    page.set_viewport_size({'width':375,'height':812})
    assert page.evaluate('document.documentElement.scrollWidth <= innerWidth')
    assert not errors,errors
    browser.close()
print('PASS: 3 motions, SVG downloads match selected frame, keyboard wrap/play/stop, input/button/modifier guards, regeneration, mobile layout, no JS errors')
