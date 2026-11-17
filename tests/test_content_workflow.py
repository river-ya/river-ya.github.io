"""Integration tests for authoring and static routing, using isolated temporary content."""
import json,shutil,subprocess,sys,tempfile,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

class ContentWorkflow(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(prefix='knowledge-workflow-')
        self.root=Path(self.temp.name)
        for folder in ['scripts','templates','static','data','content']:
            shutil.copytree(ROOT/folder,self.root/folder,ignore=shutil.ignore_patterns('__pycache__'))
    def tearDown(self):self.temp.cleanup()
    def read(self,name):return json.loads((self.root/'data'/f'{name}.json').read_text())
    def write(self,name,value):(self.root/'data'/f'{name}.json').write_text(json.dumps(value,ensure_ascii=False))
    def run_script(self,script,*args):return subprocess.run([sys.executable,'scripts/'+script,*args],cwd=self.root,capture_output=True,text=True)
    def article(self,locale='zh-CN',slug='test-note',status='published'):
        file='content/test.'+locale+'.md';(self.root/file).write_text('# A real fixture\n\nBody supplied by the test, not seed content.\n')
        return dict(slug=slug,translationKey='test-note',locale=locale,title='测试笔记' if locale=='zh-CN' else 'Test note',summary='Fixture summary',status=status,publishedAt='2026-10-22',file=file,nodeIds=['dit'],tags=['test'])
    def build(self):
        result=self.run_script('build.py');self.assertEqual(result.returncode,0,result.stdout+result.stderr)
    def test_publication_updates_route_and_keeps_original_language(self):
        self.write('articles',[self.article()]);self.build()
        node=(self.root/'dist/knowledge/nodes/dit/index.html').read_text()
        self.assertIn('/blog/test-note/',node)
        self.assertIn('测试笔记',(self.root/'dist/index.html').read_text())
        self.assertIn('English translation is not available yet',(self.root/'dist/en/index.html').read_text())
        index=json.loads((self.root/'dist/assets/search.en.json').read_text())
        result=next(x for x in index if x['title']=='测试笔记');self.assertEqual(result['url'],'/blog/test-note/');self.assertEqual(result['contentLocale'],'zh-CN')
        self.assertFalse((self.root/'dist/en/blog/test-note/index.html').exists())
        self.assertIn('阅读笔记',(self.root/'dist/knowledge/ai/families/diffusion/index.html').read_text())
        self.assertIn('/blog/test-note/?translation=unavailable',(self.root/'dist/blog/test-note/index.html').read_text())
    def test_drafts_never_get_article_routes_or_search_entries(self):
        self.write('articles',[self.article(status='draft')]);self.build()
        self.assertFalse((self.root/'dist/blog/test-note/index.html').exists())
        self.assertNotIn('test-note',(self.root/'dist/assets/search.zh-CN.json').read_text())
        self.assertNotIn('test-note',(self.root/'dist/sitemap.xml').read_text())
    def test_translation_with_a_different_slug_has_real_alternate(self):
        self.write('articles',[self.article(),self.article('en','english-note')]);self.build()
        doc=(self.root/'dist/blog/test-note/index.html').read_text()
        self.assertIn('hreflang="en" href="https://river-ya.github.io/en/blog/english-note/"',doc)
        result=self.run_script('validate.py','--output');self.assertEqual(result.returncode,0,result.stdout+result.stderr)
    def test_algorithm_body_keeps_canonical_and_has_translation_fallback(self):
        topics=self.read('algorithms');topic=next(x for x in topics if x['id']=='binary-search')
        topic['mainContentFiles']['zh-CN']='content/binary-search.zh.md';topic['contentStatus']='published'
        (self.root/'content/binary-search.zh.md').write_text('## 核心思想\n\n只用于自动测试的正文。\n');self.write('algorithms',topics);self.build()
        self.assertIn('id="核心思想"',(self.root/'dist/knowledge/algorithms/binary-search/index.html').read_text())
        en=(self.root/'dist/en/knowledge/algorithms/binary-search/index.html').read_text();self.assertIn('English translation is not available yet',en)
        self.assertNotIn('只用于自动测试的正文',en)
    def test_blog_indexes_only_published_posts_and_counts_translations_once(self):
        zh=self.article();zh['tags']=['AI / 实验','C++']
        en=self.article('en','english-note');en['tags']=['AI / 实验','C++']
        older=self.article(slug='older-note');older['translationKey']='older';older['publishedAt']='2025-05-01'
        draft=self.article(slug='private-draft',status='draft');draft['translationKey']='private'
        draft['title']='PRIVATE DRAFT'
        self.write('articles',[older,zh,en,draft]);self.build()
        blog=(self.root/'dist/blog/index.html').read_text()
        self.assertIn('/blog/test-note/',blog);self.assertIn('/blog/older-note/',blog)
        self.assertNotIn('PRIVATE DRAFT',blog);self.assertNotIn('/en/blog/english-note/',blog)
        self.assertLess(blog.index('/blog/test-note/'),blog.index('/blog/older-note/'))
        archive=(self.root/'dist/blog/archive/index.html').read_text()
        self.assertLess(archive.index('2026 <small>'),archive.index('2025 <small>'))
        self.assertIn('C%2B%2B',(self.root/'dist/blog/tags/index.html').read_text())
        english=(self.root/'dist/en/blog/index.html').read_text()
        self.assertIn('/en/blog/english-note/',english);self.assertIn('/blog/older-note/',english)
        self.assertIn('Original language',english)
        doc=(self.root/'dist/blog/test-note/index.html').read_text()
        self.assertIn('返回博客',doc);self.assertIn('href="/blog/"',doc)
        result=self.run_script('validate.py','--output');self.assertEqual(result.returncode,0,result.stdout+result.stderr)
    def test_reserved_blog_slug_is_rejected(self):
        self.write('articles',[self.article(slug='archive')])
        result=self.run_script('validate.py');self.assertNotEqual(result.returncode,0)
        self.assertIn('reserved blog slug',result.stderr)

    def test_prerequisite_cycle_is_rejected(self):
        nodes=self.read('nodes');next(n for n in nodes if n['id']=='ddpm')['prerequisiteIds']=['dit'];self.write('nodes',nodes)
        result=self.run_script('validate.py');self.assertNotEqual(result.returncode,0);self.assertIn('Cycle',result.stderr)
    def test_broken_lesson_mapping_is_rejected(self):
        topics=self.read('algorithms');topics[0]['lessonIds']=['999'];self.write('algorithms',topics)
        result=self.run_script('validate.py');self.assertNotEqual(result.returncode,0);self.assertIn('Invalid course mapping',result.stderr)

if __name__=='__main__':unittest.main()
