import pymysql
import time
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.font_manager as mfm
import os
from itertools import chain

def behavior_generation(behavior):
	event=[]
	if behavior[0][1]==1.0:
		event.append(['pl',str2time(behavior[0][2]),behavior[0][5]-behavior[0][4]])
	elif behavior[0][1]>1.0:
		event.append(['rf',str2time(behavior[0][2]),0])
		event.append(['pl',str2time(behavior[0][2]),behavior[0][5]-behavior[0][4]])
	else:
		event.append(['rs',str2time(behavior[0][2]),0])
		event.append(['pl',str2time(behavior[0][2]),behavior[0][5]-behavior[0][4]])
	
	for i in range(1,len(behavior)):
		if behavior[i][1]!=behavior[i-1][1]:#先判断是否有变速
			if behavior[i][1]==1.0:
				event.append(['rd',str2time(behavior[i][2]),0])
			elif behavior[i][1]>1.0:
				event.append(['rf',str2time(behavior[i][2]),0])
			else:
				event.append(['rs',str2time(behavior[i][2]),0])
		else:
			if abs(behavior[i][4]-behavior[i-1][5])<1:#暂停
				if str2time(behavior[i][2])-str2time(behavior[i-1][3])!=0:
				    event.append(['pa',str2time(behavior[i-1][3]),str2time(behavior[i][2])-str2time(behavior[i-1][3])])
			elif behavior[i][4]-behavior[i-1][5]>=1:#快进
				event.append(['sf',str2time(behavior[i][2]),behavior[i][4]-behavior[i-1][5]])
			else:#快退
				event.append(['sb',str2time(behavior[i][2]),behavior[i-1][5]-behavior[i][4]])
		
		event.append(['pl',str2time(behavior[i][2]),behavior[i][5]-behavior[i][4]])
	
	#合并连续出现的相同动作
	i=0
	while True:
		if len(event)<=1:
			break
			
		if event[i][0]==event[i+1][0]:
			event[i][2]=event[i][2]+event[i+1][2]
			del event[i+1]
		else:
			i=i+1
		if i>=len(event)-1:
			break
	
	return event
		
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

def dcode_seq(seq):
	
	pl=[]
	pa=[]
	sf=[]
	sb=[]
	for row in seq:
		if row[0]=='pl':
			pl.append(row[2])
		elif row[0]=='pa':
			pa.append(row[2])
		elif row[0]=='sf':
			sf.append(row[2])
		elif row[0]=='sb':
			sb.append(row[2])
	
	pl_Q1=np.quantile(pl,0.25,interpolation='lower')#下四分位数
	pl_Q2=np.median(pl) #中位数
	pl_Q3=np.quantile(pl,0.75,interpolation='higher')#上四分位数
	pa_Q1=np.quantile(pa,0.25,interpolation='lower')#下四分位数
	pa_Q2=np.median(pa) #中位数
	pa_Q3=np.quantile(pa,0.75,interpolation='higher')#上四分位数
	sf_Q1=np.quantile(sf,0.25,interpolation='lower')#下四分位数
	sf_Q2=np.median(sf) #中位数
	sf_Q3=np.quantile(sf,0.75,interpolation='higher')#上四分位数
	sb_Q1=np.quantile(sb,0.25,interpolation='lower')#下四分位数
	sb_Q2=np.median(sb) #中位数
	sb_Q3=np.quantile(sb,0.75,interpolation='higher')#上四分位数
	#print(pl_Q1,pl_Q2,pl_Q3,pa_Q1,pa_Q2,pa_Q3,sf_Q1,sf_Q2,sf_Q3,sb_Q1,sb_Q2,sb_Q3)
	
	
	avseq=[]
	for row in seq:
		if row[0]=='pa':
			if row[2]<=pa_Q1:
				avseq.append('pa1')
			elif row[2]>pa_Q1 and row[2]<=pa_Q2:
				avseq.append('pa2')
			elif row[2]>pa_Q2 and row[2]<=pa_Q3:
				avseq.append('pa3')
			else:
				avseq.append('pa4')
	
		elif row[0]=='sf':
			if row[2]<=sf_Q1:
				avseq.append('sf1')
			elif row[2]>sf_Q1 and row[2]<=sf_Q2:
				avseq.append('sf2')
			elif row[2]>sf_Q2 and row[2]<=sf_Q3:
				avseq.append('sf3')
			else:
				avseq.append('sf4')
	
		elif row[0]=='sb':
			if row[2]<=sb_Q1:
				avseq.append('sb1')
			elif row[2]>sb_Q1 and row[2]<=sb_Q2:
				avseq.append('sb2')
			elif row[2]>sb_Q2 and row[2]<=sb_Q3:
				avseq.append('sb3')
			else:
				avseq.append('sb4')
	
		elif row[0]=='rf':
			avseq.append('rf')
	
		elif row[0]=='rs':
			avseq.append('rs')
			
		elif row[0]=='rd':
			avseq.append('rd')
		
		elif row[0]=='pl':
			if row[2]<=pl_Q1:
				avseq.append('pl1')
			elif row[2]>pl_Q1 and row[2]<=pl_Q2:
				avseq.append('pl2')
			elif row[2]>pl_Q2 and row[2]<=pl_Q3:
				avseq.append('pl3')
			else:
				avseq.append('pl4')
	
	return avseq

# 打开数据库连接
db = pymysql.connect("localhost","root","hh0326lpj","videos" )
 
# 使用cursor()方法获取操作游标 
cursor = db.cursor()
 
# SQL 查询语句
sql = "SELECT distinct user_id FROM for_single_video"
# 执行SQL语句
cursor.execute(sql)
# 获取所有记录列表
user_id = cursor.fetchall()

user_list=[]
for row in user_id:
	user_list.append(row[0])
# ~ print(user_list)
print(len(user_list))

#user_id现存于字符串列表user_list中


cluster_sta={}
# ~ user='414906'
k=0
for user in user_list:
	# ~ print(k)
	#筛选所有该用户的日志
	sql="select distinct watch_os, watch_rate, start_localtime, end_localtime, start_video_location, end_video_location from for_single_video where user_id=\'"+user+"\' order by start_localtime"
	#sql='select distinct watch_os, watch_rate, start_localtime, end_localtime, cast(round(start_video_location,0) as signed) as start_video_location, cast(round(end_video_location,0) as signed) as end_video_location from for_single_video where user_id=\"'+user+'\" order by start_localtime'
	
	# ~ print(sql)
	
	cursor.execute(sql)
	logs=cursor.fetchall()
	
	i=0
	j=0
	watch_behaviors=[]
	#分开每次观看行为
	while True:
		if i==j:
			j=j+1
		else:
			if logs[j][0]!=logs[j-1][0] or str2time(logs[j][2])-str2time(logs[j-1][3])>600:
				watch_behaviors.append(load_log(logs,i,j-1))
				i=j
			else:
				j=j+1
		
		if j>=len(logs):
			watch_behaviors.append(load_log(logs,i,j-1))						
			break;
	
	# ~ print(watch_behaviors)
	
	seq=[]
	# ~ behavior=(watch_os, watch_rate, start_localtime, end_localtime, start_video_location, end_video_location)
	for behavior in watch_behaviors:
		seq.append(behavior_generation(behavior))
	
	seq=list(chain(*seq))
	
	print(seq)
	
	seq=dcode_seq(seq)
	print(seq)
	cluster_sta[user]=seq
	
	k=k+1


print(cluster_sta)
print('\n')
print("414906:")
print(cluster_sta['414906'])
# ~ print("601527:")
# ~ print(cluster_sta['414906'][23:29])

