import requests
from bs4 import BeautifulSoup
import csv
import json
import argparse
import sys
from datetime import datetime

def scrape_page(url, selector=None):
    """Scrape a web page and return parsed content."""
    headers = {'User-Agent': 'Mozilla/5.0 (compatible; SimpleScraper/1.0)'}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None

    soup = BeautifulSoup(response.text, 'html.parser')

    if selector:
        elements = soup.select(selector)
        return [el.get_text(strip=True) for el in elements]

    return soup

def scrape_links(url):
    """Extract all links from a page."""
    soup = scrape_page(url)
    if not soup:
        return []
    links = []
    for a in soup.find_all('a', href=True):
        href = a['href']
        text = a.get_text(strip=True)
        if href.startswith('http'):
            links.append({'url': href, 'text': text})
    return links

def scrape_images(url):
    """Extract all image sources from a page."""
    soup = scrape_page(url)
    if not soup:
        return []
    images = []
    for img in soup.find_all('img', src=True):
        images.append({
            'src': img['src'],
            'alt': img.get('alt', ''),
        })
    return images

def scrape_table(url, table_index=0):
    """Extract table data from a page."""
    soup = scrape_page(url)
    if not soup:
        return []
    tables = soup.find_all('table')
    if table_index >= len(tables):
        print(f"Table index {table_index} not found. Page has {len(tables)} tables.")
        return []
    table = tables[table_index]
    rows = []
    for tr in table.find_all('tr'):
        cells = [td.get_text(strip=True) for td in tr.find_all(['td', 'th'])]
        if cells:
            rows.append(cells)
    return rows

def save_csv(data, filename):
    """Save list of dicts or lists to CSV."""
    if not data:
        return
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        if isinstance(data[0], dict):
            writer.writerow(data[0].keys())
            for row in data:
                writer.writerow(row.values())
        else:
            for row in data:
                writer.writerow(row)
    print(f"Saved to {filename}")

def save_json(data, filename):
    """Save data to JSON file."""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"Saved to {filename}")


def main():
    parser = argparse.ArgumentParser(description='Simple web scraper')
    parser.add_argument('url', help='URL to scrape')
    parser.add_argument('--links', action='store_true', help='Extract links')
    parser.add_argument('--images', action='store_true', help='Extract images')
    parser.add_argument('--table', type=int, metavar='INDEX', help='Extract table by index')
    parser.add_argument('--select', type=str, help='CSS selector to extract text')
    parser.add_argument('--output', '-o', type=str, help='Output file (csv or json)')

    args = parser.parse_args()

    if args.links:
        data = scrape_links(args.url)
        print(f"Found {len(data)} links")
    elif args.images:
        data = scrape_images(args.url)
        print(f"Found {len(data)} images")
    elif args.table is not None:
        data = scrape_table(args.url, args.table)
        print(f"Found {len(data)} rows")
    elif args.select:
        data = scrape_page(args.url, args.select)
        if data:
            for item in data:
                print(item)
        return
    else:
        soup = scrape_page(args.url)
        if soup:
            title = soup.find('title')
            print(f"Title: {title.get_text() if title else 'N/A'}")
            print(f"Links: {len(soup.find_all('a'))}")
            print(f"Images: {len(soup.find_all('img'))}")
            print(f"Paragraphs: {len(soup.find_all('p'))}")
        return

    if args.output:
        if args.output.endswith('.json'):
            save_json(data, args.output)
        else:
            save_csv(data, args.output)
    else:
        for item in data[:10]:
            print(item)
        if len(data) > 10:
            print(f"... and {len(data) - 10} more")


if __name__ == '__main__':
    main()
