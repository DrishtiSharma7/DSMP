# Atlantic Books Trending — Scraping & Data Cleaning Pipeline

This project scrapes book listings from Atlantic Books, parses raw HTML cards into structured records, and cleans/normalizes the dataset for exploratory data analysis.

---

## Project Structure

```text
BookTrending/
├── booktrending.py             # Selenium scraper (saves multi-page HTML)
├── parse_books.py              # BeautifulSoup parser (HTML -> books.csv)
├── booktrending_da.ipynb       # Data cleaning & preprocessing notebook
├── books_all_pages.html        # Raw scraped HTML pages
├── books.csv                   # Parsed raw dataset (945 records)
└── atlantic_books_public.csv   # Cleaned, standardized public dataset (944 records)
```

---

## Execution Sequence

### 1. Web Scraping
```bash
python booktrending.py
```
- Automates Chrome using Selenium to navigate through the Atlantic Books Bestsellers collection.
- Handles infinite scroll / pagination and saves raw page source to `books_all_pages.html`.

### 2. Card Parsing & Extraction
```bash
python parse_books.py
```
- Extracts product titles, authors, formats, pricing, discount percentages, ratings, and raw bullet points.
- Outputs raw structured dataset to `books.csv`.

### 3. Data Cleaning & Analysis
Open and run `booktrending_da.ipynb` sequentially:
1. **Initial Inspection**: Load `books.csv` and verify dimensions.
2. **Column Pruning**: Drop frontend UI artifacts (`bullet_1` through `bullet_8`) and `url`.
3. **Column Realignment**: Shift overflow metadata caused by customer review badges back into `bullet_9`.
4. **Metadata Extraction**: Parse `author`, `publisher`, and `publisher_imprint` from consolidated strings.
5. **Shift Correction**: Correct rows where publisher data was shifted into the author column.
6. **Classification Parsing**: Extract `subject` and `bisac` categories with regex boundary detection.
7. **Price Cleaning**: Strip currency symbols (`₹`, `,`), convert USD entries to INR, and cast to integer.
8. **Missing Value Imputation**: Fill categorical nulls (`unknown`, `unknown publisher`) and lowercase strings.
9. **Summary Statistics**: Run descriptive checks and inspect top-priced books.
10. **Data Export**: Save final dataset to `atlantic_books_public.csv`.
