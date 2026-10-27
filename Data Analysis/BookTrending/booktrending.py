from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time


s = Service("/Users/drishtisharma/Downloads/DSMP/Data Analysis/chromedriver-mac-arm64/chromedriver")

chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
chrome_options.add_argument("--ignore-certificate-errors")
chrome_options.add_argument("--start-maximized")

driver = webdriver.Chrome(service = s, options = chrome_options)
driver.get("https://atlanticbooks.com/collections")
time.sleep(3)

driver.find_element(by = By.XPATH, value = '//*[@id="site-header-nav"]/nav/ul/li[9]/a').click()
time.sleep(3)

driver.find_element(by = By.XPATH, value = '//*[@id="shopify-section-template--17889691795607__main"]/div[1]/div[3]/nav[1]/div[3]/div/div/button[2]').click()
time.sleep(3)

height = driver.execute_script('return document.body.scrollHeight') # Getting the height of entire height until 2nd load
print(height)
time.sleep(5)





driver.quit()    # 1. Scroll slowly to the bottom of the current page