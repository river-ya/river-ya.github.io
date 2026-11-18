"""Validate content references and crawl the generated static output."""
from __future__ import annotations
import json,re,sys
from pathlib import Path
from datetime import date
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
from i18n import UI

ROOT=Path(__file__).resolve().parents[1]
def load(name):return json.loads((ROOT/'data'/f'{name}.json').read_text())
def need(condition,message):
    if not condition:raise ValueError(message)
def keyed(items,name):
    need(len({x['id'] for x in items})==len(items),f'Duplicate {name} IDs')
    return {x['id']:x for x in items}
def acyclic(items,key,name):
    visiting=set();done=set()
    def visit(id):
        need(id not in visiting,f'Cycle in {name}: {id}')
        if id in done:return
        visiting.add(id)
        for p in items[id].get(key,[]):
            need(p in items,f'Unknown prerequisite {p} in {name}');visit(p)
        visiting.remove(id);done.add(id)
    for id in items:visit(id)
def bilingual(x,field,context):
    need(isinstance(x.get(field),dict) and bool(x[field].get('zh-CN')),f'Missing Chinese {field}: {context}')
def validate_content():
    nodes=keyed(load('nodes'),'node');tracks=keyed(load('tracks'),'track');topics=keyed(load('algorithms'),'topic');lessons=keyed(load('lessons'),'lesson');relations=keyed(load('relations'),'relation');confluences=keyed(load('confluences'),'confluence');articles=load('articles');categories=keyed(load('categories'),'category');audit=keyed(load('source-audit'),'audit')
    need(set(UI['zh-CN'])==set(UI['en']),'UI key parity failed')
    for lang,strings in UI.items():need(all(isinstance(s,str) and s.strip() for s in strings.values()),f'Empty UI string: {lang}')
    profile=load('profile');need(set(profile['currentTopics'])<=nodes.keys(),'Unknown current topic')
    for group in profile['skills']:
        for skill in group['items']:need(skill['status'] in [None,'learning','practiced','independent'],'Unknown skill status')
    article_keys=set();translation_keys=set()
    for a in articles:
        need(re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*',a['slug']) and a['slug'] not in {'archive','tags','search','faq'},'Invalid or reserved blog slug')
        k=(a['locale'],a['slug']);need(k not in article_keys,f'Duplicate article: {k}');article_keys.add(k)
        tk=(a['locale'],a['translationKey']);need(tk not in translation_keys,f'Duplicate translation key: {tk}');translation_keys.add(tk)
        need(a['locale'] in UI,'Invalid article locale');need(a['status'] in ['planned','draft','published'],'Invalid article status')
        need(set(a['nodeIds'])<=nodes.keys(),'Unknown article node')
        file=(ROOT/a['file']).resolve();need(file.is_relative_to(ROOT/'content') and file.is_file(),f'Missing content file: {a["file"]}')
        if 'sourceFile' in a:
            name = a['sourceFile']
            need(isinstance(name,str) and re.fullmatch(r'[\w-]+\.py',name)
                 and (ROOT/'static/source'/name).is_file(), 'Invalid article source file')
        if a['status']=='published':date.fromisoformat(a['publishedAt']);need(file.read_text().strip(),'Published article has no body')
        if a.get('updatedAt'):date.fromisoformat(a['updatedAt']);need(a['updatedAt']>=a.get('publishedAt',''),'Update precedes publication')
    for id,n in nodes.items():
        need(re.fullmatch(r'[a-z0-9-]+',id) and n['slug']==id,f'Invalid stable node ID: {id}')
        for field in ['title','summary','significance']:bilingual(n,field,id)
        need(n['kind'] in ['model','method','concept','practice','research-area'],f'Invalid kind: {id}')
        need(n['contentStatus'] in ['planned','draft','published'],f'Invalid status: {id}')
        need(n['difficulty'] in ['foundation','core','advanced','optional'],f'Invalid difficulty: {id}')
        need(set(n['trackIds']+n['familyIds'])<=tracks.keys(),f'Unknown track: {id}')
        need(set(n['relatedNodeIds'])<=nodes.keys(),f'Unknown related node: {id}')
        for t in n['trackIds']+n['familyIds']:need(id in tracks[t]['learningOrder'],f'Missing reciprocal track membership: {id}/{t}')
        if n['dateVerification']=='verified':need(n['dates'] and id in audit,f'Verified date without evidence: {id}')
        for d in n['dates']:
            need(d['precision'] in ['year','month','day'],f'Invalid precision: {id}')
            need(len(d['value'])=={'year':4,'month':7,'day':10}[d['precision']],f'Date precision mismatch: {id}')
            date.fromisoformat(d['value']+{'year':'-01-01','month':'-01','day':''}[d['precision']])
            need(d['event'] in ['preprint','publication','announcement','code-release'],f'Invalid event: {id}')
            need(d['sourceUrl'].startswith('https://'),f'Date missing source: {id}')
        for slug in n['articleSlugs']:need(any(a['slug']==slug for a in articles),f'Unknown article slug: {id}/{slug}')
        if n['contentStatus']=='published':need(any(id in a['nodeIds'] and a['status']=='published' and not a.get('demo') for a in articles),f'Published node without article: {id}')
    acyclic(nodes,'prerequisiteIds','knowledge prerequisites')
    for id,t in tracks.items():
        need(len(set(t['learningOrder']))==len(t['learningOrder']),f'Duplicate track node: {id}')
        need(set(t['learningOrder'])<=nodes.keys(),f'Unknown node in track: {id}')
        for n in t['learningOrder']:need(id in nodes[n]['trackIds']+nodes[n]['familyIds'],f'Unmatched track membership: {id}/{n}')
        date.fromisoformat(t['verifiedThrough'])
    for r in relations.values():
        need(r['fromNodeId'] in nodes and r['toNodeId'] in nodes,'Unknown relation endpoint')
        need(r['kind'] in ['extends','combines','uses-component','inspired-by'],'Unknown relation kind')
        need(r['sourceUrls'] and all(x.startswith('https://') for x in r['sourceUrls']),'Relation without evidence')
        bilingual(r,'contribution',r['id'])
    # Inheritance alone is a DAG; component and inspiration edges are separate semantics.
    inheritance={id:{'parents':[]} for id in nodes}
    for r in relations.values():
        if r['kind']=='extends':inheritance[r['toNodeId']]['parents'].append(r['fromNodeId'])
    acyclic(inheritance,'parents','inheritance')
    for c in confluences.values():
        need(c['nodeId'] in nodes,'Unknown confluence node');need(set(c['familyIds'])<=set(nodes[c['nodeId']]['familyIds']),'Confluence family mismatch')
        for id in c['incomingRelationIds']:need(id in relations and relations[id]['toNodeId']==c['nodeId'],'Confluence edge mismatch')
    for id,t in topics.items():
        need(t['categoryId'] in categories,'Unknown topic category');need(t['lessonIds'] and set(t['lessonIds'])<=lessons.keys(),'Invalid course mapping')
        for l in t['lessonIds']:need(id in lessons[l]['algorithmIds'],'Nonreciprocal course mapping')
        for locale,file in t['mainContentFiles'].items():
            path=(ROOT/file).resolve();need(locale in UI and path.is_relative_to(ROOT/'content') and path.is_file(),f'Missing algorithm body: {id}')
        if t['contentStatus']=='published':need(t['mainContentFiles'],'Published algorithm lacks body')
        for slug in t['relatedArticleSlugs']:need(any(a['slug']==slug for a in articles),'Unknown related algorithm article')
    acyclic(topics,'prerequisiteIds','algorithm prerequisites')
    for id,l in lessons.items():
        need(re.fullmatch(r'\d{3}',id) and l['lessonNumber']==id,'Invalid course number')
        need(re.fullmatch(r'[0-9a-f]{40}',l['sourceRef']),'Course snapshot must pin SHA')
        need(l['sourceRef'] in l['sourceUrl'],'Course source must point to pinned revision')
        need(set(l['algorithmIds'])<=topics.keys(),'Invalid course topic');date.fromisoformat(l['checkedAt'])
    print(f'Content valid: {len(nodes)} nodes, {len(tracks)} routes, {len(topics)} topics, {len(lessons)} lessons; references and prerequisite DAGs checked.')

class Document(HTMLParser):
    def __init__(self,text):
        super().__init__(convert_charrefs=True);self.links=[];self.ids=set();self.duplicates=[];self.lang=None;self.canonical=None;self.h1=0;self.alternates=[];self.feed(text)
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if tag=='html':self.lang=a.get('lang')
        if tag=='h1':self.h1+=1
        if 'id' in a:
            if a['id'] in self.ids:self.duplicates.append(a['id'])
            self.ids.add(a['id'])
        if tag=='link' and a.get('rel')=='canonical':self.canonical=a.get('href')
        if tag=='link' and a.get('rel')=='alternate':self.alternates.append(a.get('href'))
        for key in ['href','src']:
            if key in a:self.links.append(a[key])

def validate_output():
    out=ROOT/'dist';files=set(p for p in out.rglob('*') if p.is_file());docs={p:Document(p.read_text()) for p in files if p.suffix=='.html'};errors=[];links=0
    for p,d in docs.items():
        rel=p.relative_to(out).as_posix();expected='en' if rel.startswith('en/') else 'zh-CN'
        if d.lang!=expected:errors.append(f'Language mismatch {rel}')
        if d.h1!=1:errors.append(f'Expected one h1 {rel}, got {d.h1}')
        if d.duplicates:errors.append(f'Duplicate IDs {rel}: {d.duplicates}')
        canonical='https://river-ya.github.io/'+rel.removesuffix('index.html')
        if rel!='404.html' and d.canonical!=canonical:errors.append(f'Canonical mismatch {rel}')
        for href in d.links:
            u=urlsplit(href)
            if u.scheme and u.netloc!='river-ya.github.io':continue
            if not u.path:target=p
            else:
                target=out/unquote(u.path.lstrip('/')) if u.path.startswith('/') or u.netloc else p.parent/unquote(u.path)
                if target not in files and target/'index.html' in files:target=target/'index.html'
            links+=1
            if target not in files:errors.append(f'Missing target {href} from {rel}')
            elif u.fragment and target in docs and unquote(u.fragment) not in docs[target].ids:errors.append(f'Missing anchor {href} from {rel}')
    need(not errors,'\n'.join(errors[:80]))
    need((out/'404.html').exists(),'Missing 404.html')
    need(not (out/'CNAME').exists(),'Unexpected custom domain')
    print(f'Static output valid: {len(docs)} HTML pages, {links} internal links/assets/anchors; canonical and language metadata checked.')
    return {'pages':len(docs),'internalReferences':links,'errors':errors}

if __name__=='__main__':
    validate_content()
    if '--output' in sys.argv:validate_output()
