# coding=utf-8
import os
from flask import Flask, request
import urllib.request
from hashlib import md5
import json
import time
import cv2
import shutil
import uuid
import numpy as np
#import skvideo.io
import tensorflow as tf
import math
import requests
slim = tf.contrib.slim

app = Flask(__name__)

# MODEL_PATH_TERROR = '/home/baoming/save_model/terror/terror-150000'
MODEL_PATH_TERROR = 'D:\\Yi+\\terror_model\\terror-150000'

def _image_preprocess(image):
    image = cv2.resize(image, (app.train_image_size, app.train_image_size))
    image = (image / 255. - 0.5) * 2.0
    image = np.expand_dims(image, 0)
    return image


@app.route('/blood/process', methods=['POST'])
def terror_process():
    ######得到表单数据
    url = request.form.get('url')#"http://pic2.16pic.com/00/12/14/16pic_1214635_b.jpg"#
    TIMESTAMP = request.form.get('TIMESTAMP')#time.time()#
    task_id =request.form.get('task_id') #"user_id"#
    f = urllib.request.urlopen(url)#.encode('utf-8')
    file_type =f.headers['Content-Type'].split('/')[1] #f.info().type#"image"#
    size = f.headers['content-length']
####获取这个文件并下载下来
    filename = os.path.join('D:\\Yi+\\test', str(task_id + '.' +file_type))
    with open(filename, "wb") as local_file:
        local_file.write(f.read())
        print (f.read)
    #file_size = os.path.getsize(filename)
    result_dict = {
        "task_status": 1,
        "task_id": task_id,
        "video_url": url,
        #"video_size": file_size,
        "timestamp": TIMESTAMP
    }
    if file_type == 'jpeg':
        image = cv2.imread(filename)
        image = _image_preprocess(image)
        img=image
        detect_result =app.detect_terror(img)[0]
        result_dict["video_duration"] = None
        index_ = np.argmax(detect_result)
        result_dict["video_results"] = [index_, float(detect_result[index_])]
    else:
        print ("type error")

###########dumps将字典类型数据转换成字符串，loads将字符串转换成字典类型
    return json.dumps(result_dict)


@app.route('/test/xiang', methods=['POST'])
def hello():
    pp = request.form.get('name')
    print(pp,'ddd')
    return "Hello"

if __name__ == '__main__':
    train_image_size = 299

    config = tf.ConfigProto()
    #######设置allow_growth=True，gpu使用根据需求增长
    config.gpu_options.allow_growth = True
    with tf.Session(config=config) as sess:
        saver_terror = tf.train.import_meta_graph(MODEL_PATH_TERROR + '.meta', import_scope='terror')
        saver_terror.restore(sess, MODEL_PATH_TERROR)
        detect_terror = lambda img: sess.run('terror/InceptionV3/Predictions/Reshape_1:0',
                                             feed_dict={'terror/Placeholder:0': img})

        app.detect_terror = detect_terror

    app.train_image_size = train_image_size
    ###############host是监听的主机, host绑定哪个就监听哪个. 绑定0.0.0.0表示监听所有
    app.run(host='0.0.0.0', port=62001,debug=True)