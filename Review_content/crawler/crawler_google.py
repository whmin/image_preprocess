#coding=utf-8
import requests
import re
import urllib.request
from bs4 import BeautifulSoup
from skimage import io
import os
import cv2
import chardet
import time

def save(opener,URL,keyword,count,page):
    save_image_path="D:\\Yi+\\porn_images\\pichunter1"
    try:
        req = urllib.request.Request(URL)
        data = urllib.request.urlopen(req, timeout=20)
        image_name = "%s\\%s#%d_page%d.jpg" % (save_image_path,keyword, count,page)
        tmp_file = open(image_name, "wb")
        tmp_file.write(data.read())
        tmp_file.close()

        print(u"正在悄悄保存的一张图片为", image_name)
        return 'success'

    except Exception as e:
        return 'failed'
def flip_page(base_url,n):
    page_url=base_url+str(n)
    return page_url

def main():
    proxy = urllib.request.ProxyHandler({'https': '127.0.0.1:1080'})
    opener = urllib.request.build_opener(proxy)
    opener.addheaders = [('User-Agent',
                          'Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11')]
    base_url='https://www.pichunter.com/tags/all/Beautiful/'
    count = 20221
    keyword = "porn"
    for page in range(383, 400):
        print ("current page is :",page)
        try:
            Page_URL=flip_page(base_url,page)
            html = opener.open(Page_URL).read()
            charset = chardet.detect(html)['encoding']
            #print(html.decode(charset).encode('GB18030'))
            soup=BeautifulSoup(html,'lxml')
            #print (soup)
            imgs=soup.select('body > div.mainContainer > div.dynamicRow.infiniteScroll > div > div.thumbtable > a > img')
            print (imgs)
            # f18277616 > a > img
            for img in imgs:
                #time.sleep(2)
                url=img['src']
                try:
                    if url[-5]!='i':
                        print (url)
                        save(opener, url, keyword, count,page)
                        count += 1
                except:
                    pass
        except:
            pass
    # photo_16565102_199857552 > div > a
    '''
    obj = re.compile("(https://.*?.jpg)")
    # obj=re.compile('alt=.*\s*src="//.*?\.jpg"')
    imageURLs = re.findall(obj, str(html))
    keyword="porn"
    count=0
    for image_url in imageURLs[60:]:
        # imageURL=image_url.split('src="')[1]
        # imageURL=imageURL.split('"')[0]
        image_url = image_url.strip("'")
        print(image_url)
        count+=1
        save(opener,image_url,keyword,count)
'''

if __name__=="__main__":
    main()