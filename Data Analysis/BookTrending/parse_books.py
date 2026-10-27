import os
import re
import pandas as pd
from bs4 import BeautifulSoup
from urllib.parse import urljoin

BASE_URL = "https://atlanticbooks.com"
HERE = os.path.dirname(os.path.abspath(__file__))
HTML_FILE = os.path.join(HERE, "books_all_pages.html")
CSV_FILE = os.path.join(HERE, "books.csv")
DEBUG_FILE = os.path.join(HERE, "debug_card.html")

PRICE_RE = re.compile(r"(?:₹|Rs\.?|INR|\$)\s?[\d,]+(?:\.\d+)?")
FORMAT_RE = re.compile(r"\b(paperback|hardcover|hardback|board book|boxed set|mass market|spiral|hardbound|paper back)\b", re.I)
PERCENT_RE = re.compile(r"(\d{1,2}(?:\.\d+)?)\s?%")
RATING_RE = re.compile(r"(\d(?:\.\d)?)\s*(?:out of|/)\s*5", re.I)


def to_number(price_text):
    return float(re.sub(r"[^\d.]", "", price_text) or 0)


def find_card(link):
    """Climb up from a product link to the biggest container holding only ONE product."""
    card, node = link, link.parent
    while node is not None and node.name not in ("body", "html"):
        hrefs = {a["href"].split("?")[0] for a in node.select('a[href*="/products/"]')}
        if len(hrefs) > 1:
            break
        card, node = node, node.parent
    return card


def get_title(card):
    h = card.select_one("h1, h2, h3, h4, [class*='title'], [class*='name']")
    if h and h.get_text(strip=True):
        return h.get_text(" ", strip=True)
    titles = [a.get_text(" ", strip=True) for a in card.select('a[href*="/products/"]')]
    return max(titles, key=len) if titles else ""


def get_author(card, title):
    # 1) element whose class/href mentions author/vendor/writer/brand
    for el in card.select("[class*='author'], [class*='vendor'], [class*='writer'], [class*='brand']"):
        t = el.get_text(" ", strip=True)
        if t and t != title:
            return re.sub(r"^\s*by\s+", "", t, flags=re.I)
    for a in card.select('a[href*="vendor"], a[href*="author"]'):
        t = a.get_text(" ", strip=True)
        if t and t != title:
            return t
    # 2) text like "by Author Name"
    m = re.search(r"\bby\s+([A-Z][^|\n]{2,60})", card.get_text("\n", strip=True))
    return m.group(1).strip() if m else ""


def get_rating(card):
    # look in text and in every attribute (aria-label, title, data-rating, style="--rating: 4.5")
    blobs = [card.get_text(" ", strip=True)]
    for el in card.find_all(True):
        for k, v in el.attrs.items():
            if isinstance(v, list):
                v = " ".join(v)
            if any(w in (k + str(v)).lower() for w in ("rating", "star", "review")):
                blobs.append(f"{k}={v}")
    for b in blobs:
        m = RATING_RE.search(b)
        if m:
            return float(m.group(1))
    for b in blobs:
        m = re.search(r"(?:rating|stars?)\D{0,10}(\d(?:\.\d+)?)", b, re.I)
        if m and float(m.group(1)) <= 5:
            return float(m.group(1))
    # fallback: count filled star icons
    filled = card.select("[class*='star'][class*='full'], [class*='star'][class*='filled'], [class*='star'][class*='active']")
    return float(len(filled)) if filled else ""


def get_prices(card):
    text = card.get_text(" ", strip=True)
    all_prices = list(dict.fromkeys(PRICE_RE.findall(text)))
    old = card.select_one("s, del, [class*='compare'], [class*='was'], [class*='old'], [class*='regular']")
    old_price = ""
    if old:
        m = PRICE_RE.search(old.get_text(" ", strip=True))
        old_price = m.group(0) if m else ""
    nums = sorted(all_prices, key=to_number)
    if not old_price and len(nums) > 1:
        old_price = nums[-1]                      # highest price = before discount
    actual = next((p for p in nums if p != old_price), nums[0] if nums else "")
    if old_price and to_number(old_price) < to_number(actual):
        actual, old_price = old_price, actual
    return actual, old_price, all_prices


rows, seen, debug_saved = [], set(), False

with open(HTML_FILE, encoding="utf-8") as f:
    content = f.read()

parts = re.split(r"<!-- ===== PAGE (\d+) \| (.*?) ===== -->", content)

for i in range(1, len(parts), 3):
    page_no, page_url, html = parts[i], parts[i + 1], parts[i + 2]
    soup = BeautifulSoup(html, "html.parser")

    for link in soup.select('a[href*="/products/"]'):
        url = urljoin(BASE_URL, link["href"].split("?")[0])
        if url in seen:
            continue
        seen.add(url)
        card = find_card(link)

        if not debug_saved:
            with open(DEBUG_FILE, "w", encoding="utf-8") as f:
                f.write(str(card))
            debug_saved = True

        text = card.get_text(" ", strip=True)
        title = get_title(card)
        author = get_author(card, title)
        fmt = FORMAT_RE.search(text)
        fmt = fmt.group(1).title() if fmt else ""
        actual, old_price, all_prices = get_prices(card)

        # discount %: from the badge text, else calculated from the two prices
        disc = ""
        for m in PERCENT_RE.finditer(text):
            disc = float(m.group(1))
            break
        if disc == "" and actual and old_price and to_number(old_price) > 0:
            disc = round((1 - to_number(actual) / to_number(old_price)) * 100, 1)

        stars = get_rating(card)

        # Everything left over = bullet points
        used = [title, author, fmt, *all_prices]
        bullets = []
        for line in card.stripped_strings:
            l = line.strip()
            if not l or any(u and u.lower() == l.lower() for u in used):
                continue
            if PRICE_RE.fullmatch(l) or PERCENT_RE.fullmatch(l.replace("off", "").replace("OFF", "").strip()):
                continue
            if RATING_RE.search(l) or re.fullmatch(r"\d(\.\d)?", l):
                continue
            if l.lower() in ("add to cart", "quick view", "sale", "sold out", "by"):
                continue
            bullets.append(l)

        row = {
            "page": int(page_no),
            "title": title,
            "writer": author,
            "format": fmt,
            "actual_price": actual,
            "price_before_discount": old_price,
            "discount_percent": disc,
            "stars": stars,
            "url": url,
        }
        for n, b in enumerate(bullets, 1):
            row[f"bullet_{n}"] = b
        rows.append(row)

df = pd.DataFrame(rows)
df.to_csv(CSV_FILE, index=False, encoding="utf-8-sig")

print(f"Saved {len(df)} books to {CSV_FILE}")
print(df.head(10).to_string())
print("\nEmpty values per column:\n", (df.replace("", pd.NA).isna().sum()))