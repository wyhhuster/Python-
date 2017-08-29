#-*- coding:utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pyquery import PyQuery as pq
from selenium.common.exceptions import TimeoutException
import re,pymongo

driver=webdriver.Chrome()
wait=WebDriverWait(driver,10)

MONGO_URL='localhost'
MONGO_DB='taobao'
MONGO_TABLE='taobao'
client=pymongo.MongoClient(MONGO_URL)
db=client[MONGO_DB]
def search():
    try:
        driver.get('http://taobao.com')
        input=wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#q")))
        submit=wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,'#J_TSearchForm > div.search-button > button')))
        input.send_keys('美食'.decode('utf-8'))
        submit.click()
        page=wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#mainsrp-pager > div > div > div > div.total')))
        parse_page()
        return page.text
    except TimeoutException:
        search()


def next_page(page_number):
    try:
        input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,                                "#mainsrp-pager > div > div > div > div.form > input")))
        submit = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                            '#mainsrp-pager > div > div > div > div.form > span.btn.J_Submit')))
        input.clear()
        input.send_keys(page_number)
        submit.click()
        wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR,
                                                '#mainsrp-pager > div > div > div > ul > li.item.active > span'),str(page_number)))
        parse_page()

    except TimeoutException:
        next_page()

def parse_page():
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#mainsrp-itemlist .items .item')))
    html=driver.page_source
    doc=pq(html)
    items=doc('#mainsrp-itemlist .items .item').items()
    for item in items:
        results={
            'image':item.find('.pic .img').attr['src'],
            'price':item.find('.price').text(),
            'deal':item.find('.deal-cnt').text()[:-3],
            'title':item.find('.title').text(),
            'shop':item.find('.shop').text(),
            'location':item.find('.location').text()
        }
        save_into_mongo(results)


def save_into_mongo(results):
    if db[MONGO_TABLE].insert(results):
        print 'sucess'
        return True
    return False

def main():
    page=search()
    pattern=re.compile('(\d+)')
    total=int(re.search(pattern,page).group(1))
    for i in range(2,total+1):
        next_page(i)


if __name__=='__main__':
    main()
