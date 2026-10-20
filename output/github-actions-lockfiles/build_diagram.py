from pathlib import Path
import base64
import html

OUT = Path(__file__).resolve().parent
PROJECT = Path('/Volumes/TP-1TB/WorspacePlus/Myself/XChineseTrans')
FONT_DIR = PROJECT / 'output/scion-source-control/public'
SLUG = 'actions-lockfiles-flow-v1'

fonts = '\n'.join(
    f"@font-face{{font-family:'Geist';font-style:normal;font-weight:{weight};font-display:block;src:url(data:font/woff2;base64,{base64.b64encode((FONT_DIR / name).read_bytes()).decode()}) format('woff2');}}"
    for weight, name in [(400, 'Geist-Regular.woff2'), (500, 'Geist-Medium.woff2'), (600, 'Geist-SemiBold.woff2')]
)

def txt(x, y, content, size=30, weight=400, color='#1A4A3A', anchor='start', extra=''):
    return f'<text x="{x}" y="{y}" font-family="Geist, Arial, sans-serif" font-size="{size}" font-weight="{weight}" fill="{color}" text-anchor="{anchor}" {extra}>{html.escape(content)}</text>'

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1080 1080" width="1080" height="1080" role="img" aria-labelledby="{SLUG}-title {SLUG}-desc">
<title id="{SLUG}-title">Why CI can change when your code does not</title>
<desc id="{SLUG}-desc">An upstream action moves its v2 tag from commit A to B: without a lockfile the next CI run can execute B and break, while an onboarded workflow keeps running locked commit A until a reviewed update changes the lock.</desc>
<defs>
<style>{fonts}</style>
<marker id="arrow" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto"><polygon points="0 0, 8 3, 0 6" fill="#426454"/></marker>
<marker id="arrow-accent" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto"><polygon points="0 0, 8 3, 0 6" fill="#80601B"/></marker>
<marker id="arrow-link" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto"><polygon points="0 0, 8 3, 0 6" fill="#426454"/></marker>
<filter id="paper-grain" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency="0.72" numOctaves="3" seed="9" stitchTiles="stitch"/><feColorMatrix type="saturate" values="0"/></filter>
</defs>
<rect width="1080" height="1080" fill="#FDFBF7"/>
<rect width="1080" height="1080" filter="url(#paper-grain)" opacity="0.025"/>
{txt(64, 80, 'GitHub Actions · Public preview', 24, 500, '#426454')}
{txt(64, 144, "Your code hasn't changed.", 52, 600)}
{txt(64, 204, 'So why did CI break?', 52, 600)}
{txt(64, 260, 'Same project. Same workflow. Still using build@v2.', 30)}

<!-- Connectors are painted before all process nodes. -->
<g id="connectors" fill="none" stroke="#426454" stroke-width="2.4" marker-end="url(#arrow)">
<path data-edge="upstream-to-without" d="M 380 420 V 448 Q 380 456 372 456 H 304 Q 296 456 296 464 V 492"/>
<path data-edge="upstream-to-with" d="M 700 420 V 448 Q 700 456 708 456 H 776 Q 784 456 784 464 V 492"/>
<path data-edge="without-to-result" d="M 296 620 V 668"/>
<path data-edge="with-to-result" d="M 784 620 V 668"/>
<path data-edge="review-to-update" d="M 328 860 H 392"/>
<path data-edge="update-to-run" d="M 712 860 H 788"/>
</g>

<!-- Shared upstream event: the project and workflow above stay unchanged. -->
<g data-node="upstream">
<rect x="64" y="304" width="952" height="116" fill="#FDFBF7" stroke="#80601B" stroke-width="1.6"/>
{txt(88, 342, 'Third-party build action', 26, 500, '#426454')}
{txt(88, 390, 'Upstream moves v2:  commit A → commit B', 34, 600, '#80601B')}
</g>

<!-- Left and right tracks stay aligned to make the first difference visible. -->
<g data-node="without">
<rect x="64" y="492" width="464" height="128" fill="#FDFBF7" stroke="#426454" stroke-width="1.4"/>
{txt(88, 532, 'Without a lockfile', 28, 500)}
{txt(88, 582, 'v2 resolves to B', 36, 600)}
</g>
<g data-node="with">
<rect x="552" y="492" width="464" height="128" fill="#FDFBF7" stroke="#426454" stroke-width="1.4"/>
{txt(576, 532, 'With an Actions lockfile', 28, 500)}
{txt(576, 582, 'v2 → locked A', 36, 600)}
</g>
<g data-node="without-result">
<rect x="64" y="668" width="464" height="88" rx="44" fill="#FDFBF7" stroke="#426454" stroke-width="1.4"/>
{txt(296, 724, 'Next CI may break', 34, 600, anchor='middle')}
</g>
<g data-node="with-result">
<rect x="552" y="668" width="464" height="88" rx="44" fill="#F6EDCF" stroke="#80601B" stroke-width="1.6"/>
{txt(784, 724, 'Next CI still runs A', 34, 600, anchor='middle')}
</g>

{txt(64, 802, 'To upgrade the locked action:', 26, 500, '#426454')}
<g data-node="review">
<rect x="64" y="812" width="264" height="96" fill="#FDFBF7" stroke="#426454" stroke-width="1.4"/>
{txt(196, 852, 'Review B', 32, 600, anchor='middle')}
{txt(196, 886, 'Approve upgrade', 24, 500, '#426454', anchor='middle')}
</g>
<g data-node="update">
<rect x="392" y="812" width="320" height="96" fill="#FDFBF7" stroke="#426454" stroke-width="1.4"/>
{txt(552, 870, 'Update lock to B', 30, 600, anchor='middle')}
</g>
<g data-node="run-new">
<rect x="788" y="812" width="228" height="96" rx="48" fill="#FDFBF7" stroke="#426454" stroke-width="1.4"/>
{txt(902, 870, 'Run B', 32, 600, anchor='middle')}
</g>

<line x1="64" y1="928" x2="1016" y2="928" stroke="#1A4A3A" stroke-opacity="0.25" stroke-width="1"/>
{txt(64, 960, 'Transitive action dependencies are covered.', 24, 400, '#426454')}
{txt(64, 992, "Called reusable workflows use their own repo's lockfile.", 24, 400, '#426454')}
{txt(64, 1040, 'Locking does not certify safety.', 24, 500)}
{txt(1016, 1040, 'LeoGuoLabs', 24, 500, anchor='end')}
</svg>'''

doc = f'''<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"/><meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>GitHub Actions lockfiles — LeoGuoLabs review</title>
<style>
*{{box-sizing:border-box}}html,body{{margin:0;padding:0;background:#FDFBF7}}
.frame{{max-width:1080px;min-width:0;margin:auto}}
.diagram-container{{width:100%;overflow-x:auto}}
svg{{width:100%;min-width:1080px;display:block}}
@media print{{.diagram-container{{overflow-x:visible}}svg{{min-width:0}}}}
</style></head><body><main class="frame"><div class="diagram-container">{svg}</div></main></body></html>
'''
(OUT / f'{SLUG}.html').write_text(doc)
(OUT / 'alt-en.txt').write_text("Flowchart: Your code and workflow are unchanged, still using build@v2. Upstream moves the third-party action's v2 tag from commit A to B. Without a lockfile, v2 resolves to B and the next CI run may break. With an Actions lockfile, v2 stays readable but the next run still executes locked commit A. To upgrade, review B and approve the change, update the lock to B, then run B. Transitive action dependencies are covered; called reusable workflows use their own repository's lockfile. Locking does not certify safety. GitHub Actions public preview.\n")
print(OUT / f'{SLUG}.html')
