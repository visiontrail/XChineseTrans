"""Derive text/prompt exports from the edited article; check and package assets."""
from pathlib import Path
from html import unescape
import hashlib
import json
import re
import zipfile

ROOT = Path(__file__).resolve().parents[1]
md = (ROOT / 'article.md').read_text()
prompts = re.findall(r'^### Prompt (\d{2}) — ([^\n]+)\n\n~~~prompt\n(.*?)\n~~~', md, re.M | re.S)
assert [n for n, _, _ in prompts] == [f'{n:02}' for n in range(1, 29)]
assert len(re.findall(r'^## \d+\.', md, re.M)) == 16
assert re.findall(r'^~~~([^\n]*)', md, re.M).count('prompt') == 28
assert not re.search(r'^~~~(?:bash|sh|shell)', md, re.M)
library = '# AI-native Git prompt library\n\n'
library += 'These 28 prompts match the illustrated article. Prompt 01 establishes the working agreement. Later prompts reuse the repository, goal, and authority already established in the conversation. Prompt 28 combines the complete local learning loop. The agent needs access to the relevant tools; account-owner authentication and platform-required interactions may still require a handoff.\n\n'
library += '\n'.join(f'## Prompt {n} — {title}\n\n~~~prompt\n{body}\n~~~\n' for n, title, body in prompts)
(ROOT / 'prompt-library.md').write_text(library)

# Keep paragraph boundaries, inline links, tables and exact prompt line breaks.
plain = re.sub(r'!\[([^\]]*)\]\(([^)]+)\)', r'[Figure: \1 — \2]', md)
plain = re.sub(r'\[([^\]]*)\]\(([^)]+)\)', r'\1 (\2)', plain)
plain = re.sub(r'^#{1,3} ', '', plain, flags=re.M)
plain = re.sub(r'^~~~(?:prompt)?\n?', '', plain, flags=re.M)
plain = plain.replace('**', '').replace('`', '')
plain = re.sub(r'^\*(.+)\*$', r'\1', plain, flags=re.M)
(ROOT / 'article.txt').write_text(plain)

images = re.findall(r'!\[[^\]]*\]\((images/[^)]+)\)', md)
assert len(images) == len(set(images)) == 12
for image in images:
    assert (ROOT / image).is_file(), image
html = (ROOT / 'article.html').read_text()
assert html.count('data:image/png;base64,') == 12
assert html.count('class="prompt-card"') == 28
assert all(unescape(body).strip() in unescape(html) for _, _, body in prompts)
assert 'xaiwind' not in md.lower()
assert '2104039563719262546' not in md
assert not re.search(r'~~~(?:bash|sh|shell)', (ROOT / 'companion/field-notes/README.md').read_text())

fixed = ['README.md','article.html','article.md','article.txt','prompt-library.md',
         'command-atlas.md','alt-text.md','image-prompts.json']
files = [ROOT / name for name in fixed]
files += [p for folder in ['images','diagrams','companion'] for p in (ROOT / folder).rglob('*')
          if p.is_file() and p.name != '.DS_Store' and '__pycache__' not in p.parts]
assert len([p for p in files if p.suffix == '.png']) == 12
for required in ['companion/field-notes/.gitignore','companion/field-notes/.github/workflows/check.yml']:
    assert ROOT / required in files
manifest = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(files)}
(ROOT / 'research/delivery-manifest.json').write_text(json.dumps(manifest, indent=2)+'\n')
archive = ROOT / 'github-ai-native-guide.zip'
with zipfile.ZipFile(archive, 'w', zipfile.ZIP_DEFLATED, compresslevel=8) as bundle:
    for p in sorted(files):
        bundle.write(p, Path('github-ai-native-guide') / p.relative_to(ROOT))
with zipfile.ZipFile(archive) as bundle:
    assert bundle.testzip() is None
    for name, digest in manifest.items():
        assert hashlib.sha256(bundle.read('github-ai-native-guide/'+name)).hexdigest() == digest
report = {'sections':16,'prompts':28,'figures':12,'diagrams':11,
          'approximate_english_words':len(re.findall(r"\b[\w'-]+\b", plain)),
          'archive_files':len(files),'archive_bytes':archive.stat().st_size,
          'required_hidden_companion_files':True,'zip_crc_and_sha256':'pass'}
(ROOT / 'research/delivery-validation.json').write_text(json.dumps(report, indent=2)+'\n')
print(json.dumps(report))
