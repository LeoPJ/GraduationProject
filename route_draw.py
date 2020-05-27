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

sql='select seq,video_length from dt_video'
length=tomysql(sql)

lengths={}
for row in length:
	lengths[row[0]]=row[1]

print(lengths)
video_num=len(lengths)
print(video_num)

user='207291'
sql='select seq,watch_os,start_localtime,end_localtime,cast(round(start_video_location,0) as signed) as start_video_location, cast(round(end_video_location,0) as signed) as end_video_location from dt_ana where user_id=\"'+user+'\"  order by start_localtime'

logs=tomysql(sql)


i=0
j=0
watch_behaviors=[]

#分开每次观看行为
while True:
	if i==j:
		j=j+1
	else:
		if logs[j][0]!=logs[j-1][0] or logs[j][1]!=logs[j-1][1] or str2time(logs[j][2])-str2time(logs[j-1][3])>600:
			watch_behaviors.append(load_log(logs,i,j-1))
			i=j
		else:
			j=j+1
	
	if j>=len(logs):
		watch_behaviors.append(load_log(logs,i,j-1))						
		break;
		
for row in watch_behaviors:
	print(row)

video_sequence=[]
for row in watch_behaviors:
	video_sequence.append(row[0][0])
print(video_sequence)

indexs=[]
	
for behavior in watch_behaviors:
	indexs.append(create_index(behavior))
print(indexs)

compl={}
for i in range(0,53):
	compl[i]=0
for row in indexs:
	if row[1]>compl[row[0]]:
		compl[row[0]]=row[1]

print(compl)


nodes=[]
for i in range(0,53):
	if compl[i]<0.25:
		nodes.append(opts.GraphNode(name=str(i),symbol_size=4))
	elif compl[i]>0.25 and compl[i]<0.5:
		nodes.append(opts.GraphNode(name=str(i),symbol_size=8))
	elif compl[i]>0.5 and compl[i]<0.75:
		nodes.append(opts.GraphNode(name=str(i),symbol_size=12))
	elif compl[i]>0.75:
		nodes.append(opts.GraphNode(name=str(i),symbol_size=16))


links=[]

for i in range(0,len(video_sequence)-1):
	links.append(opts.GraphLink(source=str(video_sequence[i]), target=str(video_sequence[i+1])))




c = (
    Graph(init_opts=opts.InitOpts(width="900px", height="500px"))
    .add(
        "",
        nodes=nodes,
        links=links,
        layout="circular",
        is_rotate_label=True,
        linestyle_opts=opts.LineStyleOpts(color="source", curve=0.3),
        label_opts=opts.LabelOpts(position="right",font_size=13),
    )
    .set_global_opts(
        title_opts=opts.TitleOpts(title="用户学习路径",subtitle='课程：大唐兴衰'),
    )
    .render("graph_les_miserables.html")
)
