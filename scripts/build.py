"""Deterministic static renderer: JSON content + Jinja + Markdown -> dist/.

No runtime Python/Node server, database, or SPA fallback is required.
"""
from __future__ import annotations
import json, re, shutil, sys, html, math
from functools import lru_cache
from pathlib import Path
from collections import defaultdict
from datetime import date
from jinja2 import Environment, FileSystemLoader, select_autoescape
from markupsafe import Markup
from markdown_it import MarkdownIt
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter
from i18n import UI

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'dist'
ORIGIN='https://river-ya.github.io'
def read(name):return json.loads((ROOT/'data'/f'{name}.json').read_text())
DATA={name:read(name) for name in ['nodes','tracks','relations','confluences','profile','articles','algorithms','lessons','categories']}
NODES={n['id']:n for n in DATA['nodes']}
TRACKS={t['id']:t for t in DATA['tracks']}
TOPICS={t['id']:t for t in DATA['algorithms']}
LESSONS={t['id']:t for t in DATA['lessons']}
INFRA=[
 {'id':'systems','title':{'zh-CN':'系统与网络','en':'Systems & networking'},'description':{'zh-CN':'Linux · 网络 · 操作系统 · 计算机体系结构','en':'Linux · Networking · Operating systems · Computer architecture'}},
 {'id':'environments','title':{'zh-CN':'环境与部署','en':'Environments & deployment'},'description':{'zh-CN':'开发环境 · 容器 · 部署 · 可观测性','en':'Development environments · Containers · Deployment · Observability'}},
 {'id':'data','title':{'zh-CN':'数据基础设施','en':'Data infrastructure'},'description':{'zh-CN':'数据处理 · 存储 · 数据流水线','en':'Data processing · Storage · Data pipelines'}},
 {'id':'compute','title':{'zh-CN':'AI 计算与性能','en':'AI compute & performance'},'description':{'zh-CN':'GPU · CUDA · 分布式训练 · 推理服务 · 性能优化','en':'GPU · CUDA · Distributed training · Inference · Performance'}},
 {'id':'experiments','title':{'zh-CN':'实验与复现','en':'Experiments & reproducibility'},'description':{'zh-CN':'实验管理 · 模型评测 · 工程复现','en':'Experiment tracking · Model evaluation · Reproducibility'}}]

def url(path,locale):return ('/en' if locale=='en' else '')+'/'+path.strip('/')+('/' if path.strip('/') else '')
def track_path(t):return '/knowledge/ai/'+('families/' if t['kind']=='family' else '')+t['id']+'/'
def node_date(n):return n['dates'][n.get('timelineDateIndex',0)] if n['dates'] else {'value':'','event':'preprint'}
def date_sort(n):return (node_date(n)['value'].ljust(10,'0'),n['id'])
def published(locale=None):return [a for a in DATA['articles'] if a['status']=='published' and not a.get('demo') and (locale is None or a['locale']==locale)]
def preferred_articles(locale, items=None):
    versions={}
    for a in items if items is not None else published():
        if a['translationKey'] not in versions or a['locale']==locale:versions[a['translationKey']]=a
    return list(versions.values())
SHELF_TAGS = {
    'ai': {'ai', '人工智能', '机器学习', 'deep learning', 'machine learning'},
    'algorithms': {'算法', 'algorithm', 'algorithms'},
    'infra': {'infra', 'infrastructure', '基础设施'},
}
VISION_TAGS = {'计算机视觉', 'computer vision', 'computer-vision', 'cv'}


