#coding=utf-8
from __future__ import division
import requests
import os
from random import sample
import json
import cv2
import matplotlib.pyplot as plt
import numpy as np
from sklearn import metrics
def host_request(filename):
    payload=dict()
    files={'file':open(filename,'rb')}
    res=requests.post("http://101.132.178.184:9902/api/porn_detect_by_data",files=files,timeout=5)
    if res.status_code == 200:
        #return response

        return res.json()
    else:
        return '-1'
        #print ("error!!")
        #pass
'''
def roc(predict_value,gd_pre_dict):
    #keys=gd_pre_dict.keys()
    roc=dict()
    _TPR=[]
    _FPR=[]
    for value in predict_value:
        tp, tn, fp, fn = 0, 0, 0, 0
        threshold=value
        # predict_pos=i+1
        # predict_neg=len(array)-i-i
        for i in range(len(predict_value)):
            if predict_value[i]>=threshold:
                if gd_pre_dict[predict_value[i]]=='1':
                    tp += 1
                else:
                    fp += 1
            else:
                if gd_pre_dict[predict_value[i]]=='0':
                    tn += 1
                else:
                    fn += 1
        accuracy=(tp+tn)/(tp+tn+fp+fn)
        TPR=tp/(tp+fn)
        FPR=fp/(tn+fp)
        _TPR.append(TPR)
        _FPR.append(FPR)
        print(tp + tn + fp + fn)
        print (accuracy)
    print (_TPR)
    print(_FPR)
    #print (accuracy)

    return _FPR,_TPR
'''
files_dir='G:\\Yi+\\normal_images'
ground_truths=[]
conf_gd=dict()
confidences=[]
count=0
length=len(os.listdir(files_dir))
filenames=os.listdir(files_dir)
for i in range(105807,105808):
    if filenames[i]=='0':
        ground_truth = 0
    else:
        ground_truth = 1
#for filename in (filenames[:38707]):
    # if filename[0]=='0':
    #     ground_truth=0
    # else:
    #     ground_truth=1
    ground_truths.append(ground_truth)
    #file_path=os.path.join(files_dir,filename)
    file_path = os.path.join(files_dir, filenames[i])
    value_dict=host_request(file_path)
    if value_dict!='-1':
        confidence=float(value_dict['confidence'].strip('[').strip(']'))
        confidences.append(confidence)
        count+=1
        print ('file_name:{},confidence:{},detect_rate:{}'.format(file_path,confidence,count/length))
ground_truths=np.array(ground_truths)
confidences=np.array(confidences)
    #conf_gd[confidence]=ground_truth
#返回降序的cofidence列表
#sorted_confidences=sorted(conf_gd.keys(),reverse=True)

#FPR_final,TPR_final=roc(sorted_confidences,conf_gd)
#print (roc_value)
fpr,tpr,thresholds=metrics.roc_curve(ground_truths,confidences,pos_label=1)
plt.title("FPR vs TPR")
plt.xlabel("FPR")
plt.ylabel("TPR")
plt.plot(fpr,tpr,label="ROC")
plt.legend(bbox_to_anchor=[0.1, 1])
plt.xlim([0.0,1.0])
plt.ylim([0.0,1.0])
plt.grid()
plt.show()






