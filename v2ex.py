#-*- coding:utf-8 -*-
import sys
import re,requests,csv
from bs4 import BeautifulSoup

reload(sys)
sys.setdefaultencoding('utf8')
url='http://www.v2ex.com/?tab=all'
html=requests.get(url).text
soup=BeautifulSoup(html,'html.parser')

articles = []
for article in soup.find_all(class_='cell item'):
    title = article.find(class_='item_title').get_text()
    category = article.find(class_='node').get_text()
    author = re.findall(r'(?<=<a href="/member/).+(?="><img)', str(article))[0]
    u = article.select('.item_title > a')
    link = 'https://www.v2ex.com' + re.findall(r'(?<=href=").+(?=")', str(u))[0]
    articles.append([title, category, author, link])

    f=open('v2ex.csv', 'w')
    writer = csv.writer(f)
    writer.writerow(['文章标题', '分类', '作者', '文章地址'])
    for row in articles:
        writer.writerow(row)

