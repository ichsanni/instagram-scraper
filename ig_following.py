from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait as wdw
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import csv
import re


global finished_acc
finished_acc = []
global crawling_list
crawling_list = []
global new_acc
new_acc = []
global following_list
following_list = []
global account_scraped
account_scraped = 0
global current_acc
current_acc = ""
global driver
driver = ""
global iteration_count
iteration_count = 0


def open_driver(first_login=False): 
    with open('following_acc.csv', 'r',  newline='') as key:
        print("Reading following_acc.csv")
        key_data = csv.reader(key)
        for row in key_data:
            detect = re.search(r'N', row[1])
            if detect is not None:
                global crawling_list
                crawling_list.append(row)
            else:
                global finished_acc
                finished_acc.append(row)
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
    time.sleep(15)
    if first_login:
        see_following()

def see_following():
    global current_acc
    global finished_acc
    global crawling_list
    global driver
    for acc in crawling_list:
        finished_acc.append([acc[0], 'C'])
        str_acc = ''.join(acc[0])
        fixed_str = re.sub(r'\s*', '',  str_acc)
        link = "https://www.instagram.com/" + fixed_str
        driver.get(link)
        time.sleep(5)
        following_button = driver.find_element_by_css_selector("a.-nal3[href='/"+ fixed_str + "/following/'] span")
        following_amount = following_button.text
        driver.execute_script("arguments[0].click();", following_button)
        time.sleep(5)
        display = 0
        print("following amount: " + following_amount)
        try:
            while display < int(following_amount):
                if display < 100:
                    first = driver.find_elements_by_css_selector("a.FPmhX")
                    first[0].send_keys(Keys.PAGE_DOWN * 5)
                    time.sleep(5)
                    display = len(first)
                    print("display: " + str(display))
                else:
                    break
        except ValueError as val:
            print(val)
            print("passing")
            pass
        get_following = driver.find_elements_by_css_selector("a.FPmhX")
        global following_list
        for z in get_following:
            following_list.append(z.get_attribute('href'))
        for a in following_list:
            current_acc = a
            get_account(current_acc)
        following_list = []
        time.sleep(5)

def get_account(link):
    global driver
    try:
        driver.get(link)
        global current_acc
        current_acc = link
        bio_pr = ec.presence_of_element_located((By.CSS_SELECTOR, 'div.-vDIg'))
        wdw(driver, 15).until(bio_pr)
        time.sleep(45)
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
            global new_acc
            new_acc.append([acc_name.text, 'N'])
            with open('instagram_data8.csv', 'a+', newline='') as append_data:
                append_this = csv.writer(append_data)
                append_this.writerow(raw_data)
            time.sleep(15)
            global account_scraped
            account_scraped += 1
            print(account_scraped)
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
        time.sleep(10800)
        print("reopening driver")
        open_driver()
        get_account(current_acc)
    except NoSuchElementException:
        print("user name not found")
        pass

try:
    while True:
        open_driver(True)
        driver.close()
        print(time.asctime())
        with open('following_acc.csv', 'w', newline='') as n:
            new_list = csv.writer(n)
            global finished_acc
            new_list.writerows(finished_acc)
            finished_acc = []
            global crawling_list
            new_list.writerows(crawling_list)
            crawling_list = []
            global new_acc
            new_list.writerows(new_acc)
            new_acc = []
        time.sleep(3600)
except Exception as e:
    with open('following_acc.csv', 'w', newline='')as n:
        new_list = csv.writer(n)
        global finished_acc
        new_list.writerows(finished_acc)
        finished_acc = []
        global crawling_list
        new_list.writerows(crawling_list)
        crawling_list = []
        global new_acc
        new_list.writerows(new_acc)
        new_acc = []
        print(e)