def notebook_entries(locale):
    """Index actual publications, merging translations and their topic links."""
    topics_by_work = defaultdict(set)
    algorithm_posts = {slug for t in TOPICS.values() for slug in t['relatedArticleSlugs']}
    vision_nodes = set(TRACKS['computer-vision']['learningOrder'])
    for article in published():
        groups = topics_by_work[article['translationKey']]
        tags = {part.strip().casefold() for tag in article['tags'] for part in tag.split('/')}
        groups.update(key for key, names in SHELF_TAGS.items() if names & tags)
        if article['nodeIds']:
            groups.add('ai')
        if vision_nodes.intersection(article['nodeIds']) or VISION_TAGS & tags:
            groups.update(('ai', 'computer-vision'))
        if article['slug'] in algorithm_posts:
            groups.add('algorithms')

    notes = []
    for a in preferred_articles(locale):
        notes.append(dict(title=a['title'], summary=a['summary'], lang=a['locale'],
                          url=url('/blog/'+a['slug']+'/', a['locale']),
                          date=a.get('updatedAt') or a['publishedAt'],
                          groups=topics_by_work[a['translationKey']]))
    for topic in TOPICS.values():
        versions = topic['mainContentFiles']
        if topic['contentStatus'] != 'published' or not versions:
            continue
        lang = locale if locale in versions else next(iter(versions))
        notes.append(dict(title=topic['title'][lang], summary=topic['summary'][lang], lang=lang,
                          url=url('/knowledge/algorithms/'+topic['slug']+'/', lang),
                          date=topic.get('updatedAt') or topic.get('publishedAt', ''),
                          groups={'algorithms'}))
    return sorted(notes, key=lambda entry: (entry['date'], entry['url']), reverse=True)


@lru_cache(maxsize=None)
def reading_minutes(file):
    text=(ROOT/file).read_text()
    chinese=len(re.findall(r'[\u4e00-\u9fff]',text))
    words=len(re.findall(r'[a-zA-Z0-9]+',text))
    return max(1,math.ceil(chinese/400+words/220))

def code_highlight(code,lang,*args):
    try:return highlight(code,get_lexer_by_name(lang or 'text'),HtmlFormatter())
    except Exception:return '<pre><code>'+html.escape(code)+'</code></pre>'
MD=MarkdownIt('commonmark',{'html':True,'highlight':code_highlight}).enable('table')
def markdown_file(file):
    if not file:return '',[]
    path=(ROOT/file).resolve()
    if not path.is_relative_to(ROOT/'content'):raise ValueError('Content file must be under content/')
    text=path.read_text();tokens=MD.parse(text);toc=[];counts=defaultdict(int)
    # The page title owns h1; pasted Markdown with a title must not create a second h1.
    if any(t.type=='heading_open' and t.tag=='h1' for t in tokens):
        for t in tokens:
            if t.type in ['heading_open','heading_close']:t.tag='h'+str(min(6,int(t.tag[1])+1))
    for i,token in enumerate(tokens):
        if token.type=='heading_open':
            label=tokens[i+1].content
            slug=re.sub(r'[^\w\-]+','-',label.lower()).strip('-') or 'section'
            counts[slug]+=1
            if counts[slug]>1:slug+='-'+str(counts[slug])
            token.attrSet('id',slug);toc.append({'id':slug,'title':label})
    return Markup(MD.renderer.render(tokens,MD.options,{})),toc

