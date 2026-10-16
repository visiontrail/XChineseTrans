"""Build the local review page and rich-text segments from the article source."""
from pathlib import Path
import html
import json
import re

ROOT = Path(__file__).resolve().parent
source = (ROOT / 'article.md').read_text()
title, body = source.split('\n\n', 1)
title = title.removeprefix('# ')

def inline(value):
    value = html.escape(value)
    value = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', value)
    return re.sub(r'\[([^]]+)\]\((https://[^)]+)\)', r'<a href="\2">\1</a>', value)

def render(text, figures=True):
    blocks = []
    for paragraph in text.strip().split('\n\n'):
        if paragraph.startswith('## '):
            heading = paragraph[3:]
            anchor = re.sub(r'[^a-z0-9]+', '-', heading.lower()).strip('-')
            blocks.append(f'<h2 id="{anchor}">{inline(heading)}</h2>')
        elif paragraph.startswith('!['):
            match = re.fullmatch(r'!\[([^]]*)\]\(([^)]+)\)', paragraph)
            if figures and match:
                alt, path = match.groups()
                assert (ROOT / path).is_file()
                blocks.append(f'<figure><img src="{html.escape(path)}" alt="{html.escape(alt)}" width="1122" height="1402"></figure>')
        else:
            blocks.append(f'<p>{inline(paragraph)}</p>')
    return '\n'.join(blocks)

article_html = render(body)
segments = re.split(r'\n\n!\[[^]]*\]\([^)]+\)\n\n', body)
(ROOT / 'article-segments.json').write_text(json.dumps([{'html':render(s,False),'text':re.sub(r'\[([^]]+)\]\((https://[^)]+)\)',r'\1 (\2)',s).replace('## ','').replace('**','')} for s in segments],ensure_ascii=False,indent=2)+'\n')
(ROOT / 'article-body.html').write_text(article_html+'\n')
plain = re.sub(r'!\[([^]]*)\]\(([^)]+)\)',r'[Figure: \2]',body)
plain = re.sub(r'\[([^]]+)\]\((https://[^)]+)\)',r'\1 (\2)',plain).replace('## ','').replace('**','')
(ROOT / 'article.txt').write_text(title+'\n\n'+plain)
toc = [(m.group(1),re.sub(r'[^a-z0-9]+','-',m.group(1).lower()).strip('-')) for m in re.finditer(r'^## (.+)$',body,re.M)]
nav = ''.join(f'<a href="#{slug}">{html.escape(label)}</a>' for label,slug in toc)
page = '''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>__TITLE__ — LeoGuoLabs</title>
<style>
:root{--paper:#FDFBF7;--ink:#1A4A3A;--muted:#426454;--gold:#80601B;--rule:#d5ded7;color-scheme:light}*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;background:var(--paper);color:var(--ink);font:19px/1.75 Geist,Inter,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}header{max-width:1180px;margin:auto;padding:26px 32px;display:flex;justify-content:space-between;gap:20px;border-bottom:1px solid var(--rule);font-size:14px}header strong{font-size:21px;font-weight:600;letter-spacing:-.6px}header span{color:var(--muted)}.cover{display:block;width:calc(100% - 64px);max-width:1116px;height:auto;margin:32px auto 54px}.layout{max-width:1180px;margin:auto;padding:0 32px 80px;display:grid;grid-template-columns:220px minmax(0,760px);gap:58px;align-items:start}aside{position:sticky;top:30px;padding-top:8px;font-size:13px;line-height:1.5}aside span{color:var(--gold);display:block;margin-bottom:18px}aside a{display:block;text-decoration:none;margin:0 0 16px;color:var(--muted)}aside a:hover{color:var(--ink);text-decoration:underline}h1{font-size:clamp(36px,4.7vw,58px);line-height:1.08;letter-spacing:-1.8px;font-weight:600;margin:0 0 30px}h1+p{font-size:23px;line-height:1.5;color:var(--muted);margin-bottom:40px}p{margin:0 0 24px}h2{font-size:30px;font-weight:600;line-height:1.2;letter-spacing:-.5px;margin:58px 0 24px;scroll-margin-top:24px}a{color:var(--gold);text-decoration-thickness:1px;text-underline-offset:4px}strong{font-weight:600}figure{margin:40px auto 48px;max-width:650px}figure img{width:100%;height:auto;display:block}footer{max-width:1180px;margin:auto;padding:24px 32px 40px;border-top:1px solid var(--rule);font-size:14px;color:var(--muted)}@media(max-width:850px){.layout{display:block;max-width:780px}aside{display:none}.cover{margin-bottom:36px}h1{font-size:43px}}@media(max-width:480px){body{font-size:17px;line-height:1.72}header{padding:20px 22px}header span{font-size:12px}.cover{width:100%;margin:18px 0 30px}.layout{padding:0 22px 50px}h1{font-size:36px;letter-spacing:-1px}h1+p{font-size:20px;margin-bottom:30px}h2{font-size:27px;margin-top:44px}figure{margin:30px -10px 36px}footer{padding:22px}}@media print{aside{display:none}.layout{display:block;padding:0}body{font-size:12pt}figure{max-width:430px;break-inside:avoid}.cover{max-width:750px}h2{break-after:avoid}a{color:inherit}}
</style></head><body>
<header><strong>LeoGuoLabs</strong><span>AI &amp; learning</span></header>
<img class="cover" src="00-article-cover-v1.png" alt="A learner reconstructs a diagram on paper beside a closed laptop. Learning With AI After You Close the Chat." width="1983" height="793">
<div class="layout"><aside aria-label="Article sections"><span>In this article</span>__NAV__</aside><main><article><h1>__TITLE__</h1>__BODY__</article></main></div>
<footer>LeoGuoLabs</footer></body></html>'''
page = page.replace('__TITLE__',html.escape(title)).replace('__NAV__',nav).replace('__BODY__',article_html)
(ROOT/'article.html').write_text(page)
assert len(segments)==4
assert len(re.findall('<figure>',article_html))==3
print(json.dumps({'title':title,'body_sections':len(toc),'rich_text_segments':len(segments),'inline_images':3,'source_links':len(re.findall(r'href="https://',article_html))},indent=2))
