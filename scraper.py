"""Web Scraper for Quotes & Headlines
InternCircle Project 04 | Python Programming

Polite, robust web scraper targeting https://quotes.toscrape.com
using requests and BeautifulSoup.

Time Complexity:
    - Network I/O: O(P) HTTP requests for P pages, rate-limited at 1s delay
    - DOM Parsing: O(N) where N is the character length of the HTML response
    - Summary Analytics: O(Q) where Q is the total number of extracted quotes

Space Complexity:
    - Auxiliary Memory: O(Q) to store parsed records prior to serialization
"""

import json
import os
import time
from collections import Counter
from typing import Any, Dict, List, Optional, Tuple

import requests
from bs4 import BeautifulSoup

# ==============================================================================
# CONFIGURATION & SELECTORS
# Selectors centralized in one place for maintainability.
# ==============================================================================
BASE_URL = "https://quotes.toscrape.com"
HEADERS = {
    "User-Agent": "InternCircle-learning-project (student scraper, polite rate-limited)"
}
REQUEST_TIMEOUT = 10  # seconds
POLITE_DELAY = 1.0    # seconds between requests

SELECTORS = {
    "quote_card": "div.quote",
    "text": "span.text",
    "author": "small.author",
    "tags": "a.tag",
    "next_button": "li.next a",
}


# ==============================================================================
# SCRAPER CORE FUNCTIONS
# ==============================================================================

def fetch_page(url: str) -> Optional[str]:
    """Fetches HTML content from URL with timeout and error handling.
    
    Time Complexity: O(1) network request
    Space Complexity: O(M) response text buffer
    """
    try:
        response = requests.get(url, headers=HEADERS, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        return response.text
    except requests.exceptions.Timeout:
        print(f"Error: Connection timed out fetching {url}")
    except requests.exceptions.ConnectionError:
        print(f"Error: Network connection problem accessing {url}")
    except requests.exceptions.HTTPError as http_err:
        print(f"Error: HTTP {http_err.response.status_code} fetching {url}")
    except requests.exceptions.RequestException as err:
        print(f"Error: Failed to fetch {url} ({err})")
    return None


def parse_quotes_from_html(html: str) -> Tuple[List[Dict[str, Any]], Optional[str]]:
    """Parses quotes from HTML markup safely checking for None before get_text.
    
    Returns:
        (quotes_list, next_relative_url)
    """
    soup = BeautifulSoup(html, "html.parser")
    extracted_quotes = []

    for card in soup.select(SELECTORS["quote_card"]):
        text_elem = card.select_one(SELECTORS["text"])
        author_elem = card.select_one(SELECTORS["author"])
        tag_elems = card.select(SELECTORS["tags"])

        # Guard against missing elements
        text = text_elem.get_text(strip=True) if text_elem else "N/A"
        author = author_elem.get_text(strip=True) if author_elem else "Unknown"
        tags = [t.get_text(strip=True) for t in tag_elems] if tag_elems else []

        extracted_quotes.append({
            "text": text,
            "author": author,
            "tags": tags,
        })

    next_link = soup.select_one(SELECTORS["next_button"])
    next_url = next_link.get("href") if next_link else None

    return extracted_quotes, next_url


def scrape_quotes(max_pages: Optional[int] = 3) -> List[Dict[str, Any]]:
    """Crawls pages starting from BASE_URL following the next link.
    
    Args:
        max_pages: Maximum number of pages to crawl (default: 3 pages for polite scraping).
                   Set to None to scrape all pages.
    """
    all_quotes = []
    current_url = BASE_URL + "/"
    page_count = 0

    print(f"Starting polite scrape on {BASE_URL}...")
    while current_url:
        page_count += 1
        print(f"  Fetching Page {page_count}: {current_url}")
        
        html = fetch_page(current_url)
        if not html:
            print("  Halting crawl due to request failure.")
            break

        quotes, next_href = parse_quotes_from_html(html)
        all_quotes.extend(quotes)
        print(f"  Extracted {len(quotes)} quote(s) from Page {page_count}.")

        if max_pages and page_count >= max_pages:
            print(f"  Reached target limit of {max_pages} pages.")
            break

        if next_href:
            current_url = BASE_URL + next_href
            time.sleep(POLITE_DELAY)  # Polite crawl delay
        else:
            current_url = None

    print(f"Scraping complete! Total quotes extracted: {len(all_quotes)}")
    return all_quotes


# ==============================================================================
# STORAGE & ANALYTICS HELPERS
# ==============================================================================

def save_to_json(data: List[Dict[str, Any]], filepath: str) -> None:
    """Saves records to JSON file with indent=2 and ensure_ascii=False."""
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"Saved {len(data)} records to JSON: {filepath}")


def save_to_text(data: List[Dict[str, Any]], filepath: str) -> None:
    """Saves records to human-readable formatted text file."""
    with open(filepath, "w", encoding="utf-8") as f:
        f.write("=" * 70 + "\n")
        f.write("              SCRAPED QUOTES COLLECTION\n")
        f.write("=" * 70 + "\n\n")
        for idx, item in enumerate(data, start=1):
            f.write(f"[{idx}] \"{item['text']}\"\n")
            f.write(f"     -- Author: {item['author']}\n")
            f.write(f"     -- Tags: {', '.join(item['tags']) if item['tags'] else 'None'}\n\n")
    print(f"Saved human-readable text to: {filepath}")


def print_summary_report(data: List[Dict[str, Any]]) -> None:
    """Calculates and displays summary statistics:
    - Total number of quotes
    - Most quoted author
    - Most common tag
    
    Time Complexity: O(Q) | Space Complexity: O(U)
    """
    if not data:
        print("\nNo quotes available for summary.")
        return

    author_counter = Counter(q["author"] for q in data)
    tag_counter = Counter(tag for q in data for tag in q["tags"])

    total_quotes = len(data)
    most_common_author, author_count = author_counter.most_common(1)[0]
    most_common_tag, tag_count = tag_counter.most_common(1)[0] if tag_counter else ("None", 0)

    print("\n" + "=" * 55)
    print("             SCRAPING SUMMARY REPORT")
    print("=" * 55)
    print(f"Total Quotes Collected : {total_quotes}")
    print(f"Unique Authors         : {len(author_counter)}")
    print(f"Unique Tags            : {len(tag_counter)}")
    print("-" * 55)
    print(f"Most Quoted Author     : {most_common_author} ({author_count} quotes)")
    print(f"Most Common Tag        : '{most_common_tag}' ({tag_count} occurrences)")
    print("=" * 55)


# ==============================================================================
# MAIN ENTRY POINT
# ==============================================================================

def main() -> None:
    """Executes scraping pipeline, saves dual format outputs, and reports summary."""
    output_dir = os.path.dirname(__file__)
    json_path = os.path.join(output_dir, "quotes.json")
    text_path = os.path.join(output_dir, "quotes.txt")

    # Scrape 3 pages (30 quotes) politely with 1-second delay
    quotes_data = scrape_quotes(max_pages=3)

    if quotes_data:
        save_to_json(quotes_data, json_path)
        save_to_text(quotes_data, text_path)
        print_summary_report(quotes_data)


if __name__ == "__main__":
    main()
