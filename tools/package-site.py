"""Validate local references and package only the deployable static website."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlparse, unquote
from zipfile import ZipFile, ZIP_DEFLATED
import json
import re

ROOT = Path(__file__).resolve().parents[1]
PUBLIC_FILES = ["index.html", "privacy.html", "terms.html", "404.html", ".nojekyll"]
PUBLIC_DIRS = ["css", "js", "images", "fonts"]

class References(HTMLParser):
    def __init__(self):
        super().__init__()
        self.refs = []
        self.ids = set()
    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        if "id" in values:
            assert values["id"] not in self.ids, f'Duplicate id: {values["id"]}'
            self.ids.add(values["id"])
        for attr in ("href", "src"):
            if attr in values:
                self.refs.append(values[attr])

def main():
    paths = [ROOT / name for name in PUBLIC_FILES]
    for folder in PUBLIC_DIRS:
        paths.extend(p for p in (ROOT / folder).rglob("*") if p.is_file())
    pages = {}
    for name in PUBLIC_FILES:
        if not name.endswith(".html"):
            continue
        parser = References()
        parser.feed((ROOT / name).read_text(encoding="utf-8"))
        pages[name] = parser
    for name, page in pages.items():
        for ref in page.refs:
            parsed = urlparse(ref)
            if parsed.scheme or parsed.netloc:
                continue
            assert not ref.startswith("/"), f"Absolute reference in {name}: {ref}"
            target = (ROOT / unquote(parsed.path or name)).resolve()
            assert target.is_relative_to(ROOT), f"Reference outside site: {ref}"
            assert target.exists(), f"Missing asset in {name}: {ref}"
            if parsed.fragment and target.suffix == ".html":
                assert parsed.fragment in pages[target.name].ids, f"Missing fragment in {name}: {ref}"
    for css in (ROOT / "css").glob("*.css"):
        content = css.read_text(encoding="utf-8")
        for ref in re.findall(r'url\(["\']?([^)"\']+)["\']?\)', content):
            assert not ref.startswith("http"), f"External asset request: {ref}"
            assert (css.parent / ref).exists(), f"Missing CSS dependency: {ref}"
    archive = ROOT / "unmild-designer-site.zip"
    with ZipFile(archive, "w", ZIP_DEFLATED) as bundle:
        for file in paths:
            bundle.write(file, file.relative_to(ROOT).as_posix())
    result = {"files": len(paths), "archive": archive.name, "bytes": archive.stat().st_size,
              "validation": "All local HTML links, fragments, assets and CSS font references resolve."}
    (ROOT / "qa" / "package-report.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result))

if __name__ == "__main__":
    main()
