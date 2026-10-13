"""Check this small static site without making network requests.

Scope: HTML title/H1 presence, local href/src targets and HTML fragment IDs.
Not a browser test, external-link checker, or general HTML validator.
"""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
import sys


class Page(HTMLParser):
    def __init__(self, text):
        super().__init__(convert_charrefs=True)
        self.links = []
        self.ids = set()
        self.h1_count = 0
        self.in_title = False
        self.title = ""
        self.feed(text)
        self.close()

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "h1":
            self.h1_count += 1
        if tag == "title":
            self.in_title = True
        if attrs.get("id"):
            self.ids.add(attrs["id"])
        for key in ("href", "src"):
            if attrs.get(key):
                self.links.append(attrs[key])

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        self.handle_endtag(tag)

    def handle_endtag(self, tag):
        if tag == "title":
            self.in_title = False

    def handle_data(self, data):
        if self.in_title:
            self.title += data


def check(root):
    root = root.resolve()
    pages = {
        p.resolve(): Page(p.read_text(encoding="utf-8"))
        for p in root.rglob("*.html")
    }
    errors = []
    if not pages:
        return ["No HTML pages found."]
    if root / "index.html" not in pages:
        errors.append("Missing docs/index.html.")
    for path, page in sorted(pages.items()):
        label = str(path.relative_to(root))
        if not page.title.strip():
            errors.append(f"{label}: missing nonempty title")
        if not page.h1_count:
            errors.append(f"{label}: missing H1")
        for link in page.links:
            try:
                url = urlsplit(link)
            except ValueError:
                errors.append(f"{label}: invalid URL: {link}")
                continue
            if url.scheme or url.netloc:
                continue  # External links and other schemes are outside scope.
            decoded_path = unquote(url.path)
            if decoded_path.startswith("/"):
                errors.append(f"{label}: root-relative path: {link}")
                continue
            target = (path.parent / decoded_path).resolve() if decoded_path else path
            if not target.is_relative_to(root):
                errors.append(f"{label}: path escapes docs: {link}")
                continue
            if target.is_dir():
                target = target / "index.html"
            if not target.is_file():
                errors.append(f"{label}: missing target: {link}")
                continue
            fragment = unquote(url.fragment)
            if fragment and target in pages and fragment not in pages[target].ids:
                errors.append(f"{label}: missing fragment ID: {link}")
    return errors


if __name__ == "__main__":
    site_root = Path(__file__).resolve().parents[1] / "docs"
    problems = check(site_root)
    if problems:
        print("\n".join(problems))
        sys.exit(1)
    print("PASS: local HTML structure, link targets, and fragment IDs.")
    print("Not checked: external URLs, browser behavior, or public deployment.")
