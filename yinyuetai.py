#-*- coding:utf-8 -*-
from bs4 import BeautifulSoup
import csv,requests,urllib2,urllib,sys,pymongo,csv
from config1 import *

reload(sys)
sys.setdefaultencoding('utf8')
MONGO_URL='localhost'
MONGO_DB='yinyuetai'
MONGO_TABLE='yinyuetai'
client=pymongo.MongoClient(MONGO_URL)
db=client[MONGO_DB]

def geturls(page):
    urls=[]
    for i in range(1,page):
       url='http://vchart.yinyuetai.com/vchart/trends?area=ML&page='+str(i)
       urls.append(url)
    return urls

def get_html_page(url):
    headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
             'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'}
    request=urllib2.Request(url.encode('utf-8'),headers=headers)
    response=urllib2.urlopen(request)
    html=response.read()
    return html

def parse_page(html):
    f=open('yinyuetai.csv','w')
    writer=csv.writer(f)
    writer.writerow(['MV名称','发布时间','作者','评分','排名','链接'])
    musics=[]
    soup=BeautifulSoup(html,'html.parser')
    items=soup.find_all('li',attrs={'class':'vitem'})
    for item in items:
        if item.find('h3',attrs={'class':'asc_score'}):
            score=item.find('h3',attrs={'class':'asc_score'}).get_text()
        else:
            score=item.find('h3',attrs={'class':'desc_score'}).get_text()
        rank=item.find('div',attrs={'class':'top_num'}).get_text()
        title=item.find('a',attrs={'class':'mvname'}).get_text()
        author=item.find('a',attrs={'class':'special'}).get_text()
        time=item.find('p',attrs={'class':'c9'}).get_text()[5:]
        url=item.find('a').attrs['href']
        musics.append([title,time,author,score,rank,time])
        for row in musics:
            writer.writerow(row)
        results={
            'MV名称':title,
            '发布时间':time,
            '作者':author,
            '评分':score,
            '排名':rank,
            '链接':url
        }
        save_into_mongodb(results)

def save_into_mongodb(results):
    if db[MONGO_TABLE].insert(results):
        print 'sucess'
        return True
    return False


def main():
    page=4
    urls=geturls(page)
    for url in urls:
        html=get_html_page(url)
        parse_page(html)

if __name__=='__main__':
    main()
