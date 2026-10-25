
from bs4 import BeautifulSoup
import csv
import os

# Input HTML file
html_file = "booktrending.html"

# Output CSV file
csv_file = "atlantic_books.csv"

all_books = []
seen_urls = set()

# Read the combined HTML file
with open(html_file, "r", encoding="utf-8") as file:
    combined_html = file.read()

soup = BeautifulSoup(combined_html, "html.parser")

# Each section contains one saved page
sections = soup.find_all("section", class_="scraped-page")

print("Saved page sections found:", len(sections))

for section in sections:

    heading = section.find("h2")
    page_number = heading.get_text(strip=True) if heading else "Unknown"

    # The original page source is stored inside <pre>
    source_tag = section.find("pre")

    if not source_tag:
        print("HTML source missing for", page_number)
        continue

    original_html = source_tag.get_text()

    # Parse the original webpage HTML
    page_soup = BeautifulSoup(original_html, "html.parser")

    # Find all book product links
    product_links = page_soup.select('a[href*="/products/"]')

    page_count = 0

    for link in product_links:

        url = link.get("href", "").strip()

        # Skip empty or duplicate product URLs
        if not url:
            continue

        if url.startswith("/"):
            url = "https://atlanticbooks.com" + url
        elif url.startswith("//"):
            url = "https:" + url

        if url in seen_urls:
            continue

        # Find the product card
        card = (
            link.find_parent(class_="card-wrapper")
            or link.find_parent(class_="product-card")
            or link.find_parent(class_="grid__item")
        )

        if card is None:
            card = link

        # Extract book title
        title = link.get("title", "").strip()

        if not title:
            title = link.get_text(" ", strip=True)

        if not title and card != link:
            title_tag = card.select_one(
                ".card__heading a, .product-title, h2 a, h3 a"
            )

            if title_tag:
                title = title_tag.get_text(" ", strip=True)

        # Extract price
        price = ""

        price_tag = card.select_one(
            ".price-item--sale, "
            ".price-item--regular, "
            ".price-item"
        )

        if price_tag:
            price = price_tag.get_text(" ", strip=True)

        # Extract all visible text from the product card
        card_text = card.get_text(" ", strip=True)

        # Save record
        all_books.append({
            "page": page_number,
            "title": title,
            "price": price,
            "url": url,
            "card_text": card_text
        })

        seen_urls.add(url)
        page_count += 1

    print(page_number, "- books extracted:", page_count)

# Write records to CSV
with open(
    csv_file,
    "w",
    newline="",
    encoding="utf-8-sig"
) as file:

    fieldnames = [
        "page",
        "title",
        "price",
        "url",
        "card_text"
    ]

    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(all_books)

print("\nConversion completed!")
print("Total unique book URLs:", len(all_books))
print("CSV saved at:", os.path.abspath(csv_file))
