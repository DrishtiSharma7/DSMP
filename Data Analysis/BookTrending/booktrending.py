"""
Atlantic Books Scraper
Automates browser navigation through Atlantic Books bestsellers collection,
handling infinite scroll / pagination, and saving raw HTML pages.
"""

import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ( NoSuchElementException, StaleElementReferenceException, ElementClickInterceptedException, TimeoutException,)
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

DRIVER_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "chromedriver-mac-arm64", "chromedriver")
s = Service(DRIVER_PATH if os.path.exists(DRIVER_PATH) else "/Users/drishtisharma/Downloads/DSMP/Data Analysis/chromedriver-mac-arm64/chromedriver")
os.makedirs("html_pages", exist_ok=True)

chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
chrome_options.add_argument("--ignore-certificate-errors")
chrome_options.add_argument("--start-maximized")
chrome_options.page_load_strategy = "eager"   # fast navigation without blocking on media

driver = webdriver.Chrome(service=s, options=chrome_options)
driver.set_page_load_timeout(60)

# Next button locators (semantic selectors preferred, position xpath as fallback)
NEXT_XPATH = '//*[@id="shopify-section-template--17889691795607__main"]/div[1]/div[3]/nav[2]/ul/li[8]/a'
NEXT_LOCATORS = [
    (By.CSS_SELECTOR, 'a[rel="next"]'),
    (By.CSS_SELECTOR, 'a[aria-label*="Next" i]'),
    (By.XPATH, '//nav[contains(@class,"pagination")]//a[contains(., "Next") or contains(., "›") or contains(., "»")]'),
    (By.XPATH, '//a[contains(translate(., "NEXT", "next"), "next")]'),
    (By.XPATH, NEXT_XPATH),
]

OUTPUT_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "books_all_pages.html")


def safe_get(url):
    """Open a URL, and if loading is slow, stop loading and carry on."""
    try:
        driver.get(url)
    except TimeoutException:
        print("Page load timed out, stopping load and continuing...")
        driver.execute_script("window.stop();")


# ---------------- preload mask handling ----------------
def wait_for_mask_gone(timeout=30):
    """Wait until the white full-screen 'eb-preload-mask' overlay disappears."""
    try:
        WebDriverWait(driver, timeout).until(
            lambda d: not any(
                el.is_displayed() for el in d.find_elements(By.ID, "eb-preload-mask")
            )
        )
    except TimeoutException:
        print("Preload mask still visible, removing it with JS...")
        driver.execute_script(
            "var m = document.getElementById('eb-preload-mask'); if (m) m.remove();"
        )


def safe_click(xpath, timeout=20):
    """Wait for mask to go, wait for element to be clickable, then click (JS click as fallback)."""
    wait_for_mask_gone()
    el = WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.XPATH, xpath)))
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", el)
    time.sleep(0.5)
    try:
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, xpath))).click()
    except (ElementClickInterceptedException, TimeoutException, StaleElementReferenceException):
        driver.execute_script("arguments[0].click();", el)
# ------------------------------------------------------------


def scroll_to_bottom(step=500, pause=0.4):
    """Scroll slowly until the bottom is reached (handles lazy-loaded content)."""
    last_height = driver.execute_script("return document.body.scrollHeight")
    position = 0
    while True:
        position += step
        driver.execute_script(f"window.scrollTo(0, {position});")
        time.sleep(pause)

        new_height = driver.execute_script("return document.body.scrollHeight")
        # reached the bottom AND page stopped growing
        if position >= new_height:
            time.sleep(1)  # let any lazy content finish loading
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
        last_height = new_height


def next_button_available():
    """Return the Next button if it exists and is clickable, else None."""
    for by, value in NEXT_LOCATORS:
        try:
            elements = driver.find_elements(by, value)
        except NoSuchElementException:
            continue

        for btn in elements:
            disabled = btn.get_attribute("disabled")
            aria_disabled = btn.get_attribute("aria-disabled")
            cls = (btn.get_attribute("class") or "").lower()

            if disabled or aria_disabled == "true" or "disabled" in cls:
                continue
            if not btn.is_enabled():
                continue
            # a real Next link must have an href (when it is an <a> tag)
            if btn.tag_name == "a" and not btn.get_attribute("href"):
                continue
            return btn
    return None


def find_next_with_retry(tries=3):
    """Pagination can load late, so retry a few times before giving up."""
    for _ in range(tries):
        btn = next_button_available()
        if btn is not None:
            return btn
        time.sleep(2)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    return None


def get_product_links():
    """All product links on the current page (Shopify product URLs contain /products/)."""
    return {a.get_attribute("href") for a in driver.find_elements(By.CSS_SELECTOR, 'a[href*="/products/"]')}


def url_with_page(url, n):
    """Return the same URL with ?page=n (keeps any other filters in the URL)."""
    u = urlparse(url)
    q = parse_qs(u.query)
    q["page"] = [str(n)]
    return urlunparse(u._replace(query=urlencode(q, doseq=True)))


def print_pagination_debug():
    """Show what the pagination looks like when Next was not found."""
    print("Current URL:", driver.current_url)
    for nav in driver.find_elements(By.XPATH, '//nav[contains(@class,"pagination") or @aria-label="Pagination"]'):
        print("Pagination HTML:", nav.get_attribute("outerHTML")[:1500])


safe_get("https://atlanticbooks.com/collections")
time.sleep(3)

# Navigate to bestsellers collection
safe_click('//*[@id="site-header-nav"]/nav/ul/li[9]/a')
time.sleep(3)

# Filter / sorting options
safe_click('//*[@id="shopify-section-template--17889691795607__main"]/div[1]/div[3]/nav[1]/div[3]/div/div/button[2]')
time.sleep(3)

# Initialize output file
with open(OUTPUT_FILE, mode='w', encoding='utf-8') as f:
    f.write("")
print("Saving to:", OUTPUT_FILE)

page = 1
while True:
    wait_for_mask_gone()   # make sure page is visible before scrolling
    print(f"Scrolling page {page}...")
    scroll_to_bottom()

    current_links = get_product_links()
    print(f"Page {page}: {len(current_links)} product links | {driver.current_url}")

    # Append this page to the single combined file
    with open(OUTPUT_FILE, mode='a', encoding='utf-8') as f:
        f.write(f"\n<!-- ===== PAGE {page} | {driver.current_url} ===== -->\n")
        f.write(driver.page_source)
        f.write("\n")
    print(f"Appended page {page} to {OUTPUT_FILE}")

    btn = find_next_with_retry()
    print("Next button found:", btn.get_attribute("outerHTML") if btn else None)

    if btn is not None:
        try:
            wait_for_mask_gone()
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn)
            time.sleep(1)
            btn.click()
        except (ElementClickInterceptedException, StaleElementReferenceException, TimeoutException):
            # fallback: JS click if something overlays the button
            driver.execute_script("arguments[0].click();", btn)
    else:
        # button not found, so try the next page by URL before giving up
        print_pagination_debug()
        safe_get(url_with_page(driver.current_url, page + 1))
        time.sleep(3)
        new_links = get_product_links()
        if not new_links or new_links <= current_links:
            print(f"No more pages (page {page + 1} has no new products). Done.")
            break
        print(f"Next button missing, but ?page={page + 1} worked. Continuing.")

    page += 1
    time.sleep(3)  # wait for the next page to load

driver.quit()   # browser closes when scraping is finished (data is already saved in the file)