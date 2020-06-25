from selenium import webdriver
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait as wdw
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import csv
import re

# search result = div.rc r a
# ignore: https://www.instagram.com/p https://www.instagram.com/explore
# addr: https://www.google.com/search?q=query+here
# nav: tr td a['href']
page_nav = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90]
keywords = []
with open('og_keyword.csv', newline='') as key:
    print("Reading keyword.csv")
    key_data = csv.reader(key)
    for row in key_data:
        keywords.append(row)
global current_acc
current_acc = ""
global driver
driver = ""
global ig_url
ig_url = []
global acc_count
acc_count = 0

def open_driver():
    global driver
    driver = webdriver.Firefox()
    for ind_key in keywords:
        for pg in page_nav:
            search_query = "site:https://www.instagram.com/ " + ''.join(ind_key) + " jakarta&start=" + str(pg)
            driver.get("https://www.google.com/search?q=" + search_query)
            time.sleep(3)
            find_results()
        print(ig_url)
        login()
        print("logged in")
        time.sleep(30)
        global ig_url
        for acc in ig_url:
            get_account(acc)
            time.sleep(30)
        time.sleep(3600)
        ig_url = []

def find_results():
    global driver
    results = driver.find_elements_by_css_selector('div.rc .r a')
    global ig_url
    for rs in results:
        link = rs.get_attribute('href')
        insta = re.match(r'https\:\/\/www\.instagram\.com', link)
        post = re.search(r'p\/', link)
        explore = re.search(r'explore\/', link)
        if insta:
            if post is None and explore is None:
                link_edit = re.sub(r'\/\?.+', '', link)    
                ig_url.append(link_edit)

def get_account(link):
    global driver
    driver.get(link)
    global current_acc
    current_acc = link
    try:
        no_acc_found = driver.find_element_by_css_selector('div.error-container')
        print('Account not found.')
        pass
    except NoSuchElementException:
        try:
            bio_pr = ec.presence_of_element_located((By.CSS_SELECTOR, 'div.-vDIg'))
            wdw(driver, 15).until(bio_pr)
            time.sleep(30)
            bio = driver.find_element_by_css_selector('div.-vDIg')
            rm_d = re.sub(r'\D', '', bio.text)
            prog = re.search(r'(08|628)\d{8,10}', rm_d)
            if prog:
                follower_count = driver.find_element_by_css_selector('ul li a span')
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
                with open('google_instagram_data.csv', 'a+', newline='') as append_data:
                    append_this = csv.writer(append_data)
                    append_this.writerow(raw_data)
                    global acc_count
                    acc_count += 1
                    print(acc_count)
        except IndexError:
            print("no bio found")
            pass
        except ValueError:
            print("follower exceeds 999")
            pass
        except TimeoutException:
            print("blocked, sleep for 2 hours")
            driver.close()
            print(time.asctime())
            time.sleep(7200)
            print("reopening driver")
            global driver
            driver = webdriver.Firefox()
            login()
            get_account(current_acc)
        except NoSuchElementException:
            print("username not found")
            pass

def login():
    global driver
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
    
open_driver()
#driver = webdriver.Firefox()
#login()
#get_account('https://www.instagram.com/_ichsanni')
#time.sleep(5)
#get_account('https://www.instagram.com/titipoigin')
