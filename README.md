# Web Scraper for Headlines & Quotes

**InternCircle | Project 04: Python Programming**

A polite, modular web scraper built using `requests` and `BeautifulSoup4` targeting [quotes.toscrape.com](https://quotes.toscrape.com), extracting multi-page quote collections into structured JSON and readable text formats with summary statistics.

---

## ⚡ Time & Space Complexity Analysis

| Component / Phase | Time Complexity | Auxiliary Space Complexity | Analysis |
| :--- | :---: | :---: | :--- |
| **Network Request** | $\mathcal{O}(P)$ | $\mathcal{O}(M)$ | $P$ HTTP round-trips for $P$ pages, rate-limited with a 1-second polite sleep delay. |
| **DOM Parsing (`BeautifulSoup`)** | $\mathcal{O}(N)$ | $\mathcal{O}(N)$ | $N$ character length of the raw HTML text converted to a parse tree. |
| **Record Extraction** | $\mathcal{O}(Q)$ | $\mathcal{O}(Q)$ | Linear iteration over $Q$ quote nodes per page ($Q = 10 \times P$). |
| **Frequency Analysis (`Counter`)** | $\mathcal{O}(Q + T)$ | $\mathcal{O}(A + U)$ | Single linear pass over quotes ($Q$) and tags ($T$); $A$ unique authors, $U$ unique tags. |
| **JSON & Text Serialization** | $\mathcal{O}(Q)$ | $\mathcal{O}(1)$ | Streaming buffered write to disk. |

---

## 🌐 Source & Politeness Rules (Submission Requirement)

### Why the Source is Allowed:
- **Target URL**: `https://quotes.toscrape.com`
- **Authorization**: This website was created and hosted specifically by Zyte (formerly Scrapinghub) as an open sandbox for developers and students to learn and practice web scraping legally without violating copyright or service terms.

### Politeness & Scraping Rules Implemented:
1. **Descriptive User-Agent**: Every request sends a custom header identifying the client as `InternCircle-learning-project (student scraper, polite rate-limited)`.
2. **Rate Limiting**: Includes a mandatory `time.sleep(1.0)` delay between successive page crawls to prevent server stress.
3. **Network Timeouts**: All HTTP requests enforce `timeout=10` seconds to avoid hung sockets.
4. **Error Handling**: Uses `raise_for_status()` and catches `requests.exceptions.RequestException` to handle connection drops or HTTP errors gracefully.
5. **Defensive Parsing**: Validates that HTML elements exist (`if elem is not None`) before calling `.get_text()`.

---

## 📋 Checklist Verification

- [x] **Only allowed sources are scraped**: Scrapes exclusively `quotes.toscrape.com`.
- [x] **Requests use a timeout and a polite delay**: Configured with `timeout=10` and `time.sleep(1.0)`.
- [x] **Errors such as a failed request are handled**: Try/except guards catch connection, timeout, and HTTP status errors.
- [x] **Output is saved as JSON and readable text**: Generates both `quotes.json` and `quotes.txt`.
- [x] **The summary of results is printed**: Outputs total quotes, most quoted author, and most common tag.
- [x] **Your README names the source and your scraping rules**: Fully detailed above.

---

## 🚀 How to Run

```bash
# Run the scraper
python scraper.py

# Run unit tests
python test_scraper.py
```
