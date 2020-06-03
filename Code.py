# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re
import collections
import jieba
import wordcloud
from PIL import Image
#导入数据
data = pd.read_excel(r'C:\Users\Administrator\Desktop\Python\大一下Python实训\消费者投诉举报信息意见挖掘\data\
                     12315某段时间内的投诉数据.xlsx')
#把“品牌”列索引出来，显示布尔值   #去除无商标
pinpai1 = data['品牌'] == '无'
pinpai2 = data['品牌'] == '无商标'
#反布尔值
pinpai3 = ~pinpai1
pinpai4 = ~pinpai2
data1 = data.loc[pinpai3,:]    #用原数据按pinpai3索引把为“无”的数据去掉
data2 = data1.loc[pinpai4,:]   #用原数据按pinpai4索引把为“无”的数据去掉
#用dropna去除空值
data3 = data2.dropna(axis=0)
#把“品牌”，“信息类别”索引出来
data4 = data3.loc[:,['品牌','信息类别']]
#分别索引出信息类别为1,2,3的品牌
leibie1 = data4.loc[data4['信息类别']==1,:]
leibie2 = data4.loc[data4['信息类别']==2,:]
leibie3 = data4.loc[data4['信息类别']==3,:]
#只留下品牌列方便后续建图
leibie11 = leibie1.iloc[:,0]
leibie12 = leibie2.iloc[:,0]
leibie13 = leibie3.iloc[:,0]
#保存数据
leibie11.to_csv(r'C:\Users\Administrator\Desktop\品牌投诉数据.txt',index=False)
leibie12.to_csv(r'C:\Users\Administrator\Desktop\品牌举报数据.txt',index=False)
leibie13.to_csv(r'C:\Users\Administrator\Desktop\品牌咨询数据.txt',index=False)
#合并数据
leibiehebing = pd.concat([leibie11,leibie12,leibie13],axis=1)
leibiehebing.columns = ['投诉品牌数据','举报品牌数据','咨询品牌数据']
leibiehebing.to_csv(r'C:\Users\Administrator\Desktop\品牌合并数据.txt',index=False)
#绘制消费者投诉举报咨询比例图
plt.rcParams['font.sans-serif'] = 'SimHei'   #设置中文显示
plt.rcParams['axes.unicode_minus'] = False
plt.figure(figsize=(7,7))    #设定画布a
label = ['投诉','举报','咨询']
#设定各项距离圆心n个半径
explode = [0.01,0.01,0.01]
#绘制饼图
plt.pie([np.size(leibie11),np.size(leibie12),np.size(leibie13)],explode=explode,labels=label,autopct='%1.1f%%')
plt.title('消费者投诉举报咨询比例图')
plt.show()
#统计投诉、举报、咨询三大类各品牌前十,并索引出来
zong_tousu = leibie1.品牌.value_counts().head(10)
zong_jubao = leibie2.品牌.value_counts().head(10)
zong_zixun = leibie3.品牌.value_counts().head(10)
#投诉前十的品牌直方图
label1 = list(zong_tousu.index)
plt.figure(figsize=(6,5))   #设置画布
plt.bar(range(10),np.int64(zong_tousu),width = 0.5)
plt.xlabel('投诉排名')   #添加横坐标
plt.ylabel('投诉次数')
plt.xticks(range(10),label1)
plt.title('投诉排名前十的品牌直方图')
plt.show()
#举报前十的品牌直方图
label2 = list(zong_jubao.index)
plt.figure(figsize=(6,5))   #设置画布
plt.bar(range(10),np.int64(zong_jubao),width = 0.5)
plt.xlabel('举报排名')   #添加横坐标
plt.ylabel('举报次数')
plt.xticks(range(10),label2)
plt.title('举报排名前十的品牌直方图')
plt.show()
#咨询前十的品牌直方图
label3 = list(zong_zixun.index)
plt.figure(figsize=(6,5))   #设置画布
plt.bar(range(10),np.int64(zong_zixun),width = 0.5)
plt.xlabel('咨询排名')   #添加横坐标
plt.ylabel('咨询次数')
plt.xticks(range(10),label3)
plt.title('咨询排名前十的品牌直方图')
plt.show()
#把华为的‘品牌’、‘信息类别’、‘备注’索引出来
huawei = data3.loc[data3['品牌'] == '华为',['品牌','信息类别','备注']]
#将华为的信息类别分类
huawei1 = huawei.loc[huawei['信息类别'] == 1]
huawei2 = huawei.loc[huawei['信息类别'] == 2]
huawei3 = huawei.loc[huawei['信息类别'] == 3]
#提取华为品牌的备注列
huawei_bz1 = huawei1.loc[:,'备注']
huawei_bz2 = huawei2.loc[:,'备注']
huawei_bz3 = huawei3.loc[:,'备注']
#对三类信息的备注列进行分词
huawei_cut1=huawei_bz1.apply(lambda x: jieba.lcut(x))
huawei_cut2=huawei_bz2.apply(lambda x: jieba.lcut(x))
huawei_cut3=huawei_bz3.apply(lambda x: jieba.lcut(x))
#将分词好的三类备注合并在一起
huawei_cut_1 = [huawei_cut1,huawei_cut2,huawei_cut3]
#去除停用词
with open(r'C:\Users\Administrator\Desktop\Python\大一下Python实训\参考\stoplist.txt',encoding='utf-8') as f:
    stop=f.read()
    
stop=stop.split() 
stop = [' '] + stop  #Pandas自动过滤了空格符，这里手动添加
aa = []
for a in huawei_cut_1:
    comment_cut=a.apply(lambda x: [i for i in x if i not in stop])
# 去除无内容的记录，分词后有记录缺失
    ind9=comment_cut.apply(lambda x: x!=[])
    aa.append(comment_cut.loc[ind9])
GJC_tousu = aa[0]
GJC_jubao = aa[1]
GJC_zixun = aa[2]
#词云图
from scipy.misc import imread
from wordcloud import WordCloud
import matplotlib.pyplot as plt
#统计词频
for i in range(len(aa)):
    tmp = aa[i].apply(lambda x: ' '.join(x))  # 去除逗号
    tmp2 = ' '.join(tmp) #去除列表符号
    num = pd.Series(tmp2.split()).value_counts()
#读取背景图片
    pic = imread(r'C:\Users\Administrator\Desktop\zz.jpg')
#设置背景图参数
    wc = WordCloud(mask=pic, background_color='white', 
               font_path='C:/Windows/Fonts/simhei.TTF',
               random_state=123)
    wc2 = wc.fit_words(num) #num是由频数构成的Series的形式，且单词作为索引
#绘图
    plt.figure(figsize=(16,8))
    plt.imshow(wc2)
    plt.axis('off')
    plt.savefig(r'C:\Users\Administrator\Desktop\%d'%i)

from gensim import corpora
from gensim import models
cdd = [GJC_tousu,GJC_jubao,GJC_zixun]

for a in range(len(cdd)):
    
    text1 = corpora.Dictionary(cdd[a])
    text2 = [text1.doc2bow(i) for i in cdd[a]]
    text2_model = models.LdaModel(corpus = text2,num_topics = 2,id2word = text1)

    for i in range(2):
        print(text2_model.print_topic(i))
        print('__________第%d次____________'%i)


