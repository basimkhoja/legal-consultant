#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Fetch an instrument from an official legislation portal and print it as markdown.

Usage:
  fetch-law.py --portal boe --id <law-guid> [--lang ar|en] [--out FILE]
  fetch-law.py --portal boe --index            # list laws the portal exposes (GUID, title)
  fetch-law.py --portal boe --search "نظام العمل"
  fetch-law.py --portal boe --id <law-guid> --attachments   # official PDFs and translations

Portals are adapters keyed by the code used in references/jurisdictions/<code>/MANIFEST.md
(`source_portal:`). Today only `boe` (laws.boe.gov.sa, Kingdom of Saudi Arabia) is implemented.
The script uses curl because the portal's TLS chain is verified by the OS trust store but
rejected by some HTTP libraries. Output is plain text for a skill to quote from; the skill,
not this script, decides the provenance tag. Nothing here interprets the law.

Exit codes: 0 fetched, 2 usage, 3 fetch failed (skill must stop, not supplement).
"""
import argparse
import html
import re
import subprocess
import sys
from html.parser import HTMLParser

PORTALS = {
    "boe": {
        "name": "Bureau of Experts at the Council of Ministers (laws.boe.gov.sa)",
        "detail": "https://laws.boe.gov.sa/BoeLaws/Laws/LawDetails/{id}/{lang}",
        "folders": ["https://laws.boe.gov.sa/BoeLaws/Laws/Folders/1",
                    "https://laws.boe.gov.sa/BoeLaws/Laws/Folders/2"],
        "langs": {"ar": "1", "en": "2"},
    }
}


def curl(url: str) -> str:
    r = subprocess.run(
        ["curl", "-sS", "--max-time", "90", "-A", "Mozilla/5.0 (legal-consultant fetch-law)", url],
        capture_output=True, text=True)
    if r.returncode != 0 or not r.stdout.strip():
        sys.stderr.write(f"fetch failed: {url}\n{r.stderr}\n")
        sys.exit(3)
    return r.stdout


class _Text(HTMLParser):
    """Collapse HTML to text, keeping headings and paragraphs on their own lines."""
    BLOCK = {"p", "div", "h1", "h2", "h3", "h4", "li", "br", "tr", "table"}

    def __init__(self):
        super().__init__()
        self.parts = []
        self.skip = 0

    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style"):
            self.skip += 1
        if tag in self.BLOCK:
            self.parts.append("\n")
        if tag == "h3":
            self.parts.append("\n### ")

    def handle_endtag(self, tag):
        if tag in ("script", "style") and self.skip:
            self.skip -= 1
        if tag in self.BLOCK:
            self.parts.append("\n")

    def handle_data(self, data):
        if not self.skip:
            self.parts.append(data)

    def text(self):
        t = html.unescape("".join(self.parts))
        t = re.sub(r"[ \t ]+", " ", t)
        t = re.sub(r"\n\s*\n+", "\n\n", t)
        return t.strip()


def _html_to_text(fragment: str) -> str:
    parser = _Text()
    parser.feed(fragment)
    return parser.text()


def boe_detail(guid: str, lang: str) -> str:
    """Render a BOE law page as markdown, article by article.

    The portal keeps the ORIGINAL wording in each article body and puts every
    amendment (with the amending decree and the new wording) in a pop-up list
    above it. For an amended article this renders the body under "النص الأصلي"
    and each amendment under "تعديلات المادة" in the portal's order, so the LAST
    amendment block is the wording currently in force. Readers must use that
    block, not the body, for any article marked amended.
    """
    p = PORTALS["boe"]
    url = p["detail"].format(id=guid, lang=p["langs"][lang])
    raw = curl(url)
    meta = []
    for label in ("تاريخ الإصدار", "تاريخ النشر", "الحالة", "Issue Date", "Publication Date"):
        mm = re.search(label + r".{0,160}", raw, flags=re.S)
        if mm:
            clean = re.sub(r"<[^>]+>", " ", mm.group(0))
            meta.append(re.sub(r"\s+", " ", html.unescape(clean)).strip())
    tools = re.search(r"أدوات إصدار النظام(.*?)</div>\s*</div>", raw, flags=re.S)
    if tools:
        meta.append("أدوات الإصدار: " + re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " | ", tools.group(1)))).strip(" |"))
    # Preamble (law description block) before the first article container.
    first = re.search(r'<div[^>]*class="[^"]*article_item[^"]*"', raw)
    head_text = _html_to_text(raw[:first.start()]) if first else ""
    head_text = "\n".join(l for l in head_text.splitlines() if l.strip())
    # Split into article blocks.
    blocks = re.split(r'(?=<div[^>]*class="article_item[^"]*")', raw[first.start():] if first else raw)
    out = []
    changed = 0
    for b in blocks:
        m = re.match(r'<div[^>]*class="article_item([^"]*)"', b)
        if not m:
            continue
        is_changed = "changed-article" in m.group(1)
        title = re.search(r"<h3[^>]*>(.*?)</h3>", b, flags=re.S)
        title_txt = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", "", title.group(1)))).strip() if title else "مادة"
        popups = re.findall(r'<div class="article_item_popup">(.*?)</div>\s*<a href', b, flags=re.S)
        pop_txt = [_html_to_text(re.sub(r"<h3.*?</h3>", "", x, flags=re.S)) for x in popups]
        body_html = re.sub(r'<div[^>]*class="[^"]*popup-list"[^>]*>.*?</div>\s*</div>\s*</div>', "", b, flags=re.S) if popups else b
        body_html = re.sub(r"<h3.*?</h3>", "", body_html, count=1, flags=re.S)
        body_html = re.sub(r'<div class="article_btns">.*?</div>', "", body_html, flags=re.S)
        body_txt = _html_to_text(body_html)
        body_txt = re.sub(r"^\s*(تعديلات المادة)\s*", "", body_txt).strip()
        if is_changed:
            changed += 1
            out.append(f"### {title_txt} [معدلة]")
            out.append("**النص الأصلي (قبل التعديل):**\n" + body_txt)
            for i, t in enumerate(pop_txt, 1):
                tag = " (النص النافذ)" if i == len(pop_txt) else ""
                out.append(f"**تعديلات المادة {i}/{len(pop_txt)}{tag}:**\n" + t.strip())
        else:
            out.append(f"### {title_txt}")
            out.append(body_txt)
        out.append("")
    status = next((m for m in meta if m.startswith("الحالة")), "الحالة: (not found)")
    if "لاغي" in status:
        sys.stderr.write(f"WARNING: portal status is repealed (لاغي) for {guid}; find the current law with --search\n")
    head = [f"<!-- source: {url} -->", f"<!-- portal: {p['name']} -->", f"<!-- status: {status} -->",
            f"<!-- articles marked as amended on the portal: {changed} -->",
            "<!-- For an article marked [معدلة], the body is the ORIGINAL text; the last 'تعديلات المادة' block is the wording in force. -->"]
    return "\n".join(head + [""] + meta + ["", head_text, ""] + out)


def boe_attachments(guid: str, lang: str) -> list:
    """List downloadable attachments (official PDFs, translations) on a BOE law page."""
    p = PORTALS["boe"]
    raw = curl(p["detail"].format(id=guid, lang=p["langs"][lang]))
    out = []
    for m in re.finditer(r'href="([^"]*Files/Download/\?attId=[0-9a-f-]{36})"[^>]*>(.*?)</a>', raw, flags=re.S):
        label = re.sub(r"<[^>]+>", " ", m.group(2))
        label = re.sub(r"\s+", " ", html.unescape(label)).strip() or "(no label)"
        url = m.group(1)
        if url.startswith("/"):
            url = "https://laws.boe.gov.sa" + url
        out.append((label, url))
    return out


def boe_index() -> list:
    seen = {}
    for url in PORTALS["boe"]["folders"]:
        raw = curl(url)
        for m in re.finditer(r'LawDetails/([0-9a-f-]{36})/\d[^"]*"[^>]*>\s*(?:<i[^>]*></i>)?\s*([^<]{2,200}?)\s*<', raw):
            guid, title = m.group(1), html.unescape(m.group(2)).strip()
            if guid not in seen or len(title) > len(seen[guid]):
                seen[guid] = title
    return sorted(seen.items(), key=lambda kv: kv[1])


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--portal", required=True, choices=PORTALS.keys())
    ap.add_argument("--id")
    ap.add_argument("--lang", default="ar")
    ap.add_argument("--index", action="store_true")
    ap.add_argument("--search")
    ap.add_argument("--attachments", action="store_true", help="list attachment download links for --id")
    ap.add_argument("--out")
    a = ap.parse_args()
    if a.index or a.search:
        rows = boe_index()
        if a.search:
            rows = [r for r in rows if a.search in r[1]]
        for guid, title in rows:
            print(f"{guid}\t{title}")
        return 0
    if not a.id:
        ap.print_usage()
        return 2
    if a.attachments:
        for label, url in boe_attachments(a.id, a.lang):
            print(f"{label}\t{url}")
        return 0
    if a.lang not in PORTALS[a.portal]["langs"]:
        sys.stderr.write(f"lang must be one of {list(PORTALS[a.portal]['langs'])}\n")
        return 2
    text = boe_detail(a.id, a.lang)
    if a.out:
        with open(a.out, "w", encoding="utf-8") as f:
            f.write(text + "\n")
        print(f"wrote {a.out} ({len(text)} chars)")
    else:
        print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
