from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait as wdw
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import csv
import re

# hoxx auth id = zbd-4sabl-zw
keywords = []
global account_scraped
account_scraped = 0
with open('keyword.csv', newline='') as key:
    print("Reading keyword.csv")
    key_data = csv.reader(key)
    for row in key_data:
        keywords.append(row)
global current_acc
current_acc = ""
global driver
driver = ""
global iteration_count
iteration_count = 0


def open_driver(first_login=False):
    global driver
    driver = webdriver.Firefox()
    driver.get("https://www.instagram.com/accounts/login/")
    login = ec.presence_of_element_located((By.NAME, 'username'))
    wdw(driver, 15).until(login)
    uname_field = driver.find_element_by_name('username')
    username = '_sys32_exe'
    for i in username:
        uname_field.send_keys(i)
        time.sleep(0.2)
    pword_field = driver.find_element_by_name('password')
    password = 'sivispacem'
    for i in password:
        pword_field.send_keys(i)
        time.sleep(0.4)
    pword_field.send_keys(Keys.ENTER)
    print("Successfully logged in.")
    time.sleep(30)
    if first_login:
        driver.get("https://www.instagram.com/")
        not_now = driver.find_elements_by_css_selector('div[role="dialog"] div div div button')
        driver.execute_script("arguments[0].click();", not_now[1])
        global iteration_count
        for query in keywords:
            city = ["Bekasi","Tangerang","Tangsel","Depok","Bogor","Jakarta"]
            for c in city:
                q = ''.join(query) + " " + c
                search(q)
                driver.close()
                print(c + " has finished scraping, moving on.")
                print(time.asctime())
                time.sleep(1800)
                open_driver()


def search(kword):
    target_addr = []
    global driver
    search_bar = driver.find_element_by_css_selector('input[type="text"]')
    search_bar.send_keys(kword)
    print("Starts searching " + str(kword))
    acc_pr = ec.presence_of_element_located((By.CSS_SELECTOR, 'a.yCE8d'))
    wdw(driver, 15).until(acc_pr)
    time.sleep(5)
    account_lists = driver.find_elements_by_css_selector('a.yCE8d')
    for a in account_lists:
        target_addr.append(a.get_attribute('href'))
    print("total acc: " + str(len(target_addr)))
    for addr in target_addr:
        escape_hashtag = re.search('/explore/', addr)
        if escape_hashtag is None:
            get_account(addr)


def get_account(link):
    global driver
    try:
        driver.get(link)
        global current_acc
        current_acc = link
        bio_pr = ec.presence_of_element_located((By.CSS_SELECTOR, 'div.-vDIg'))
        wdw(driver, 15).until(bio_pr)
        time.sleep(15)
        bio = driver.find_element_by_css_selector('div.-vDIg')
        rm_d = re.sub(r'\D', '', bio.text)
        prog = re.search(r'(08|628)\d{8,10}', rm_d)
        if prog:
            follower_count = driver.find_element_by_css_selector('span.g47SY')
            fol = int(follower_count.text)
            acc_name = driver.find_element_by_css_selector('h2')
            rm_nl = re.sub(r'\n', '', bio.text)
            uni_ascii = rm_nl.encode('ascii', 'ignore')
            raw_data = []
            raw_data.append(link)
            raw_data.append(acc_name.text)
            raw_data.append(fol)
            raw_data.append(prog.group())
            raw_data.append(uni_ascii)
            print(raw_data)
            time.sleep(30)
            with open('instagram_data12.csv', 'a+', newline='') as append_data:
                append_this = csv.writer(append_data)
                append_this.writerow(raw_data)
            global account_scraped
            account_scraped += 1
            print(account_scraped)
            time.sleep(15)
    except IndexError:
        print("no bio found")
    except ValueError:
        print("follower exceeds 999")
    except TimeoutException:
        print("blocked, sleep for 2 hours")
        driver.close()
        print(time.asctime())
        time.sleep(7200)
        print("reopening driver")
        open_driver()
        get_account(current_acc)
    except NoSuchElementException as nsee:
        print(nsee)
        print("user name not found")


open_driver(True)
# last things last
print("Finished.")
time.sleep(5)
driver.close()
