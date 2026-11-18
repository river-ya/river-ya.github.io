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
    page.locator('.collection-links .terminal-link').click()
    prompt = page.locator('#shell-input')
    log = page.locator('#shell-log')

    def run(text):
        prompt.fill(text)
        prompt.press('Enter')

    expect(page.locator('#shell-path')).to_have_text('/ai/computer-vision')
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
            for category in ['ai','algorithms','infra']:
                link = page.locator(f'[data-notebook="{category}"]')
                link.click()
                expect(link).to_have_attribute('aria-current','true')
                assert page.url == site+prefix+'/notes/'+category+'/'
                panel = page.locator('.shelf').bounding_box()
                dock = page.locator('.notes-dock').bounding_box()
                assert panel['x'] + panel['width'] < dock['x']
                assert page.evaluate('document.documentElement.scrollWidth<=innerWidth+1')
            page.goto(site+prefix+'/knowledge/ai/computer-vision/')
            page.wait_for_url('**/notes/ai/computer-vision/')
            expect(page.locator('.timeline, .milestones, #graph')).to_have_count(0)
            expect(page.locator('h1')).to_be_visible()
            first = page.locator('.shelf-entry h3 a').first
            if first.count():
                first.click()
                expect(page.locator('.article-header')).to_be_visible()
                page.locator('[data-blog-back]').click()
                page.wait_for_url('**/notes/ai/computer-vision/')
            check_terminal(page, site, prefix)
            page.close()
        browser.close()
        server.shutdown()
    print('Notes Dock, responsive layouts, retired bookmarks and site terminal passed.')


if __name__ == '__main__':
    main()
