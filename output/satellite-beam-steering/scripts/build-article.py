from pathlib import Path
import html
import re

ROOT = Path(__file__).resolve().parent.parent


def inline(text):
    text = html.escape(text)
    text = re.sub(r'`([^`]+)`', r'<code>\1</code>', text)
    text = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'\*([^*]+)\*', r'<em>\1</em>', text)
    return re.sub(r'\[([^\]]+)\]\((https?://[^)]+)\)', r'<a href="\2">\1</a>', text)


def markdown(text, zh=False):
    blocks, paragraph, code, table, bullets = [], [], [], [], []
    in_code = False

    def flush():
        if paragraph:
            blocks.append('<p>' + inline(' '.join(paragraph)) + '</p>')
            paragraph.clear()

    def flush_list():
        if bullets:
            blocks.append('<ul>' + ''.join('<li>' + inline(s) + '</li>' for s in bullets) + '</ul>')
            bullets.clear()

    def flush_table():
        if table:
            cells = [[c.strip() for c in row.strip('|').split('|')] for row in table]
            blocks.append('<div class="table-wrap"><table><thead><tr>' + ''.join('<th>' + inline(c) + '</th>' for c in cells[0]) + '</tr></thead><tbody>' + ''.join('<tr>' + ''.join('<td>' + inline(c) + '</td>' for c in row) + '</tr>' for row in cells[2:]) + '</tbody></table></div>')
            table.clear()

    for line in text.splitlines():
        if line.startswith('```'):
            flush(); flush_table(); flush_list()
            if in_code:
                blocks.append('<pre><code>' + html.escape('\n'.join(code)) + '</code></pre>')
                code.clear()
            in_code = not in_code
            continue
        if in_code:
            code.append(line)
            continue
        if line.startswith('|'):
            flush(); flush_list(); table.append(line)
            continue
        flush_table()
        if line.startswith('- '):
            flush(); bullets.append(line[2:])
            continue
        flush_list()
        if not line:
            flush()
        elif line.startswith('# '):
            flush()
        elif line.startswith('## '):
            flush()
            if line.startswith('## 3.'):
                blocks.append(figure('0870', '将同一个阵面用于卫星全景、近景和结构分层镜头。' if zh else 'The same aperture is reused across the spacecraft, macro and exploded views.'))
            if line.startswith('## 5.'):
                blocks.append(figure('1320', '同一个扫描角驱动相位曲线、波前朝向和归一化方向图。' if zh else 'One steering angle drives the phase traces, wavefront orientation and normalized pattern.'))
            blocks.append('<h2>' + inline(line[3:]) + '</h2>')
        elif line.startswith('> '):
            flush(); blocks.append('<blockquote>' + inline(line[2:]) + '</blockquote>')
        else:
            paragraph.append(line)
    flush(); flush_table(); flush_list()
    return '\n'.join(blocks)


def figure(frame, caption):
    return f'<figure class="wide"><img loading="lazy" src="frames/frame-{frame}.png" alt="{html.escape(caption)}"><figcaption>{html.escape(caption)}</figcaption></figure>'


def build(zh=False):
    stem = 'article-review-zh' if zh else 'article'
    source = (ROOT / (stem + '.md')).read_text()
    title = source.splitlines()[0].removeprefix('# ')
    lang = 'zh-CN' if zh else 'en'
    deck = '从导演 Brief 到成片验证：用一段 36 秒卫星短片说明六步流程，并将方法提炼为独立 Skill。' if zh else 'From director brief to final-file verification, with a 36-second satellite film as a worked example and a reusable Skill.'
    eyebrow = '中文审查稿 · 仅用于内容审查' if zh else 'A PRACTICAL CODEX WORKFLOW'
    nav = '<a href="article.html">English article →</a>' if zh else '<a href="review.html">Film and frame viewer →</a>'
    video = '<figure class="wide"><video controls playsinline preload="metadata" poster="frames/frame-0150.png" src="steering-without-turning.mp4"></video><figcaption>Steering without turning · 36 s · 1920 × 1080 · 60 fps</figcaption></figure>'
    footer = '<a href="steering-without-turning.mp4" download>' + ('下载视频' if zh else 'Download the film') + '</a>'
    footer += f'<a href="{stem}.md">' + ('文章文本' if zh else 'Article text') + '</a>'
    footer += '<a href="video-director.zip" download>' + ('下载 Video Director Skill' if zh else 'Download the Video Director Skill') + '</a>'
    footer += '<a href="article-review-zh.html">中文审查稿</a>' if not zh else ''
    style = (ROOT / 'scripts/article-style.css').read_text()
    page = f'<!doctype html><html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{html.escape(title)}</title><style>{style}</style></head><body><nav><span>LeoGuoLabs</span>{nav}</nav><header><p class="eyebrow">{eyebrow}</p><h1>{html.escape(title)}</h1><p class="deck">{deck}</p></header><article>{video}{markdown(source, zh)}<footer>{footer}</footer></article></body></html>'
    (ROOT / (stem + '.html')).write_text(page)
    print(f'{stem}.html built')


if __name__ == '__main__':
    build()
    build(zh=True)
