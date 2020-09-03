import json

from pyecharts import options as opts
from pyecharts.charts import Graph
import numpy as np
from sklearn.cluster import KMeans
import re
from sklearn.mixture import GaussianMixture
import math as m
import pandas as pd
import json
import matplotlib.pyplot as plt
import matplotlib.font_manager as mfm
import pymysql
import matplotlib
import time

def create_index(behavior):
	# ~ for row in behavior:
		# ~ print(row)
	
	video_length=int(lengths[behavior[0][0]])
	
	if_watch=[]
	for k in range(0,video_length):
		if_watch.append(False)
	
	NP=0
	MP=0
	NF=0
	SR=0
	NB=0
	RL=0

	duration=behavior[0][5]-behavior[0][4]
	SC=0
	
	for l in range(behavior[0][4],behavior[0][5]):
		if_watch[l]=True
	
	i=0
	MP_sta=[]
	for i in range(0,len(behavior)-1):
		if behavior[i][1]!=behavior[i+1][1]:#变速
			SC=SC+1
		
		#计算加权倍速

		duration=duration+behavior[i+1][5]-behavior[i+1][4]
			
		if behavior[i][5]==behavior[i+1][4]:#暂停
			if str2time(behavior[i+1][2])-str2time(behavior[i][3])!=0:
				NP=NP+1
				MP_sta.append(str2time(behavior[i+1][2])-str2time(behavior[i][3]))
		
		elif behavior[i][5]<behavior[i+1][4]:#快进
			NF=NF+1
	
		else:#后退
			NB=NB+1
	
		for l in range(behavior[i+1][4],behavior[i+1][5]):
			if(if_watch[l]):
				RL=RL+1
			else:
				if_watch[l]=True		
				

	
	for m in range(0,len(if_watch)):
		if if_watch[m]:
			start=m
			break
	for n in range(len(if_watch)-1,-1,-1):
		if if_watch[n]:
			end=n+1
			break
	completion=0
	for p in range(start,end):
		if if_watch[p]:
			completion=completion+1
		else:
			SR=SR+1
	SR=SR/(end-start)
	
	if NP!=0:
		MP = np.median(MP_sta)
	else:
		MP=0
	
	index=[behavior[0][0],completion/video_length]
	
	return index

def tomysql(sql):
#执行mysql语句专用器
	
	# 打开数据库连接
	db = pymysql.connect("localhost","root","hh0326lpj","videos" )
	
	# 使用cursor()方法获取操作游标 
	cursor = db.cursor()
	
	cursor.execute(sql)
	data=cursor.fetchall()
	
	return data

def load_log(logs,i,j):
	behavior=[]
	while True:
		behavior.append(logs[i])
		i=i+1
		if i>j:break
	return behavior

def str2time(a1):
#字符串时间转时间戳	
	
	# 先转换为时间数组
	timeArray = time.strptime(a1, "%Y-%m-%d %H:%M:%S")
	# 转换为时间戳
	timeStamp = int(time.mktime(timeArray))
	return timeStamp

#连接数据库
db = pymysql.connect("localhost","root","hh0326lpj","videos" )
cursor = db.cursor()

#读取编码数据
f=open('/home/cuper/python_work/GraduationProject/toPaper/encode/computer_encode_data.txt', 'r')
data=eval(f.read())
print(len(data))

#获取视频个数
sql='select count(distinct seq) from computer_mining'
cursor.execute(sql)
length=cursor.fetchall()
video_num=length[0][0]

user='3715751'
# ~ data[user]['route']=['1D', '6D', '7D', '8D', '9D', '10D', '11D', '12D', '18D', '19D', '20D', '21D', '22A', '23D',  '24D', '25D','30B','31C','32B','33A', '70D','71D','72D','73D','74D', '75D', '76D', '77D','42D', '43D', '44D', '45D', '149D','150C','151D','152D']
# ~ data[user]['route']=['1A', '2A', '3A', '4A', '4B', '5A', '6A', '27C', '28A', '29A', '30A','76A','77A','78A','79A','80B', '93A','94A','95A','96A','97B','103B','104A', '105A','106A', '107C','126A', '127A', '134B', '148C', '153A', '150D', '151C', '152C', '153A', '148A', '149A','53A','54A','55A','56A','57B','58B','60A']
print(data[user]['route'])
video_sequence=[]
for item in data[user]['route']:
	video_sequence.append(int(item[:-1]))
print(video_sequence)

compl={}
for i in range(1,video_num+1):
	compl[i]={'time':0,'com':'A'}
for item in data[user]['route']:
	compl[int(item[:-1])]['time']+=1
	if item[-1]>compl[int(item[:-1])]['com']:
		compl[int(item[:-1])]['com']=item[-1]

print(compl)


nodes=[]
for i in range(1,video_num+1):
	string=str(compl[i]['time'])
	if compl[i]['com']=='A':
		nodes.append(opts.GraphNode(name='V'+str(i),symbol_size=5,value=string))
	elif compl[i]['com']=='B':
		nodes.append(opts.GraphNode(name='V'+str(i),symbol_size=10,value=string))
	elif compl[i]['com']=='C':
		nodes.append(opts.GraphNode(name='V'+str(i),symbol_size=15,value=string))
	elif compl[i]['com']=='D':
		nodes.append(opts.GraphNode(name='V'+str(i),symbol_size=20,value=string))


links=[]

for i in range(0,len(video_sequence)-1):
	links.append(opts.GraphLink(source='V'+str(video_sequence[i]), target='V'+str(video_sequence[i+1])))



c = (
    Graph(init_opts=opts.InitOpts(width="1500px", height="1000px"))
    .add(
        "",
        nodes=nodes,
        links=links,
        layout="circular",
        is_rotate_label=True,
        linestyle_opts=opts.LineStyleOpts(color="source", curve=0.3),
        label_opts=opts.LabelOpts(position="right",font_size=12),
    )
    # ~ .set_global_opts(
        # ~ title_opts=opts.TitleOpts(title="Learning Paths of learners",subtitle='Course：C++'),
    # ~ )
    .render("graph_les_miserables.html")
)
