"""Browser acceptance checks against the built output, without external requests.

Uses Playwright request fulfillment to serve the exact dist files in a test origin.
The browser still requires OS socket permissions. A launch failure is a failure,
never reported as a passing check. Run on a normal workstation or GitHub Actions.
"""
import argparse,json,mimetypes,os
from pathlib import Path
from urllib.parse import urlsplit,unquote
from playwright.sync_api import sync_playwright,expect
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'dist';EVIDENCE=ROOT/'evidence';EVIDENCE.mkdir(exist_ok=True)
ORIGIN='http://knowledge.test'

def main(intro_only=False):
    errors=[];missing=[];checks=[]
    def serve(route):
        req=urlsplit(route.request.url)
        if req.hostname!='knowledge.test':route.abort();return
        target=OUT/unquote(req.path).lstrip('/')
        if target.is_dir():target=target/'index.html'
        if not target.is_file():missing.append(req.path);route.fulfill(status=404,body='Not found');return
        route.fulfill(status=200,content_type=mimetypes.guess_type(str(target))[0] or 'application/octet-stream',body=target.read_bytes())
    with sync_playwright() as p:
        options={'headless':True}
        if os.environ.get('BROWSER_EXECUTABLE'):options['executable_path']=os.environ['BROWSER_EXECUTABLE']
        browser=p.chromium.launch(**options)
        context=browser.new_context(viewport={'width':1440,'height':1000},reduced_motion='reduce')
        context.route('**/*',serve);page=context.new_page();page.on('pageerror',lambda error:errors.append(str(error)))
        if not intro_only:
            paths=['/','/en/','/skills/','/knowledge/','/knowledge/ai/','/knowledge/ai/computer-vision/','/knowledge/ai/families/diffusion/','/knowledge/ai/confluence/','/knowledge/nodes/dit/','/knowledge/algorithms/','/knowledge/algorithms/binary-search/','/en/knowledge/algorithms/binary-search/','/knowledge/infra/','/demo/article/']
            for width in [375,768,1440]:
                page.set_viewport_size({'width':width,'height':1000})
                for path in paths:
                    page.goto(ORIGIN+path);page.wait_for_load_state('networkidle')
                    expect(page.locator('h1')).to_be_visible()
                    assert page.evaluate('document.documentElement.scrollWidth <= innerWidth + 1'),f'Horizontal overflow: {width} {path}'
                page.goto(ORIGIN+'/en/');page.screenshot(path=str(EVIDENCE/f'home-en-{width}.png'),full_page=True)
                checks.append(f'{width}px: {len(paths)} pages, no horizontal overflow')
            page.set_viewport_size({'width':1440,'height':1000})
            page.goto(ORIGIN+'/notes/ai/')
            page.locator('#language-switch').click()
            expect(page.locator('html')).to_have_attribute('lang','en')
            expect(page.locator('.notes-dock a[aria-current]')).to_have_attribute('data-notebook','ai')
            page.keyboard.press('/');expect(page.locator('#search-dialog')).to_be_visible();page.locator('#global-search').fill('变分自编码器');expect(page.locator('#search-results a').first).to_be_visible();page.keyboard.press('Escape');expect(page.locator('#search-dialog')).to_be_hidden()
            page.locator('#theme-toggle').click();expect(page.locator('html')).to_have_attribute('data-theme','light');page.reload();expect(page.locator('html')).to_have_attribute('data-theme','light')
            checks.append('Keyboard search/Escape and persisted theme')
            page.goto(ORIGIN+'/knowledge/algorithms/?view=course&q=006');expect(page.locator('[data-panel=course] [data-filter-item]:visible')).to_have_count(1)
            page.locator('[data-panel=course] [data-return-link]:visible').click();assert '/binary-search/' in page.url;page.locator('[data-back]').first.click();assert 'q=006' in page.url
            checks.append('Course number search and stable algorithm article URLs')
            page.goto(ORIGIN+'/');expect(page.locator('#intro')).to_be_hidden();checks.append('Reduced-motion intro bypass')
            nojs=browser.new_context(java_script_enabled=False,viewport={'width':375,'height':850});nojs.route('**/*',serve);static=nojs.new_page();static.goto(ORIGIN+'/knowledge/nodes/dit/');expect(static.locator('h1')).to_have_text('DiT');nojs.close();checks.append('No-JavaScript deep page readability')
        for width in [375,768,1440]:
            plain=browser.new_context(reduced_motion='no-preference',viewport={'width':width,'height':850})
            plain.route('**/*',serve);intro=plain.new_page();intro.on('pageerror',lambda error:errors.append(str(error)))
            intro.clock.install(time=0);intro.clock.pause_at(10000)
            intro.goto(ORIGIN+'/');expect(intro.locator('#intro')).to_be_visible()
            dimensions=intro.locator('#intro').evaluate('(el)=>{const r=el.getBoundingClientRect(),s=getComputedStyle(el);return {x:r.x,y:r.y,w:r.width,h:r.height,bg:s.backgroundColor,radius:s.borderRadius,font:s.fontSize}}')
            assert dimensions=={'x':0,'y':0,'w':width,'h':850,'bg':'rgb(0, 0, 0)','radius':'0px','font':'18px' if width<=600 else '22px'},dimensions
            block=intro.locator('.intro-body').bounding_box()
            assert abs(block['x']+block['width']/2-width/2)<1
            assert abs(block['y']+block['height']/2-425)<1
            def advance_until(predicate,limit=20000):
                elapsed=0
                while not predicate():
                    assert elapsed<limit, 'Intro did not reach expected state'
                    intro.clock.run_for(50);elapsed+=50
            def stage(name):
                advance_until(lambda:intro.locator('#intro').get_attribute('data-stage')==name)
            def capture(name):
                # Repaint after terminal clearing for reliable headless screenshots.
                intro.set_viewport_size({'width':width+1,'height':850})
                intro.set_viewport_size({'width':width,'height':850})
                intro.screenshot(path=str(EVIDENCE/f'{name}-{width}.png'))
            expect(intro.locator('#intro')).to_have_attribute('data-stage','ssh')
            intro.clock.run_for(260);expect(intro.locator('.shell-input')).to_have_text('s')
            assert intro.locator('.shell-line > .terminal-cursor').count()==1
            stage('connecting')
            expect(intro.locator('.shell-input')).to_have_text('ssh river_ya@192.0.2.24')
            expect(intro.locator('#intro-script')).to_contain_text('Connecting to 192.0.2.24...')
            expect(intro.locator('.shell-pixel-art')).to_have_count(0)
            stage('welcome')
            expect(intro.locator('#intro-script')).to_contain_text('Connection established.')
            expect(intro.locator('.shell-welcome')).to_contain_text('奶龙')
            art=intro.locator('.shell-pixel-art').inner_text()
            assert len(art.splitlines())==40 and set(art)<=set(' ▀▄█\n')
            expect(intro.locator('.shell-pixel-art')).to_be_visible()
            assert intro.locator('#intro img, #intro canvas, #intro svg').count()==0
            assert intro.locator('#intro').evaluate('el=>el.scrollWidth<=el.clientWidth')
            artbox=intro.locator('.shell-pixel-art').bounding_box()
            assert artbox['x']>=0 and artbox['x']+artbox['width']<=width
            assert artbox['y']>=0 and artbox['y']+artbox['height']<780
            capture('intro-workspace')
            intro.clock.run_for(2500)
            expect(intro.locator('.shell-pixel-art')).to_be_visible()
            expect(intro.locator('.shell-input')).to_have_count(1)
            stage('clearing')
            expect(intro.locator('#intro-script')).to_have_text('')
            expect(intro.locator('#intro')).to_be_visible()
            stage('server')
            expect(intro.locator('.shell-line')).to_have_text('river_ya@knowledge:~/knowledge$ ')
            intro.clock.run_for(260);expect(intro.locator('.shell-input')).to_have_text('n')
            advance_until(lambda:'Server starting...' in intro.locator('#intro-script').inner_text())
            expect(intro.locator('.shell-input')).to_have_text('npm run start')
            assert 'Server listening' not in intro.locator('#intro-script').inner_text()
            advance_until(lambda:'Server listening' in intro.locator('#intro-script').inner_text())
            expect(intro.locator('#intro-script')).to_contain_text('Server listening on http://localhost:5173')
            capture('intro')
            stage('shattering')
            expect(intro.locator('.terminal-shatter')).to_have_count(1)
            expect(intro.locator('.terminal-shard')).to_have_count(18 if width<600 else 30)
            expect(intro.locator('#intro-script')).to_have_count(1)
            assert intro.locator('.terminal-shard').first.inner_text().find('npm run start')>=0
            assert intro.locator('#intro').evaluate("el=>getComputedStyle(el).backgroundColor==='rgba(0, 0, 0, 0)'")
            intro.clock.run_for(1550);expect(intro.locator('#intro')).to_be_hidden()
            expect(intro.locator('.terminal-shatter')).to_have_count(0)
            intro.clock.run_for(1400)
            expect(intro.locator('.hero-copy h1')).to_have_class('is-revealed')
            expect(intro.locator('.notes-dock')).to_have_class('notes-dock is-revealed')
            # Reveal the lower modules when they enter the viewport.
            intro.locator('.shelf').scroll_into_view_if_needed()
            intro.clock.run_for(1400)
            expect(intro.locator('.shelf')).to_have_class('shelf is-revealed')
            intro.evaluate('scrollTo({top:0,behavior:"instant"})')
            assert not intro.locator('html').evaluate("el=>el.classList.contains('intro-open')")
            intro.locator('#replay').click();expect(intro.locator('#intro')).to_be_visible()
            intro.keyboard.press('Escape');expect(intro.locator('#intro')).to_be_hidden()
            expect(intro.locator('#replay')).to_be_focused()
            stopped=intro.locator('#intro-script').inner_text();intro.clock.run_for(20000)
            assert intro.locator('#intro-script').inner_text()==stopped
            intro.reload();expect(intro.locator('#intro')).to_be_hidden()
            for target in ['connecting','welcome','clearing','server','shattering']:
                intro.locator('#replay').click();stage(target)
                intro.locator('#skip-intro').click();expect(intro.locator('#intro')).to_be_hidden()
                stopped=intro.locator('#intro-script').inner_text();intro.clock.run_for(20000)
                assert intro.locator('#intro-script').inner_text()==stopped
            intro.locator('#replay').click();stage('welcome')
            intro.reload();expect(intro.locator('#intro')).to_be_hidden()
            intro.goto(ORIGIN+'/en/');expect(intro.locator('#intro')).to_be_hidden()
            intro.locator('#replay').click();stage('welcome')
            expect(intro.locator('.shell-welcome')).to_have_text('[ Welcome ]  Nailong welcomes you, river_ya!')
            stage('shattering')
            intro.emulate_media(reduced_motion='reduce')
            expect(intro.locator('#intro')).to_be_hidden()
            expect(intro.locator('.terminal-shatter')).to_have_count(0)
            assert intro.locator('.hero-copy h1').evaluate("el=>getComputedStyle(el).opacity==='1'")
            plain.close()
        checks.append('375/768/1440px intro: full viewport, centered larger text, pure black, SSH/connection/Nailong Unicode art/clear/npm startup sequence, river_ya login identity, faster command-only typing, inline cursor, falling terminal shards, staggered/scroll-triggered homepage entry, auto close, replay, Escape/skip, focus restoration and session suppression')
        reduced=browser.new_context(reduced_motion='reduce');reduced.route('**/*',serve)
        rp=reduced.new_page();rp.goto(ORIGIN+'/')
        expect(rp.locator('#intro')).to_be_hidden()
        assert rp.locator('.hero-copy h1').evaluate("el=>getComputedStyle(el).opacity==='1'")
        expect(rp.locator('.terminal-shatter')).to_have_count(0)
        reduced.close()
        readable=browser.new_context(java_script_enabled=False);readable.route('**/*',serve)
        readable_page=readable.new_page();readable_page.goto(ORIGIN+'/')
        expect(readable_page.locator('.hero-copy h1')).to_be_visible()
        assert readable_page.locator('.hero-copy h1').evaluate("el=>getComputedStyle(el).opacity==='1'")
        readable.close();checks.append('Homepage remains readable with reduced motion or JavaScript disabled')
        blocked=browser.new_context();blocked.route('**/*',serve);blocked.add_init_script("Object.defineProperty(window,'localStorage',{get(){throw new Error('storage blocked')}});Object.defineProperty(window,'sessionStorage',{get(){throw new Error('storage blocked')}})")
        blocked_page=blocked.new_page();blocked_page.on('pageerror',lambda error:errors.append(str(error)));blocked_page.goto(ORIGIN+'/');expect(blocked_page.locator('h1')).to_be_visible();expect(blocked_page.locator('#intro')).to_be_hidden();blocked.close();checks.append('Storage-unavailable graceful fallback')
        context.close();browser.close()
    report={'status':'passed' if not errors and not missing else 'failed','checks':checks,'pageErrors':errors,'missingAssets':missing}
    (EVIDENCE/('intro-results.json' if intro_only else 'browser-results.json')).write_text(json.dumps(report,ensure_ascii=False,indent=2))
    assert not errors and not missing,report
    print(json.dumps(report,ensure_ascii=False,indent=2))

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--intro-only',action='store_true',help='Run only terminal intro and storage fallback checks')
    main(parser.parse_args().intro_only)
