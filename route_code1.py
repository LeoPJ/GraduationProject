import pymysql
import time
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.font_manager as mfm
import os
from itertools import chain

def load_log(logs,i,j):
	behavior=[]
	while True:
		behavior.append(logs[i])
		i=i+1
		if i>j:break
	return behavior

def str2time(a1):
	# 先转换为时间数组
	timeArray = time.strptime(a1, "%Y-%m-%d %H:%M:%S")
	# 转换为时间戳
	timeStamp = int(time.mktime(timeArray))
	return timeStamp

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


# 打开数据库连接
db = pymysql.connect("localhost","root","hh0326lpj","videos" )
 
# 使用cursor()方法获取操作游标 
cursor = db.cursor()

sql='select seq,video_length from cs_video'
cursor.execute(sql)
length=cursor.fetchall()

lengths={}
for row in length:
	lengths[row[0]]=row[1]

print(lengths)
video_num=len(lengths)
print(video_num)

sql = "SELECT distinct user_id FROM cs_base_ana"
cursor.execute(sql)
user_id = cursor.fetchall()

user_list=[]
for row in user_id:
	user_list.append(row[0])
# ~ print(user_list)
print(len(user_list))

#user_id现存于字符串列表user_list中

k=0

cluster_sta={}

for user in user_list:
	
	sql='select seq,watch_os,start_localtime,end_localtime,cast(round(start_video_location,0) as signed) as start_video_location, cast(round(end_video_location,0) as signed) as end_video_location from cs_base_ana where user_id=\"'+user+'\"  order by start_localtime'
	cursor.execute(sql)
	logs=cursor.fetchall()
	
	#for row in logs:
		#print(row)
		#print('\n')
		
		
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
			
	# ~ for row in watch_behaviors:	
		# ~ print(row)
		
	indexs=[]
	
	for behavior in watch_behaviors:
		indexs.append(create_index(behavior))
	
	#print(indexs)
	
	sequ=[]
	#sequ.append('P')
	if indexs[0][1]<0.25:
		sequ.append('P1')
	elif indexs[0][1]>=0.25 and indexs[0][1]<0.5:
		sequ.append('P2')
	elif indexs[0][1]>=0.5 and indexs[0][1]<0.75:
		sequ.append('P3')
	else:
		sequ.append('P4')

	
	for i in range(0,len(indexs)-1):
		if indexs[i+1][0]!=indexs[i][0]+1:
			if indexs[i+1][0]==indexs[i][0]:
				sequ.append('R')
			
			elif indexs[i+1][0]<indexs[i][0]:
				#sequ.append('B')
				if indexs[i][0]-indexs[i+1][0]<0.25*video_num:
					sequ.append('B1')
				elif indexs[i][0]-indexs[i+1][0]>=0.25*video_num and indexs[i][0]-indexs[i+1][0]<0.5*video_num:
					sequ.append('B2')
				elif indexs[i][0]-indexs[i+1][0]>=0.5*video_num and indexs[i][0]-indexs[i+1][0]<0.75*video_num:
					sequ.append('B3')
				else:
					sequ.append('B4')

			elif indexs[i+1][0]>indexs[i][0]+1:
				#sequ.append('F')
				if indexs[i+1][0]-indexs[i][0]<0.25*(video_num-1):
					sequ.append('F1')
				elif indexs[i+1][0]-indexs[i][0]>=0.25*(video_num-1) and indexs[i+1][0]-indexs[i][0]<0.5*(video_num-1):
					sequ.append('F2')
				elif indexs[i+1][0]-indexs[i][0]>=0.5*(video_num-1) and indexs[i+1][0]-indexs[i][0]<0.75*(video_num-1):
					sequ.append('F3')
				else:
					sequ.append('F4')
		
		if indexs[i+1][1]<0.25:
			sequ.append('P1')
		elif indexs[i+1][1]>=0.25 and indexs[i+1][1]<0.5:
			sequ.append('P2')
		elif indexs[i+1][1]>=0.5 and indexs[i+1][1]<0.75:
			sequ.append('P3')
		else:
			sequ.append('P4')
		#sequ.append('P')
			
	
	#print(sequ)
	#se = ''.join(sequ)
	cluster_sta[user]=sequ
	
	k=k+1
	if(k%100==0):
		print(k)

data=open("./data/cs_base_data(code1).txt",'w+') 
print(cluster_sta)
print(cluster_sta,file=data)
data.close()

