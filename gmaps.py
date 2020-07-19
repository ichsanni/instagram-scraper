from selenium import webdriver
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import time
import re
import csv

# selatan rendang
locations = ["utara", "pusat", "selatan", "barat", "timur"]
keywords = []
with open('gmaps_keyword.csv', newline='') as key:
    print("Reading keyword.csv")
    key_data = csv.reader(key)
    for row in key_data:
        keywords.append(row)
global driver
driver = ""
global count
count = 0
global dcount
dcount = 1

def card_scraping(link="", recursion=False):
    global driver
    if recursion:
        driver = webdriver.Firefox()
        driver.get(link)
    title_present = ec.presence_of_element_located((By.CSS_SELECTOR, 'h3.section-result-title span'))
    WebDriverWait(driver, 60).until(title_present)
    time.sleep(5)
    next_button_present = ec.presence_of_element_located((By.CSS_SELECTOR, "button[id$='_section-pagination-button-next']"))
    try:
        WebDriverWait(driver, 30).until(next_button_present)
        global count
        if count < 3:
            count += 1
            get_card_details()
            #next_button = driver.find_element_by_css_selector("button[id$='_section-pagination-button-next']")
            try:
                next_button = driver.find_element_by_css_selector("button[id$='_section-pagination-button-next']")
            except NoSuchElementException:
                time.sleep(60)
                next_button = driver.find_element_by_css_selector("button[jsaction='pane.paginationSection.nextPage']")
            driver.execute_script("arguments[0].click();", next_button)
            print("next button pressed")
            print(time.asctime())
            card_scraping()
        else:
            count = 0
            driver.close()
    except TimeoutException:
        driver.close()
        pass

def get_card_details():
    try:
        global dcount
        global driver
        for item in range(20):
            raw_data = []
            titles = driver.find_elements_by_css_selector("h3.section-result-title span")
            driver.execute_script("arguments[0].click();", titles[item])
            txt_title = titles[item].text
            print(str(dcount) + ". " + txt_title)
            dcount += 1
            details_present = ec.presence_of_element_located((By.CSS_SELECTOR, 'div.gm2-body-2'))
            WebDriverWait(driver, 120).until(details_present)
            needed_data = [1, 3, 5, 6, 7]
            found_details = driver.find_elements_by_css_selector('div.gm2-body-2')
            current = driver.current_url
            link = re.sub(r'\@.+', '', current)
            print(link)
            image_avail = ec.presence_of_element_located((By.CSS_SELECTOR, 'div.section-hero-header-image div button img'))
            WebDriverWait(driver, 120).until(image_avail)
            image_link = driver.find_element_by_css_selector('div.section-hero-header-image div button img').get_attribute('src')
            print(image_link)
            raw_data.append(txt_title)
            raw_data.append(link)
            raw_data.append(image_link)
            for i in needed_data:
                txt_detail = found_details[i].text
                print(txt_detail)
                raw_data.append(txt_detail)
            with open('gmaps_data2.csv', 'a+', newline='') as append_data:
                append_this = csv.writer(append_data)
                append_this.writerow(raw_data)
            button_present = ec.presence_of_element_located((By.CSS_SELECTOR, 'button.section-back-to-list-button'))
            WebDriverWait(driver, 60).until(button_present)
            back = driver.find_element_by_css_selector('button.section-back-to-list-button')
            driver.execute_script("arguments[0].click();", back)
            print("-----------")
            time.sleep(6)
    except IndexError:
        button_present = ec.presence_of_element_located((By.CSS_SELECTOR, 'button.section-back-to-list-button'))
        WebDriverWait(driver, 60).until(button_present)
        back = driver.find_element_by_css_selector('button.section-back-to-list-button')
        driver.execute_script("arguments[0].click();", back)
        print("-----------")
        time.sleep(6)
        pass

for loc in locations:
    for key in keywords:
        concat = ''.join(key) + " rumahan jakarta " + str(loc)
        final_query = re.sub("\s", "+", concat)
        print("query: " + final_query)
        address = "https://www.google.co.id/maps/search/" + final_query
        card_scraping(address, True)

