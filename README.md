# Web Scraper

A command-line web scraper built with Python, requests and BeautifulSoup.

## Features

- Extract links from any page
- Extract images
- Extract HTML tables
- CSS selector support
- Export to CSV or JSON
- Page overview (title, link count, etc.)

## Setup

```bash
pip install -r requirements.txt
```

## Usage

```bash
# page overview
python scraper.py https://example.com

# extract links
python scraper.py https://example.com --links

# extract with CSS selector
python scraper.py https://example.com --select "h2.title"

# extract table and save as CSV
python scraper.py https://example.com --table 0 -o data.csv

# extract images as JSON
python scraper.py https://example.com --images -o images.json
```
