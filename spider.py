#-*- coding:utf-8 -*-
import requests,sys,json,re,pymongo,urllib
from bs4 import BeautifulSoup
from multiprocessing import Pool
from requests.exceptions import RequestException
from config import *
import os
from hashlib import md5

client=pymongo.MongoClient(MONGO_URL)
db=client[MONGO_DB]

reload(sys)
sys.setdefaultencoding('utf8')



def get_page_index(offset,keyword):
    data={
        'offset': offset,
        'format': 'json',
        'keyword': keyword,
        'autoload': 'true',
        'count': '20',
        'cur_tab': 3
    }
    url='http://www.toutiao.com/search_content/?'+urllib.urlencode(data)
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        print 'wrong'
        return None


def parse_page_index(html):
    data=json.loads(html)
    if data and 'data' in data.keys():
        for item in data.get('data'):
            yield item.get('article_url')

def get_page_detail(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        print '错误'
        return None

def parse_page_detail(html,url):
    soup=BeautifulSoup(html,'lxml')
    title=soup.select('title')[0].get_text()
    images_pattern=re.compile('gallery: (.*?),\n',re.S)
    result=re.search(images_pattern,html)
    if result:
        data=json.loads(result.group(1))
        if data and 'sub_images' in data:
            sub_images=data.get('sub_images')
            images=[item.get('url') for item in sub_images]
            for image in images:
                download_image(image)
            return {
                    'title':title,
                    'url':url,
                    'images':images
                }
def save_to_mongo(result):
    if db[MONGO_TABLE].insert(result):
        print 'sucess'
        return True
    return False

def download_image(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            save_image(response.content)
        return None
    except RequestException:
        print '图片错误'
        return None

def save_image(content):
    file_path='{0}/{1}.{2}'.format(os.getcwd(),md5(content).hexdigest(),'jpg')
    if not os.path.exists(file_path):
        with open(file_path,'wb') as f:
            f.write(content)
            f.close()
def main(offset):
    html=get_page_index(offset,'街拍')
    for url in parse_page_index(html):
        html=get_page_detail(url)
        result=parse_page_detail(html,url)
        if result:
            save_to_mongo(result)

if __name__=='__main__':
    groups=[x*20 for x in range(GROUP_START,GROUP_END+1)]
    pool=Pool()
    try:
        pool.map(main,groups)
    except WindowsError:
        pass