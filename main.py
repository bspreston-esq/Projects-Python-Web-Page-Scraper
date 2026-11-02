#!/usr/bin/env python3
"""Scrape all links and images from a page into a deduplicated index."""
import argparse
import http.server
import json
import threading
import urllib.parse
import urllib.request
from html.parser import HTMLParser

class LinkParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links, self.images, self.title = [], [], ""
        self._in_title = False

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        if tag == "a" and attributes.get("href"):
            self.links.append(attributes["href"])
        elif tag == "img" and attributes.get("src"):
            self.images.append(attributes["src"])
        elif tag == "title":
            self._in_title = True

    def handle_endtag(self, tag):
        if tag == "title":
            self._in_title = False

    def handle_data(self, data):
        if self._in_title:
            self.title += data

def scrape(url: str):
    request = urllib.request.Request(url, headers={"User-Agent": "page-scraper/1.0"})
    with urllib.request.urlopen(request, timeout=15) as response:
        charset = response.headers.get_content_charset() or "utf-8"
        html = response.read().decode(charset, errors="replace")
    parser = LinkParser()
    parser.feed(html)
    base = url
    links = sorted({urllib.parse.urljoin(base, link) for link in parser.links})
    images = sorted({urllib.parse.urljoin(base, image) for image in parser.images})
    return {"url": url, "title": parser.title.strip(), "links": links, "images": images}

PAGE = b"""<!doctype html><html><head><title>Demo Page</title></head><body>
<a href="/about">About</a><a href="https://example.com/contact">Contact</a>
<a href="/about">About again</a><img src="/logo.png"><img src="images/hero.jpg">
</body></html>"""

def demo() -> None:
    class Handler(http.server.BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(PAGE)))
            self.end_headers(); self.wfile.write(PAGE)
        def log_message(self, *args): pass
    server = http.server.HTTPServer(("127.0.0.1", 0), Handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    try:
        result = scrape(f"http://127.0.0.1:{server.server_address[1]}/")
        print("title:", result["title"])
        for link in result["links"]:
            print("link: ", link)
        for image in result["images"]:
            print("image:", image)
        print(f"{len(result['links'])} unique links, {len(result['images'])} unique images")
    finally:
        server.shutdown(); server.server_close()

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--url")
    parser.add_argument("--output", help="write the index as JSON")
    parser.add_argument("--images-only", action="store_true")
    parser.add_argument("--demo", action="store_true")
    args = parser.parse_args()
    if args.demo or not args.url:
        demo(); return
    try:
        result = scrape(args.url)
    except OSError as exc:
        raise SystemExit(f"Error: {exc}")
    print(f"{result['title']!r}: {len(result['links'])} links, {len(result['images'])} images")
    for item in (result["images"] if args.images_only else result["links"]):
        print(item)
    if args.output:
        with open(args.output, "w", encoding="utf-8") as fh:
            json.dump(result, fh, indent=2)
        print("index written:", args.output)

if __name__ == "__main__":
    main()
