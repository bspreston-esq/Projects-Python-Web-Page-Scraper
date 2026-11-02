# Page Scraper

**Category:** Web

## Problem

Create an application which connects to a site and pulls out all links, or images, and saves them to a list. Optional: Organize the indexed content and don't allow duplicates. Have it put the results into an easily searchable index file.

## Solution

Fetches the page with urllib, parses anchors and image sources with a small `HTMLParser` subclass, resolves relative URLs with `urljoin`, deduplicates with sets, and can export a JSON index. The demo serves a page locally so the full fetch/parse path runs offline.

## How to run

Requires Python 3.8+ and no third-party packages.

```bash
python3 main.py --url https://example.com
python3 main.py --url https://example.com --images-only --output index.json
python3 main.py --demo
```

## Example

```text
title: Demo Page
link:  http://127.0.0.1:38835/about
link:  https://example.com/contact
image: http://127.0.0.1:38835/images/hero.jpg
image: http://127.0.0.1:38835/logo.png
2 unique links, 2 unique images
```

## Attribution

The problem statement is from [karan/Projects](https://github.com/karan/Projects), a list of practical projects that anyone can solve in any programming language (MIT License, Copyright (c) 2013 Karan Goel). The Python solution in this repository was implemented by [bspreston-esq](https://github.com/bspreston-esq).

This repository is part of the [Projects-Python-All](https://github.com/bspreston-esq/Projects-Python-All) collection.
