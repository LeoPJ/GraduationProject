import pymysql
import time
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.font_manager as mfm
import os

def str2time(a1):
	# 先转换为时间数组
	timeArray = time.strptime(a1, "%Y-%m-%d %H:%M:%S")
	# 转换为时间戳
	timeStamp = int(time.mktime(timeArray))
	return timeStamp

def create_index(behavior):
	# ~ for row in behavior:
		# ~ print(row)
	
	video_length=358
	
	if_watch=[]
	for k in range(0,video_length):
		if_watch.append(False)
	
	NP=0
	MP=0
	NF=0
	SR=0
	NB=0
	RL=0
	AS=(behavior[0][5]-behavior[0][4])*behavior[0][1]
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
		AS=AS+(behavior[i+1][5]-behavior[i+1][4])*behavior[i+1][1]
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
				
	AS=AS/duration
	
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
	
	index=[NP,MP,NF,SR,NB,RL,AS,SC,completion]
	
	return index
	
def load_log(logs,i,j):
	behavior=[]
	while True:
		behavior.append(logs[i])
		i=i+1
		if i>j:break
	return behavior

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


# ~ behavior_list=[]
k=0

cluster_sta={}

for user in user_list:
	#筛选所有该用户的日志
	#sql="select distinct watch_os, watch_rate, start_localtime, end_localtime, start_video_location, end_video_location from for_single_video where user_id=\'"+user+"\' order by start_localtime"
	sql='select distinct watch_os, watch_rate, start_localtime, end_localtime, cast(round(start_video_location,0) as signed) as start_video_location, cast(round(end_video_location,0) as signed) as end_video_location from for_single_video where user_id=\"'+user+'\" order by start_localtime'

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
			if logs[j][0]!=logs[j-1][0] or str2time(logs[j][2])-str2time(logs[j-1][3])>600:
				watch_behaviors.append(load_log(logs,i,j-1))
				i=j
			else:
				j=j+1
		
		if j>=len(logs):
			watch_behaviors.append(load_log(logs,i,j-1))						
			break;
	
	# ~ for row in watch_behaviors:	
		# ~ print(row)
	
	# ~ 暂停次数Number of pauses (NP)
	# ~ 暂停持续时间的中值Median duration of pauses (MP)
	# ~ 快进的次数Number of forward seeks (NF)
	# ~ 快进中跳过的视频内容占比Proportion of skipped video content (SR)
	# ~ 快退的次数Number of backward seeks (NB)
	# ~ 重复播放的视频长度Replayed video length (RL)
	# ~ 加权平均播放速度Average video speed (AS)
	indexs=[]
	# ~ behavior=(watch_os, watch_rate, start_localtime, end_localtime, start_video_location, end_video_location)
	for behavior in watch_behaviors:
		indexs.append(create_index(behavior))
		
	# ~ for row in indexs:
		# ~ print(row)
	
	summ=0
	for row in indexs:
		summ=summ+row[8]
	
	NP=0
	MP=0
	NF=0
	SR=0
	NB=0
	RL=0
	AS=0
	SC=0
	
	for row in indexs:
		por=row[8]/summ
		NP=NP+row[0]*por
		MP=MP+row[1]*por
		NF=NF+row[2]*por
		SR=SR+row[3]*por
		NB=NB+row[4]*por
		RL=RL+row[5]*por
		AS=AS+row[6]*por
		SC=SC+row[7]*por
	user_index=[NP,MP,NF,SR,NB,RL,AS,SC,summ]
	
	cluster_sta[user]=user_index
	
	k=k+1
	if(k%100==0):
		print(k)

print(cluster_sta)

output = open('data2.csv','w+')
for k in cluster_sta.keys():
	output.write(k)
	output.write(',')
	for r in range(0,9):
		output.write(str(cluster_sta[k][r]))
		if r==8:
			break
		else:
			output.write(',')
	output.write('\n')      
output.close()



# 关闭数据库连接
db.close()

