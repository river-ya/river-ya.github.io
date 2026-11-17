"""Blog acceptance: real empty state plus isolated published-content fixtures."""
import json,mimetypes,os,shutil,subprocess,sys,tempfile
from pathlib import Path
from urllib.parse import unquote,urlsplit
from playwright.sync_api import sync_playwright,expect
ROOT=Path(__file__).resolve().parents[1];EVIDENCE=ROOT/'evidence';ORIGIN='http://knowledge.test'

def main():
    EVIDENCE.mkdir(exist_ok=True)
    base=ROOT/'dist';errors=[];missing=[];checks=[]
    def serve(route):
        target=base/unquote(urlsplit(route.request.url).path).lstrip('/')
        if target.is_dir():target=target/'index.html'
        if not target.is_file():missing.append(str(target));route.fulfill(status=404,body='Missing');return
        route.fulfill(content_type=mimetypes.guess_type(str(target))[0] or 'application/octet-stream',body=target.read_bytes())
    with sync_playwright() as p,tempfile.TemporaryDirectory(prefix='knowledge-blog-fixture-') as tmp:
        opts={'headless':True}
        if os.environ.get('BROWSER_EXECUTABLE'):opts['executable_path']=os.environ['BROWSER_EXECUTABLE']
        browser=p.chromium.launch(**opts)
        for width in [375,768,1440]:
            ctx=browser.new_context(viewport={'width':width,'height':1000},reduced_motion='reduce');ctx.route('**/*',serve)
            page=ctx.new_page();page.on('pageerror',lambda e:errors.append(str(e)))
            page.goto(ORIGIN+'/');page.locator('.main-nav a[href="/blog/"]').click()
            expect(page.locator('h1')).to_have_text('把理解，写下来。')
            expect(page.locator('#intro')).to_be_hidden()
            expect(page.locator('.blog-empty')).to_be_visible();expect(page.locator('[data-blog-post]')).to_have_count(0)
            assert page.evaluate('document.documentElement.scrollWidth<=innerWidth+1')
            page.screenshot(path=str(EVIDENCE/f'blog-dark-{width}.png'),full_page=True)
            page.locator('#theme-toggle').click();page.reload();expect(page.locator('html')).to_have_attribute('data-theme','light')
            page.screenshot(path=str(EVIDENCE/f'blog-light-{width}.png'),full_page=True)
            for part in ['archive','tags','search']:
                page.locator(f'.blog-nav a[href="/blog/{part}/"]').click()
                expect(page.locator('h1')).to_be_visible()
                assert page.evaluate('document.documentElement.scrollWidth<=innerWidth+1')
            page.locator('#blog-query').fill('不存在的内容');expect(page.locator('#blog-no-results')).to_be_visible()
            page.locator('#language-switch').click();assert '/en/blog/search/' in page.url
            expect(page.locator('#blog-query')).to_have_value('不存在的内容')
            page.locator('#blog-no-results [data-blog-reset]').click();assert 'q=' not in page.url
            page.goto(ORIGIN+'/demo/article/');page.locator('[data-blog-back]').click();assert page.url==ORIGIN+'/blog/'
            ctx.close();checks.append(f'{width}px: entry links, 4 blog pages, dark/light themes, empty state, language/query preservation, preview return and no overflow')
        fixture=Path(tmp)
        for folder in ['scripts','templates','static','data','content']:
            shutil.copytree(ROOT/folder,fixture/folder,ignore=shutil.ignore_patterns('__pycache__'))
        (fixture/'content/check.md').write_text('## Test content\n\nThis fixture never ships with the website.\n')
        articles=[]
        for slug,title,date,tags,status in [('new-note','Diffusion 实验','2026-11-17',['AI / 实验','C++'],'published'),('old-note','算法笔记','2025-01-03',['算法'],'published'),('secret-note','PRIVATE DRAFT','2026-11-16',['private'],'draft')]:
            articles.append(dict(slug=slug,translationKey=slug,locale='zh-CN',title=title,summary='Only test fixture',publishedAt=date,tags=tags,status=status,file='content/check.md',nodeIds=['dit']))
        (fixture/'data/articles.json').write_text(json.dumps(articles,ensure_ascii=False))
        subprocess.run([sys.executable,'scripts/build.py'],cwd=fixture,check=True,capture_output=True)
        base=fixture/'dist';ctx=browser.new_context(reduced_motion='reduce');ctx.route('**/*',serve);page=ctx.new_page();page.on('pageerror',lambda e:errors.append(str(e)))
        page.goto(ORIGIN+'/blog/')
        expect(page.locator('[data-blog-post]')).to_have_count(2)
        expect(page.locator('[data-blog-post] h2').first).to_contain_text('Diffusion')
        expect(page.locator('body')).not_to_contain_text('PRIVATE DRAFT')
        page.locator('#blog-query').fill('diffusion');expect(page.locator('[data-blog-post]:visible')).to_have_count(1)
        page.locator('[data-blog-post]:visible .blog-tag-list a').filter(has_text='C++').click()
        expect(page.locator('#blog-filter strong')).to_have_text('C++');expect(page.locator('[data-blog-post]:visible')).to_have_count(1)
        page.locator('#blog-filter [data-blog-reset]').click();expect(page.locator('[data-blog-post]:visible')).to_have_count(2)
        page.locator('.blog-nav a[href="/blog/archive/"]').click()
        expect(page.locator('.blog-archive-year h2').first).to_contain_text('2026')
        page.locator('.blog-archive-row').first.click();expect(page.locator('h1')).to_have_text('Diffusion 实验')
        page.locator('[data-blog-back]').click();assert page.url==ORIGIN+'/blog/'
        page.goto(ORIGIN+'/en/blog/');expect(page.locator('[data-blog-post]')).to_have_count(2)
        expect(page.locator('.blog-language').first).to_contain_text('zh-CN')
        page.locator('[data-blog-post] h2 a').first.click();assert '/en/blog/new-note/' not in page.url
        ctx.close();checks.append('Isolated fixtures: newest first, draft exclusion, keyword and encoded-tag filters, reset, archive/year order, article return and real-language fallback')
        ctx=browser.new_context(java_script_enabled=False);ctx.route('**/*',serve);page=ctx.new_page();page.goto(ORIGIN+'/blog/')
        expect(page.locator('[data-blog-post]')).to_have_count(2);expect(page.locator('[data-blog-post] h2 a').first).to_be_visible()
        ctx.close();browser.close();checks.append('Published list remains readable without JavaScript')
    report={'status':'passed' if not errors and not missing else 'failed','checks':checks,'pageErrors':errors,'missingAssets':missing}
    (EVIDENCE/'blog-results.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');assert not errors and not missing,report
    print(json.dumps(report,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
