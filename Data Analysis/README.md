# Books Price & Rating Analysis

An exploratory data analysis of book pricing, discounts and ratings, using data collected from the Atlantic Books website via web scraping.

## Project Overview

This project covers the full workflow: scraping book listings, cleaning the data, and analysing how price, discount, format and subject relate to customer ratings.

##  Data Source

- **Website:** Atlantic Books (https://atlanticbooks.com/)
- **Collected on:** [27/OCT/2026]
- **Method:** Web scraping with Python (`requests` / `BeautifulSoup`) 
- **Purpose:** Educational and portfolio use only

> **Note:** The raw dataset is **not redistributed** in this repository. Run `scraper.py` to collect the data yourself, and please respect the website's Terms of Service and `robots.txt`.

## 🧾 Dataset Columns

| Column | Description |
|---|---|
| `page` | Number of pages in the book |
| `title` | Book title |
| `writer` | Author name |
| `format` | Book format (e.g., Hardcover, Paperback) |
| `actual_price` | Current selling price |
| `price_before_discount` | Original price before discount |
| `discount_percent` | Discount percentage |
| `stars` | Average customer rating |
| `publisher` | Publisher name |
| `publisher_imprint` | Publisher imprint |
| `subject` | Book subject / category |
| `bisac` | BISAC subject code |

## 🎯 Objectives

1. Clean and prepare the scraped data for analysis
2. Understand the distribution of prices, discounts and ratings
3. Compare pricing across formats, publishers and subjects
4. Check whether price or discount is related to ratings

## 🔧 Approach

1. **Data collection:** scraping book listings
2. **Data cleaning:** handling missing values, duplicates, wrong data types, price formatting
3. **Exploratory data analysis:** summary statistics and visualisations
4. **Insights:** key findings and conclusions

## 📊 Key Findings

> Replace with your actual results.

- Finding 1: [e.g., Average discount is X% across all books]
- Finding 2: [e.g., Hardcover books are priced higher than paperbacks on average]
- Finding 3: [e.g., Subject Y has the highest average rating]

## 🛠️ Tools & Libraries

- Python
- Pandas, NumPy
- Matplotlib, Seaborn
- Requests, BeautifulSoup
- Jupyter Notebook

## 📁 Repository Structure

```
books-price-analysis/
├── scraper.py            # Web scraping script
├── analysis.ipynb        # Cleaning + EDA notebook
├── sample_data.csv       # Small sample (optional, 10-20 rows)
├── requirements.txt      # Python dependencies
└── README.md
```

## ▶️ How to Run

```bash
# 1. Clone the repository
git clone https://github.com/[your-username]/books-price-analysis.git
cd books-price-analysis

# 2. Install dependencies
pip install -r requirements.txt

# 3. Collect the data (check the site's ToS first)
python scraper.py

# 4. Open the notebook
jupyter notebook analysis.ipynb
```

## ⚠️ Disclaimer

This project is for educational purposes. All book information belongs to its respective owners and the Atlantic Books website. No ownership of the source data is claimed.

## 👤 Author

**[Your Name]**
- GitHub: [@your-username](https://github.com/your-username)
- LinkedIn: [add link]

⭐ If you found this project useful, consider giving it a star!