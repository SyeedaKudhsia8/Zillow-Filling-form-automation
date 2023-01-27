from bs4 import BeautifulSoup as bs
import requests as rq
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time

header = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36",
    "Accept-Language" : "en-GB, en-US, q=0.9, en;q=0.8"
}

response = rq.get("https://www.zillow.com/homes/San-Francisco,-CA_rb/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22usersSearchTerm%22%3A%22San%20Francisco%2C%20CA%22%2C%22mapBounds%22%3A%7B%22west%22%3A-122.55177535009766%2C%22east%22%3A-122.31488264990234%2C%22south%22%3A37.69926912019228%2C%22north%22%3A37.851235694487485%7D%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A20330%2C%22regionType%22%3A6%7D%5D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22pmf%22%3A%7B%22value%22%3Afalse%7D%2C%22pf%22%3A%7B%22value%22%3Afalse%7D%2C%22mp%22%3A%7B%22max%22%3A3000%7D%2C%22price%22%3A%7B%22max%22%3A872627%7D%2C%22beds%22%3A%7B%22min%22%3A1%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A12%7D",
                  headers=header)

data = response.text
soup = bs(data, "html.parser")

all_link_elements = soup.select(".property-card-data a")

all_links = []
for link in all_link_elements:
    href = link["href"]
    #print(href)
    if "http" not in href:
        all_links.append(f"https://www.zillow.com{href}")
    else:
        all_links.append(href)

#print(all_links)

all_address_elements = soup.select(".property-card-link address")
all_addresses = [address.get_text().split(" | ")[-1] for address in all_address_elements]
#print(all_addresses)

all_price_elements = soup.select(".wgiFT span")
all_prices = []

for element in all_price_elements:
    all_prices.append(element.text.replace(" ", "")[:6])



#print(all_prices)


# create a spreadsheet using google form
driver = webdriver.Chrome(ChromeDriverManager().install())

for n in range(len(all_links)):
    # Substitute your own Google form URL here
    driver.get("https://docs.google.com/forms/d/e/1FAIpQLScxSa7iGiIaC3LlvIpX0uobWctSx1XYfcD9tMoHe9Fw-Td58w/viewform")

    time.sleep(2)
    address = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
    price = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    link = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
    submit_button = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div/span')

    address.send_keys(all_addresses[n])
    time.sleep(1)
    price.send_keys(all_prices[n])
    time.sleep(1)
    link.send_keys(all_links[n])
    time.sleep(1)
    submit_button.click()