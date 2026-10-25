
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from html import escape
import time


s = Service("/Users/drishtisharma/Downloads/DSMP/Data Analysis/chromedriver-mac-arm64/chromedriver")

chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
chrome_options.add_argument("--ignore-certificate-errors")
chrome_options.add_argument("--start-maximized")

driver = webdriver.Chrome(service=s, options=chrome_options)
wait = WebDriverWait(driver, 15)

base_url = "https://atlanticbooks.com/collections/bestsellers"


all_pages_html = []

try:
    for page_num in range(1, 17):

        if page_num == 1:
            page_url = base_url
        else:
            page_url = f"{base_url}?page={page_num}"

        driver.get(page_url)
        wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, 'a[href*="/products/"]')
            )
        )

        time.sleep(2)

        print("Scraping page:", page_num)
        print("URL:", driver.current_url)

        page_html = driver.page_source

        all_pages_html.append(
            f"""
            <section class="scraped-page">
                <h2>Page {page_num}</h2>
                <p>Source URL:
                    <a href="{escape(driver.current_url, quote=True)}">
                        {escape(driver.current_url)}
                    </a>
                </p>
                <details>
                    <summary>View original HTML source</summary>
                    <pre>{escape(page_html)}</pre>
                </details>
            </section>
            <hr>
            """
        )

    with open(
        "booktrending.html",
        "w",
        encoding="utf-8"
    ) as f:

        f.write("""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Atlantic Books - All Pages HTML</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    margin: 30px;
                    line-height: 1.5;
                }
                section {
                    margin-bottom: 25px;
                }
                pre {
                    white-space: pre-wrap;
                    overflow-wrap: anywhere;
                    background: #f4f4f4;
                    padding: 15px;
                    border: 1px solid #ddd;
                }
                summary {
                    cursor: pointer;
                    font-weight: bold;
                }
            </style>
        </head>
        <body>
            <h1>Atlantic Books - All Pages</h1>
            <p>Total pages collected: """ + str(len(all_pages_html)) + """</p>
        """)

        for page_html in all_pages_html:
            f.write(page_html)

        f.write("""
        </body>
        </html>
        """)

    print("\nScraping completed successfully!")
    print("Total pages collected:", len(all_pages_html))
    print("File saved: booktrending.html")

finally:
    driver.quit()
