#coding = utf-8
import urllib
import re

def getHtml(url):
    page = urllib.urlopen(url)
    html = page.read()
    return html

def getImg(html):
    reg = 'src="(.+?\.jpg)" '
    imgre = re.compile(reg)
    imglist = re.findall(imgre, html)
    x=0
    for imgurl in imglist:   
        urllib.urlretrieve(imgurl, 'D:\Python27\picture\%s.jpg' % x)
        x+=1
    

html = getHtml("http://tieba.baidu.com/p/5237993377")

print getImg(html)
print 'finished'
