
import requests
import re
import urllib.request
from bs4 import BeautifulSoup
from skimage import io

import urllib
import os
import cv2

save_image_path='F:\\工作Yi+\\bloody_0330\\normal_images\\man'
keyword='man'
user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36"
headers = {'User-Agent': user_agent, "Upgrade-Insecure-Requests": 1,
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                "Accept-Encoding": "gzip, deflate, sdch",
                "Accept-Language": "zh-CN,zh;q=0.8,en;q=0.6",
                "Cache-Control": "no-cache"}
def flip_pages(page):
    now_page='/search/flip?tn=baiduimage&ie=utf-8&word=%E4%BA%BA%E7%89%A9&pn='+str(page*20)+'&gsm=0&ct=&ic=0&lm=-1&width=0&height=0'

    page_url='http://image.baidu.com'+now_page
    return page_url

def saveImg(imageURL,count):
    try:
        '''r = requests.get(imageURL)
        print(r.status_code)
        print(r.request.url)
        demo = r.text
        html = BeautifulSoup(demo, 'html.parser')
        print(html)'''
        # get image into self.save_image_path directory and rename it by its md5
        req = urllib.request.Request(imageURL,headers=headers)
        data = urllib.request.urlopen(req,timeout=20)
        image_name = "%s\\%s#%d.jpg" % (save_image_path,keyword, count)
        tmp_file = open(image_name, "wb")
        tmp_file.write(data.read())
        tmp_file.close()

        print(u"正在悄悄保存的一张图片为", image_name)
        return 'success'

    except Exception as e:
        return 'failed'
count=0
n_page_url='http://image.baidu.com/search/flip?tn=baiduimage&ie=utf-8&word=%E4%BA%BA%E7%89%A9&pn=0&gsm=0&ct=&ic=0&lm=-1&width=0&height=0'
for page in range(5):
    if page==0:
        page_url=n_page_url
    else:
        page_url=flip_pages(page)
    res = urllib.request.Request(page_url)
    res=urllib.request.urlopen(res)
    html = res.read()
    print(html)
    print ('page is:{}'.format(page))
    obj = re.compile('"thumbURL":"(http://.*?.jpg)"')
    # obj=re.compile('alt=.*\s*src="//.*?\.jpg"')
    imageURLs=re.findall(obj,str(html))
    for image_url in imageURLs:
        #imageURL=image_url.split('src="')[1]
        #imageURL=imageURL.split('"')[0]
        image_url=image_url.strip("'")
        if saveImg(image_url,count)=='success':
            count+=1
        else:
            count+=0






