import time
from selenium import webdriver
from bs4 import BeautifulSoup as bs
UserAGENT = "Mozilla/5.0 (Windows; U;  Windows NT 10.0; en-US) AppleWebKit/604.3.38 (KHTML, like Gecko) Chrome/68.0.3325.162"


def scrape(url):
    options = webdriver.ChromeOptions()
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--incognito')
    options.add_argument("--user-agent=%s" % (UserAGENT))
    options.add_argument("window-size=1920x1080")
    driver = webdriver.Chrome(chrome_options=options)
    driver.get(url)
    driver.implicitly_wait(10)
    link_a = find_by_xpath_or_none('//*[@id="ip_server"]/li[1]/a', driver)
    link_b = find_by_xpath_or_none('//*[@id="ip_server"]/li[2]/a', driver)
    link_c = find_by_xpath_or_none('//*[@id="ip_server"]/li[3]/a', driver)
    link_list = [link_a, link_b, link_c]
    data = []
    for l in link_list:
        if l:
            close_all_popups(driver)
            l.click()
            time.sleep(1)
            soup = bs(driver.page_source, 'html.parser')
            ifr = soup.find("div", attrs={'id': 'ipplayer_wrapper'}).findChild(
                "iframe").attrs.get("src")
            data.append(ifr)
    driver.quit()
    return data


def find_by_xpath_or_none(xpath, driver):
    try:
        return driver.find_element_by_xpath(xpath)
    except:
        return None


def close_all_popups(driver):
    driver.switch_to_window(driver.window_handles[0])


if __name__ == '__main__':
    print(scrape(input("enter the url:")))
