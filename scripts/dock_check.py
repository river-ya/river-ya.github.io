"""Check published notebook navigation and the replacement for retired timelines."""
import os
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Thread
from playwright.sync_api import expect, sync_playwright

ROOT = Path(__file__).resolve().parents[1]


class StaticFiles(SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass


def check_terminal(page, site, prefix):
    page.goto(site+prefix+'/terminal/?cwd=/ai/computer-vision')
    prompt = page.locator('#shell-input')
    log = page.locator('#shell-log')

    def run(text):
        prompt.fill(text)
        prompt.press('Enter')

    expect(page.locator('#shell-path')).to_have_text('/ai/computer-vision')
    active = page.locator('#shell-form .shell-prompt')
    expect(active).to_have_text('river_ya@knowledge:~/ai/computer-vision$')
    expect(log.locator('.shell-command .shell-prompt')).to_have_text(active.inner_text())
    for _ in range(2):
        expect(page.locator('.shell-window')).to_have_css('background-color','rgb(48, 10, 36)')
        expect(active.locator('.prompt-user')).to_have_css('color','rgb(38, 162, 105)')
        expect(active.locator('.prompt-dir')).to_have_css('color','rgb(8, 69, 143)')
        page.locator('#theme-toggle').click()
    assert page.evaluate("""async () => (await document.fonts.load('13pt "Site Ubuntu Mono"')).length > 0""")
    first_note = log.locator('.shell-list a').first
    if first_note.count():
        run('cat '+first_note.inner_text())
        expect(log.locator('.shell-reading div')).not_to_be_empty()
        expect(log.locator('.shell-reading .shell-error')).to_have_count(0)
    run('cd ../..')
    expect(page.locator('#shell-path')).to_have_text('/')
    run('search infra')
    expect(log.locator('button').last).to_have_text('/infra/')
    run('cd /infra')
    page.reload()
    expect(page.locator('#shell-path')).to_have_text('/infra')
    run('open /missing-page')
    expect(log.locator('.shell-error')).to_be_visible()
    prompt.fill('cd /algo')
    prompt.press('Tab')
    expect(prompt).to_have_value('cd /algorithms/')
    prompt.press('Enter')
    expect(page.locator('#shell-path')).to_have_text('/algorithms')
    prompt.press('ArrowUp')
    expect(prompt).to_have_value('cd /algorithms/')
    run('clear')
    expect(log).to_be_empty()
    expect(active).to_have_text('river_ya@knowledge:~/algorithms$')
    assert abs(page.locator('#shell-form').bounding_box()['y'] - page.locator('#shell-screen').bounding_box()['y'] - 8) <= 1
    page.locator('[data-command="help"]').click()
    expect(log).to_contain_text('pwd')
    assert page.evaluate('document.documentElement.scrollWidth<=innerWidth+1')
    run('open /blog')
    page.wait_for_url(site+prefix+'/blog/')


def main():
    handler = partial(StaticFiles, directory=str(ROOT/'dist'))
    with ThreadingHTTPServer(('127.0.0.1', 0), handler) as server, sync_playwright() as playwright:
        Thread(target=server.serve_forever, daemon=True).start()
        site = f'http://127.0.0.1:{server.server_port}'
        browser = playwright.chromium.launch(executable_path=os.getenv('BROWSER_EXECUTABLE'))
        for width, prefix in [(375,''), (768,'/en'), (1440,'')]:
            page = browser.new_page(viewport={'width':width,'height':850},reduced_motion='reduce')
            page.goto(site+prefix+'/')
            home_links = page.locator('.desk-links a')
            expect(home_links).to_have_count(2)
            expect(home_links.nth(0)).to_have_attribute('href', prefix+'/blog/')
            expect(home_links.nth(1)).to_have_attribute('href', prefix+'/terminal/')
            expect(page.locator('.notes-dock a')).to_have_count(3)
            shelf = page.locator('.update-list')
            if shelf.count():
                assert shelf.bounding_box()['x'] + shelf.bounding_box()['width'] < page.locator('.notes-dock').bounding_box()['x']
                dates = shelf.locator('time').all_text_contents()
                assert dates == sorted(dates, reverse=True)
            for category in ['ai','algorithms','infra']:
                page.locator(f'.notes-dock a[data-notebook="{category}"]').click()
                page.wait_for_url(site+prefix+'/blog/category/'+category+'/')
                expect(page.locator('.blog-categories a[aria-current]')).to_have_attribute(
                    'href', prefix+'/blog/category/'+category+'/')
                assert page.evaluate('document.documentElement.scrollWidth<=innerWidth+1')
                page.goto(site+prefix+'/')
            page.goto(site+prefix+'/knowledge/ai/computer-vision/')
            page.wait_for_url('**/blog/category/computer-vision/')
            expect(page.locator('.timeline, .milestones, #graph')).to_have_count(0)
            expect(page.locator('h1')).to_be_visible()
            first = page.locator('.post-card[data-blog-post] h2 a').first
            if first.count():
                first.click()
                expect(page.locator('.article-header')).to_be_visible()
                page.locator('[data-blog-back]').click()
                page.wait_for_url('**/blog/category/computer-vision/')
            check_terminal(page, site, prefix)
            page.close()
        browser.close()
        server.shutdown()
    print('Blog categories, responsive layouts, legacy bookmarks and site terminal passed.')


if __name__ == '__main__':
    main()
