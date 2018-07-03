import os
import time

from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import dbmanage
import upload
UserAGENT = "Mozilla/5.0 (Windows; U;  Windows NT 10.0; en-US) AppleWebKit/604.3.38 (KHTML, like Gecko) Chrome/68.0.3325.162"


def scrape(url):
    options = webdriver.ChromeOptions()
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--incognito')
    options.add_argument("headless")
    options.add_argument(
        "--user-agent=Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3526.73 Safari/537.36")
    options.add_argument("window-size=1920x1080")
    print("opening url")
    try:
        capa = DesiredCapabilities.CHROME
        capa["pageLoadStrategy"] = "none"
        driver = webdriver.Chrome(
            chrome_options=options, desired_capabilities=capa)
        wait = WebDriverWait(driver, 20)
        driver.get(url)
        wait.until(EC.presence_of_element_located(
            (By.ID, 'ip_server')))
        driver.execute_script("window.stop();")
    except Exception as e:
        raise e
    driver.implicitly_wait(5)
    print("Page Loaded")
    l = 0
    tr_ = True
    data = []
    while l <= 2:
        close_all_popups(driver)
        print("Clicking Element")
        driver.execute_script('''try{
        var a = document.getElementById("ip_server").children;
        a[%d].children[0].click();}catch(e){console.log(e)}
        ''' % (l))
        close_all_popups(driver)
        time.sleep(2)
        driver.implicitly_wait(2)
        soup = bs(driver.page_source, 'html.parser')
        try:
            ifr = soup.find("div", attrs={'id': 'ipplayer_wrapper'}).findChild(
                "iframe").attrs.get("src")
        except:
            if tr_:
                l, tr_ = len(data), False
                print("Retrying")
                continue
            else:
                raise Exception("Recursion limit")
        ifr = ifr.replace("http://", "https://")
        print("URL:", ifr)
        if ifr not in data:
            data.append(ifr)
        l += 1
    driver.quit()
    if len(data) != 3:
        nones = [None]*(3-len(data))
        for i in nones:
            data.append(i)
    return data


def find_by_xpath_or_none(xpath, driver):
    try:
        return driver.find_element_by_xpath(xpath)
    except:
        return None


def close_all_popups(driver):
    driver.switch_to_window(driver.window_handles[0])


if __name__ == '__main__':
    data = scrape(input("enter the url:"))
    print(data)
    yn = input("Should I Add These Links?(y/n)").lower()
    if yn == "y":
        name = input("Enter The Name:")
        thumb = upload.upload(
            input("Enter the thumbnail url:")).get("secure_url")
        send = (name, *data, thumb)
        print("Data Will Look Like This:", send)
        print(dbmanage.add_to_db(send))
    else:
        print("Bye")
        exit()
