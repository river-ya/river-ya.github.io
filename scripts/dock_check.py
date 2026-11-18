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
            page.close()
        browser.close()
        server.shutdown()
    print('Notes Dock, responsive layouts and retired timeline bookmarks passed.')


if __name__ == '__main__':
    main()
