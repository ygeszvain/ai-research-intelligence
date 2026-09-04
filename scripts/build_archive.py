#!/usr/bin/env python3
"""Regenerate archive metadata from reports/YYYY-MM-DD.html (stdlib only)."""
from __future__ import annotations
import hashlib, json, re, sys, xml.etree.ElementTree as ET
from datetime import datetime, time, timezone
from email.utils import format_datetime
from html import escape, unescape
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
REPORTS=ROOT/'reports'
BASE='https://ygeszvain.github.io/ai-research-intelligence'
DATE_RE=re.compile(r'^(\d{4}-\d{2}-\d{2})\.html$')
TAG_RE=re.compile(r'<[^>]+>')
TOPICS={
 'Agentic AI':('agent','tool use','orchestration'),
 'Evaluation':('evaluation','benchmark','verifier','audit','metric'),
 'Safety & Security':('safety','security','authorization','attack','policy'),
 'Memory & Context':('memory','context','state','kv cache'),
 'RAG & Knowledge':('rag','retrieval','knowledge','provenance','citation'),
 'AI Software Engineering':('coding','code generation','software engineering','repository'),
 'Inference & Infrastructure':('inference','serving','gpu','latency','scheduler','runtime'),
 'Human–AI Workflow':('human-ai','human review','clinician','trust','collaboration'),
 'Multimodal':('multimodal','vision','video','image','audio'),
 'Applied AI':('clinical','medical','financial','chemistry','sepsis','enterprise')}


def clean(s:str)->str:
 return ' '.join(unescape(TAG_RE.sub(' ',s or '')).replace('\xa0',' ').split())

def first(pattern:str,text:str)->str:
 m=re.search(pattern,text,re.I|re.S); return clean(m.group(1)) if m else ''

def excerpt(text:str)->str:
 meta=re.search(r'<meta[^>]+name=["\']description["\'][^>]+content=["\'](.*?)["\']',text,re.I|re.S)
 candidates=[clean(meta.group(1))] if meta else []
 candidates += [clean(x) for x in re.findall(r'<p\b[^>]*>(.*?)</p>',text,re.I|re.S)]
 skip=('executed ','research window','america/chicago','paper fact','author interpretation','independent analysis','enterprise inference','uncertainty')
 for s in candidates:
  if 90<=len(s)<=900 and not s.lower().startswith(skip): return s[:420].rstrip()
 return clean(text)[:420].rstrip()

def display(d:datetime)->str: return f'{d.strftime("%B")} {d.day}, {d.year}'

def parse(path:Path)->dict:
 m=DATE_RE.match(path.name)
 if not m: raise ValueError(f'Invalid report filename: {path.name}')
 date=m.group(1); d=datetime.strptime(date,'%Y-%m-%d'); raw=path.read_bytes(); text=raw.decode('utf-8','replace')
 if '<html' not in text.lower() or '</html>' not in text.lower(): raise ValueError(f'Incomplete HTML: {path}')
 title=first(r'<title\b[^>]*>(.*?)</title>',text) or first(r'<h1\b[^>]*>(.*?)</h1>',text)
 if 'AI Research Intelligence' not in title: title=f'AI Research Intelligence Brief — {display(d)}'
 searchable=clean(re.sub(r'<(?:script|style|svg)\b.*?</(?:script|style|svg)>',' ',text,flags=re.I|re.S)).lower()
 scored=sorted(((sum(searchable.count(w) for w in words),topic) for topic,words in TOPICS.items()),key=lambda x:(-x[0],x[1]))
 topics=[t for n,t in scored if n][:5] or ['AI Research']
 return {'date':date,'date_display':display(d),'title':title[:220],'excerpt':excerpt(text),'topics':topics,
  'path':f'reports/{path.name}','url':f'{BASE}/reports/{path.name}','size_bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}

def write(name:str,content:str): (ROOT/name).write_text(content,encoding='utf-8',newline='\n')

def main()->int:
 if not REPORTS.exists(): print('Missing reports/',file=sys.stderr); return 1
 files=sorted((p for p in REPORTS.iterdir() if p.is_file() and DATE_RE.match(p.name)),reverse=True)
 rows=sorted((parse(p) for p in files),key=lambda x:x['date'],reverse=True)
 if not rows: raise ValueError('No dated reports found')
 now=datetime.now(timezone.utc); latest=rows[0]
 manifest={'site':{'title':'AI Research Intelligence','url':BASE,'description':'Evidence-grounded daily AI and machine-learning research intelligence.','generated_at_utc':now.isoformat(),'report_count':len(rows),'latest_report':latest['date'],'latest_report_url':latest['url']},'reports':rows}
 write('manifest.json',json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
 p=escape(latest['path'],quote=True); u=escape(latest['url'],quote=True); t=escape(latest['title'])
 write('latest.html',f'<!doctype html>\n<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta http-equiv="refresh" content="0; url={p}"><link rel="canonical" href="{u}"><title>Latest AI Research Intelligence Brief</title></head><body><p>Opening <a href="{p}">{t}</a>.</p></body></html>\n')
 items=[]
 for r in rows[:30]:
  dt=datetime.combine(datetime.strptime(r['date'],'%Y-%m-%d').date(),time(9),tzinfo=timezone.utc)
  items.append(f'<item><title>{escape(r["title"])}</title><link>{escape(r["url"])}</link><guid isPermaLink="true">{escape(r["url"])}</guid><pubDate>{format_datetime(dt)}</pubDate><description>{escape(r["excerpt"])}</description></item>')
 write('feed.xml',f'<?xml version="1.0" encoding="UTF-8"?>\n<rss version="2.0"><channel><title>AI Research Intelligence</title><link>{BASE}/</link><description>Evidence-grounded daily AI and machine-learning research intelligence.</description><language>en-us</language><lastBuildDate>{format_datetime(now)}</lastBuildDate>{"".join(items)}</channel></rss>\n')
 urls=[f'{BASE}/',f'{BASE}/latest.html',*[r['url'] for r in rows]]
 write('sitemap.xml','<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join(f'<url><loc>{escape(x)}</loc></url>' for x in urls)+'</urlset>\n')
 write('robots.txt',f'User-agent: *\nAllow: /\nSitemap: {BASE}/sitemap.xml\n')
 write('archive-status.json',json.dumps({'status':'ok','generated_at_utc':now.isoformat(),'report_count':len(rows),'latest_report':latest['date']},indent=2)+'\n')
 data=json.loads((ROOT/'manifest.json').read_text()); assert data['site']['report_count']==len(rows); ET.parse(ROOT/'feed.xml'); ET.parse(ROOT/'sitemap.xml')
 index=(ROOT/'index.html').read_text(encoding='utf-8'); assert 'manifest.json' in index and 'renderArchive' in index
 print(f'Archive rebuilt: {len(rows)} reports; latest={latest["date"]}')
 return 0
if __name__=='__main__': raise SystemExit(main())
