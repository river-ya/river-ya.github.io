"""Render AI timelines and verify interaction, chronology and progressive enhancement."""
import json,os,mimetypes
from urllib.parse import urlsplit,unquote
from browser_check import ROOT,OUT,EVIDENCE,ORIGIN
from playwright.sync_api import sync_playwright,expect

def main():
    errors=[];missing=[];checks=[]
    def serve(route):
        path=OUT/unquote(urlsplit(route.request.url).path).lstrip('/')
        if path.is_dir():path=path/'index.html'
        if not path.is_file():missing.append(str(path));route.fulfill(status=404,body='Missing');return
        route.fulfill(content_type=mimetypes.guess_type(str(path))[0] or 'application/octet-stream',body=path.read_bytes())
    with sync_playwright() as p:
        options={'headless':True}
        if os.environ.get('BROWSER_EXECUTABLE'):options['executable_path']=os.environ['BROWSER_EXECUTABLE']
        browser=p.chromium.launch(**options)
        for width in [375,768,1440]:
            context=browser.new_context(viewport={'width':width,'height':1000},reduced_motion='no-preference')
            context.route('**/*',serve);page=context.new_page();page.on('pageerror',lambda e:errors.append(str(e)))
            page.goto(ORIGIN+'/knowledge/ai/computer-vision/')
            items=page.locator('[data-panel=history] .timeline-node')
            dates=items.locator('.node-meta time').evaluate_all('(els)=>els.map(el=>el.dateTime)')
            assert dates==sorted(dates),dates
            expect(items).to_have_count(13)
            first=items.first;card=first.locator('.timeline-card')
            first.evaluate("el=>el.scrollIntoView({block:'center',behavior:'instant'})")
            page.wait_for_timeout(800)
            assert page.evaluate('document.documentElement.scrollWidth<=innerWidth+1')
            assert page.locator('[data-panel=history] .timeline-progress').evaluate('el=>el.getBoundingClientRect().height')>0
            page.screenshot(path=str(EVIDENCE/f'ai-timeline-{width}.png'))
            if width==1440:
                before=card.bounding_box();card.hover();page.wait_for_timeout(350);after=card.bounding_box()
                assert after['width']>before['width']*1.01,(before,after)
                expect(first).to_have_class('timeline-node is-current')
                year=first.get_attribute('data-year')
                expect(page.locator(f'[data-year-jump="{year}"]')).to_have_attribute('aria-current','date')
                page.screenshot(path=str(EVIDENCE/'ai-timeline-hover.png'))
            first.locator('a.node-link').focus();expect(first.locator('a.node-link')).to_be_focused()
            page.locator('input[name=q]').fill('1506.01497')
            expect(page.locator('[data-panel=history] .timeline-node:visible')).to_have_count(1)
            page.wait_for_timeout(100)
            assert page.locator('[data-year-jump][aria-disabled=false]').count()==1
            page.locator('[data-view=learning]').click()
            expect(page.locator('[data-panel=learning] .timeline-node:visible')).to_have_count(1)
            page.locator('#language-switch').click();assert '/en/' in page.url and 'q=1506.01497' in page.url
            page.locator('[data-panel=learning] a.node-link:visible').click()
            expect(page.locator('h1')).to_contain_text('Faster R-CNN')
            page.locator('[data-back]').first.click();assert 'q=1506.01497' in page.url
            page.locator('.filters [data-reset]').click()
            page.locator('[data-view=history]').click()
            group=page.locator('[data-panel=history] details').first
            group.locator('summary').click();expect(group).not_to_have_attribute('open','')
            group.locator('summary').click();expect(group).to_have_attribute('open','')
            page.locator('#theme-toggle').click();expect(page.locator('html')).to_have_attribute('data-theme','light')
            page.locator('[data-panel=history] .timeline-node').first.evaluate("el=>el.scrollIntoView({block:'center',behavior:'instant'})")
            page.wait_for_timeout(700);page.screenshot(path=str(EVIDENCE/f'ai-timeline-light-{width}.png'))
            assert page.evaluate('document.documentElement.scrollWidth<=innerWidth+1')
            page.goto(ORIGIN+'/knowledge/ai/')
            milestones=page.locator('.milestones');milestones.scroll_into_view_if_needed();page.wait_for_timeout(1400)
            expect(milestones).to_have_class('milestones timeline-in-view')
            expect(milestones.locator('a')).to_have_count(6)
            assert page.evaluate('document.documentElement.scrollWidth<=innerWidth+1')
            page.screenshot(path=str(EVIDENCE/f'ai-milestones-{width}.png'))
            checks.append(f'{width}px: chronology, connected spine, progress, hover/focus, filtering, view/language/return state, collapse, light theme and overview milestones')
            context.close()
        context=browser.new_context(reduced_motion='reduce');context.route('**/*',serve)
        page=context.new_page();page.goto(ORIGIN+'/knowledge/ai/families/diffusion/')
        card=page.locator('[data-panel=history] .timeline-card').first;card.hover()
        assert card.evaluate("el=>getComputedStyle(el).transform==='none'")
        assert page.locator('[data-panel=history] .timeline-node').evaluate_all('els=>els.every(el=>el.getAnimations().length===0)')
        context.close()
        context=browser.new_context(java_script_enabled=False);context.route('**/*',serve)
        page=context.new_page();page.goto(ORIGIN+'/knowledge/ai/computer-vision/')
        expect(page.locator('[data-panel=history] .timeline-node').first).to_be_visible()
        expect(page.locator('[data-panel=history] .timeline-node')).to_have_count(13)
        context.close();browser.close()
        checks.append('Reduced motion disables zoom/entry; chronology remains readable without JavaScript')
    report={'status':'passed' if not errors and not missing else 'failed','checks':checks,'pageErrors':errors,'missingAssets':missing}
    (EVIDENCE/'timeline-results.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    assert not errors and not missing,report
    print(json.dumps(report,ensure_ascii=False,indent=2))

if __name__=='__main__':main()
