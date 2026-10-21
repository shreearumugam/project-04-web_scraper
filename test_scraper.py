"""Unit tests for Project 04: Web Scraper for Headlines & Quotes."""

import json
import os
import unittest
from scraper import (
    parse_quotes_from_html,
    save_to_json,
    save_to_text,
)


SAMPLE_HTML = """
<html>
  <body>
    <div class="quote">
      <span class="text">"Life is what happens to us while we are making other plans."</span>
      <small class="author">Allen Saunders</small>
      <div class="tags">
        <a class="tag" href="/tag/fate/">fate</a>
        <a class="tag" href="/tag/life/">life</a>
      </div>
    </div>
    <div class="quote">
      <span class="text">"The opposite of love is not hate, it's indifference."</span>
      <small class="author">Elie Wiesel</small>
      <div class="tags">
        <a class="tag" href="/tag/hate/">hate</a>
        <a class="tag" href="/tag/indifference/">indifference</a>
        <a class="tag" href="/tag/love/">love</a>
      </div>
    </div>
    <div class="quote">
      <span class="text">"A day without sunshine is like, you know, night."</span>
      <small class="author">Steve Martin</small>
      <div class="tags">
        <a class="tag" href="/tag/humor/">humor</a>
      </div>
    </div>
    <ul class="pager">
      <li class="next">
        <a href="/page/2/">Next <span aria-hidden="true">&rarr;</span></a>
      </li>
    </ul>
  </body>
</html>
"""


class TestScraper(unittest.TestCase):
    def test_parse_quotes_from_html(self):
        quotes, next_url = parse_quotes_from_html(SAMPLE_HTML)
        self.assertEqual(len(quotes), 3)
        self.assertEqual(quotes[0]["author"], "Allen Saunders")
        self.assertIn("life", quotes[0]["tags"])
        self.assertEqual(next_url, "/page/2/")

    def test_missing_elements_handled_safely(self):
        broken_html = '<div class="quote"><span class="text">Only text</span></div>'
        quotes, next_url = parse_quotes_from_html(broken_html)
        self.assertEqual(len(quotes), 1)
        self.assertEqual(quotes[0]["author"], "Unknown")
        self.assertEqual(quotes[0]["tags"], [])
        self.assertIsNone(next_url)

    def test_save_json_and_text(self):
        test_dir = os.path.dirname(__file__)
        temp_json = os.path.join(test_dir, "temp_quotes.json")
        temp_txt = os.path.join(test_dir, "temp_quotes.txt")

        quotes, _ = parse_quotes_from_html(SAMPLE_HTML)
        save_to_json(quotes, temp_json)
        save_to_text(quotes, temp_txt)

        self.assertTrue(os.path.exists(temp_json))
        self.assertTrue(os.path.exists(temp_txt))

        with open(temp_json, "r", encoding="utf-8") as f:
            data = json.load(f)
            self.assertEqual(len(data), 3)

        # Clean up
        os.remove(temp_json)
        os.remove(temp_txt)


if __name__ == "__main__":
    unittest.main()
