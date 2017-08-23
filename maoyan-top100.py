from bs4 import BeautifulSoup
import csv,urllib,sys
reload(sys)
sys.setdefaultencoding('utf8')
f=open('maoyan.csv','w')
writer=csv.writer(f)
writer.writerow(['rank','name','star','releasetime','score'])
def find_one_page(url):
    movie=[]
    html=urllib.urlopen(url).read()
    soup=BeautifulSoup(html,'html.parser')
    items=soup.find_all('dd')
    for item in items:
        rank=item.find('i',attrs={'class':'board-index'}).text
        name=item.find('p',attrs={'class':'name'}).text
        star=item.find('p',attrs={'class':'star'}).text.strip()[3:]
        releasetime=item.find('p',attrs={'class':'releasetime'}).text[5:]
        score=item.find('i',attrs={'class':'integer'}).text+item.find('i',attrs={'class':'fraction'}).text
        movie.append([rank,name,star,releasetime,score])
    for row in movie:
        writer.writerow(row)

for i in range(0,10):
    if i==0:
        url='http://maoyan.com/board/4?'
        find_one_page(url)
    else:
        url=('http://maoyan.com/board/4?offset=%d') % (i*10)
        find_one_page(url)