def main():
    from validate import validate_content
    validate_content()
    # Published article relationships are derived, so one metadata edit updates all views.
    for n in DATA['nodes']:
        linked=[a for a in published() if n['id'] in a['nodeIds']]
        if linked:n['contentStatus']='published'
        n['articleSlugs']=list(dict.fromkeys(n['articleSlugs']+[a['slug'] for a in linked]))
    if OUT.exists():shutil.rmtree(OUT)
    OUT.mkdir();shutil.copytree(ROOT/'static',OUT/'assets',ignore=shutil.ignore_patterns('timeline.js','graph.js'))
    (OUT/'assets/highlight.css').write_text(HtmlFormatter().get_style_defs('.highlight'))
    env=Environment(loader=FileSystemLoader(ROOT/'templates'),autoescape=select_autoescape(['html']),trim_blocks=True,lstrip_blocks=True)
    urls=[];search={locale:[] for locale in UI}
    def render(path,template,title,locale,description='',noindex=False,alternate=True,**extra):
        p=url(path,locale); target=OUT/p.strip('/')/'index.html'; target.parent.mkdir(parents=True,exist_ok=True)
        def loc(obj):return obj.get(locale,obj.get('zh-CN','')) if isinstance(obj,dict) else obj
        def U(path):return url(path,locale)
        def label_tag(tag):return loc(TRACKS[tag]['title']) if tag in TRACKS else UI[locale].get(tag,tag)
        def stage_label(s):return UI[locale][{'入门':'intro_stage','必备':'essential_stage','扩展':'extended_stage','挺难':'hard_stage'}[s]]
        def article_url(a):return url('/blog/'+a['slug']+'/',a['locale'])
        pairs=[('zh-CN',url(path,'zh-CN')),('en',url(path,'en'))] if alternate else [(locale,p)]
        ctx=dict(locale=locale,ui=UI[locale],ui_json=json.dumps(UI[locale],ensure_ascii=False).replace("<", "\\u003c"),L=loc,U=U,label_tag=label_tag,path=path,current_url=p,origin=ORIGIN,title=title,description=description or title,alternate=pairs,language_url=url(path,'zh-CN' if locale=='en' else 'en') if alternate else url('/knowledge/','zh-CN' if locale=='en' else 'en'),noindex=noindex,profile=DATA['profile'],tracks=DATA['tracks'],nodes=NODES,topics=TOPICS,lessons=LESSONS,categories=DATA['categories'],relations=DATA['relations'],node_date=node_date,track_path=track_path,reading_minutes=reading_minutes,year='2026',published_count=len(published()),recent=sorted(published(locale),key=lambda a:a.get('updatedAt',a['publishedAt']),reverse=True)[:4],infra=INFRA)
        ctx.update(stage_label=stage_label,article_url=article_url,preferred_articles=preferred_articles,recent=sorted(preferred_articles(locale),key=lambda a:a.get('updatedAt',a['publishedAt']),reverse=True)[:4],published_count=len({a['translationKey'] for a in published()}))
        ctx.update(extra);target.write_text(env.get_template(template).render(**ctx),encoding='utf-8')
        if not noindex:urls.append(ORIGIN+p)
        return p
    for locale in UI:
        ui=UI[locale];L=lambda x:x.get(locale,x.get('zh-CN',''))
        def index(title,path,kind,summary='',tags='',status='planned'):
            search[locale].append(dict(title=title,url=url(path,locale),kind=kind,summary=summary,tags=tags,status=status))
        notes = notebook_entries(locale)
        render('/', 'notebooks.html', L(DATA['profile']['name']), locale, L(DATA['profile']['intro']),
               view='home', entries=notes[:5])
        render('/knowledge/', 'notebooks.html', ui['all_notes'], locale, view='notes', entries=notes)
        for category in SHELF_TAGS:
            name = ui['shelf_'+category]
            title = name+' 笔记' if locale=='zh-CN' else name+' notes'
            path = '/notes/'+category+'/'
            render(path, 'notebooks.html', title, locale, view='notes', category=category,
                   entries=[note for note in notes if category in note['groups']])
            index(title, path, ui['notebooks'])
        render('/notes/ai/computer-vision/', 'notebooks.html', ui['cv_shelf'], locale,
               view='notes', category='ai', subcategory='computer-vision',
               entries=[note for note in notes if 'computer-vision' in note['groups']])
        for path,view,title,desc in [('/skills/','skills',ui['skills'],ui['skills_intro']),('/knowledge/infra/','infra',ui['infra'],ui['infra_desc'])]:
            render(path,'overview.html',title,locale,desc,view=view)
            index(title,path,ui['knowledge'],desc)
        posts=sorted(preferred_articles(locale),key=lambda a:(a['publishedAt'],a['slug']),reverse=True)
        archive={y:[a for a in posts if a['publishedAt'].startswith(y)] for y in sorted({a['publishedAt'][:4] for a in posts},reverse=True)}
        tag_counts={tag:sum(tag in a['tags'] for a in posts) for tag in sorted({tag for a in posts for tag in a['tags']},key=str.casefold)}
        for section,key in [('posts','blog'),('archive','blog_archive'),('tags','blog_tags'),('search','blog_search'),('faq','faq_title')]:
            path='/blog/'+('' if section=='posts' else section+'/')
            render(path,'blog.html',ui[key],locale,ui['blog_desc'],blog_section=section,posts=posts,archive=archive,tag_counts=tag_counts)
        index(ui['blog'],'/blog/',ui['blog'],ui['blog_desc'])
        # Keep bookmarked timeline URLs useful after retiring the timeline views.
        retired = {'/knowledge/ai/','/knowledge/ai/families/','/knowledge/ai/confluence/'}
        retired.update(track_path(t) for t in DATA['tracks'])
        for path in sorted(retired):
            target = '/notes/ai/computer-vision/' if path.endswith('/computer-vision/') else '/notes/ai/'
            render(path, 'retired.html', ui['notebooks'], locale, noindex=True, destination=target)
        for n in DATA['nodes']:
            path='/knowledge/nodes/'+n['slug']+'/'
            related_articles=preferred_articles(locale,[a for a in published() if n['id'] in a['nodeIds']])
            render(path,'node.html',L(n['title']),locale,L(n['summary']),node=n,related_articles=related_articles)
            index(L(n['title']),path,ui[n['kind']],L(n['summary']),' '.join(n['aliases']+n['tags']),n['contentStatus'])
        render('/knowledge/algorithms/','algorithms.html',ui['algorithms'],locale,ui['algorithms_desc'])
        for topic in DATA['algorithms']:
            file=topic['mainContentFiles'].get(locale);body,toc=markdown_file(file)
            related_articles=preferred_articles(locale,[a for a in published() if a['slug'] in topic['relatedArticleSlugs']])
            render('/knowledge/algorithms/'+topic['slug']+'/','algorithm.html',L(topic['title']),locale,L(topic['summary']),topic=topic,body=body,toc=toc,related_articles=related_articles,missing_translation=locale=='en' and not file and bool(topic['mainContentFiles'].get('zh-CN')))
            index(L(topic['title']),'/knowledge/algorithms/'+topic['slug']+'/',ui['algorithms'],L(topic['summary']),' '.join(topic['aliases']+topic['lessonIds']),topic['contentStatus'])
        for item in INFRA:
            render('/knowledge/infra/'+item['id']+'/','overview.html',L(item['title']),locale,L(item['description']),view='infra-detail',infra_item=item)
        body,toc=markdown_file('content/demo.'+('en' if locale=='en' else 'zh')+'.md')
        render('/demo/article/','article.html',ui['demo'],locale,noindex=True,article=dict(title=ui['demo'],summary=ui['demo'],tags=[],nodeIds=['dit'],demo=True),body=body,toc=toc,previous=None,next_article=None)
        render('/404/','overview.html','404',locale,noindex=True,view='404')
    for a in DATA['articles']:
        if a['status']!='published' or a.get('demo'):continue
        locale=a['locale'];body,toc=markdown_file(a['file']);versions=[x for x in published() if x['translationKey']==a['translationKey']];same=sorted(published(locale),key=lambda item:(item['publishedAt'],item['slug']),reverse=True);position=same.index(a)
        pairs=[(v['locale'],url('/blog/'+v['slug']+'/',v['locale'])) for v in versions]
        other=next((v for v in versions if v['locale']!=locale),None)
        other_url=url('/blog/'+other['slug']+'/',other['locale']) if other else url('/blog/'+a['slug']+'/',locale)+'?translation=unavailable'
        source = ''
        if a.get('sourceFile'):
            source = Markup(code_highlight((ROOT/'static/source'/a['sourceFile']).read_text(), 'python'))
        render('/blog/'+a['slug']+'/','article.html',a['title'],locale,a['summary'],article=a,source=source,body=body,toc=toc,previous=same[position-1] if position else None,next_article=same[position+1] if position+1<len(same) else None,language_url=other_url,translation_unavailable=not bool(other),article_alternates=pairs)
    for locale in UI:
        for a in preferred_articles(locale):
            summary=a['summary']
            if a['locale']!=locale:summary+=' · '+UI[locale]['translation_missing']
            search[locale].append(dict(title=a['title'],url=url('/blog/'+a['slug']+'/',a['locale']),kind=UI[locale]['articles'],summary=summary,tags=' '.join(a['tags']),status='published',contentLocale=a['locale']))
    for locale,index in search.items(): (OUT/'assets'/f'search.{locale}.json').write_text(json.dumps(index,ensure_ascii=False))
    shutil.copyfile(OUT/'404/index.html',OUT/'404.html')
    (OUT/'sitemap.xml').write_text('<?xml version="1.0" encoding="utf-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join('<url><loc>'+html.escape(p)+'</loc></url>' for p in sorted(urls))+'</urlset>')
    (OUT/'robots.txt').write_text('User-agent: *\nAllow: /\nDisallow: /demo/\nDisallow: /en/demo/\nSitemap: '+ORIGIN+'/sitemap.xml\n')
    (OUT/'.nojekyll').touch()
    print(f'Built {len(list(OUT.rglob("*.html")))} static HTML files; {len(NODES)} nodes; {len(TOPICS)} algorithm topics; {len(preferred_articles("zh-CN"))} distinct published articles.')

if __name__=='__main__':main()
