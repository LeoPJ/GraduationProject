import pymysql
import time
import os

def str2time(a1):
	# 先转换为时间数组
	timeArray = time.strptime(a1, "%Y-%m-%d %H:%M:%S")
	# 转换为时间戳
	timeStamp = int(time.mktime(timeArray))
	return timeStamp

def load_log(logs,i,j):
	behavior=[]
	while True:
		behavior.append(logs[i])
		i=i+1
		if i>j:break
	return behavior

def split_log(logs):
#分开每次视频观看行为
	i=0
	j=0
	watch_behaviors=[]
	
	while True:
		if i==j:
			j=j+1
		else:
			if logs[j][0]!=logs[j-1][0] or logs[j][1]!=logs[j-1][1] or str2time(logs[j][2])-str2time(logs[j-1][3])>600:
				#以相邻两个日志观看的视频不同或相隔十分钟以上作为分界
				watch_behaviors.append(load_log(logs,i,j-1))
				i=j
			else:
				j=j+1
		
		if j>=len(logs):
			watch_behaviors.append(load_log(logs,i,j-1))						
			break;

	return watch_behaviors

def get_video_code(logs,video_length):
#获取视频+观看率元素
	
	#生成视频的bool数组
	if_watch=[]
	for k in range(0,video_length):
		if_watch.append(False)
	
	#把已看过的片段改为True
	for row in logs:
		for l in range(row[4],row[5]):
			if_watch[l]=True
	
	#统计已看过的长度
	count=0
	for item in if_watch:
		if item:
			count=count+1
	
	#观看完成率的离散化处理
	completion_percentage=count/video_length
	if completion_percentage<=0.25:
		discreted_completion='A'
	elif completion_percentage>0.25 and completion_percentage<=0.5:
		discreted_completion='B'
	elif completion_percentage>0.5 and completion_percentage<=0.75:
		discreted_completion='C'
	else:
		discreted_completion='D'
	
	video_code=str(logs[0][0])+discreted_completion
	
	return video_code

def get_behavior_sequence(video_sequence,video_num):
#获取观看行为序列
	sequence=[]
	
	#先存入第一个视频的播放行为
	if video_sequence[0][-1]=='A':
		sequence.append('P1')
	elif video_sequence[0][-1]=='B':
		sequence.append('P2')
	elif video_sequence[0][-1]=='C':
		sequence.append('P3')
	else:
		sequence.append('P4')
	
	for i in range(0,len(video_sequence)-1):
		
		#记录播放之前的其他行为
		if int(video_sequence[i+1][:-1])!=int(video_sequence[i][:-1])+1:
			#记录重放行为
			if int(video_sequence[i+1][:-1])==int(video_sequence[i][:-1]):
				sequence.append('R')
			
			#记录后退行为
			elif int(video_sequence[i+1][:-1])<int(video_sequence[i][:-1]):
				back_num=int(video_sequence[i][:-1])-int(video_sequence[i+1][:-1])
				if back_num<=0.25*video_num:
					sequence.append('B1')
				elif back_num>0.25*video_num and back_num<=0.5*video_num:
					sequence.append('B2')
				elif back_num>0.5*video_num and back_num<=0.75*video_num:
					sequence.append('B3')
				else:
					sequence.append('B4')
			
			#记录快进行为
			elif int(video_sequence[i+1][:-1])>int(video_sequence[i][:-1])+1:
				forward_num=int(video_sequence[i+1][:-1])-int(video_sequence[i][:-1])
				if forward_num<=0.25*(video_num-1):
					sequence.append('F1')
				elif forward_num>0.25*(video_num-1) and forward_num<=0.5*(video_num-1):
					sequence.append('F2')
				elif forward_num>0.5*(video_num-1) and forward_num<=0.75*(video_num-1):
					sequence.append('F3')
				else:
					sequence.append('F4')
		
		#记录必有的播放行为
		if video_sequence[i+1][-1]=='A':
			sequence.append('P1')
		elif video_sequence[i+1][-1]=='B':
			sequence.append('P2')
		elif video_sequence[i+1][-1]=='C':
			sequence.append('P3')
		else:
			sequence.append('P4')
	
	return sequence
			

if __name__ == '__main__':
	# 连接数据库
	db = pymysql.connect("localhost","root","hh0326lpj","videos" )
	cursor = db.cursor()
	
	#获取视频长度
	sql='select seq,video_length from cs_video'
	cursor.execute(sql)
	length=cursor.fetchall()
	video_lengths={}
	for row in length:
		video_lengths[row[0]]=row[1]
	
	#获取视频数量
	video_num=len(video_lengths)
	
	#获取用户id列表
	sql = "SELECT distinct user_id FROM cs_base_ana"
	cursor.execute(sql)
	user_id = cursor.fetchall()	
	user_list=[]
	for row in user_id:
		user_list.append(row[0])
	
	#对每个用户进行编码
	data={}
	
	i=0
	for user in user_list:
		
		#获取观看日志
		sql='select seq,watch_os,start_localtime,end_localtime,cast(round(start_video_location,0) as signed) as start_video_location, cast(round(end_video_location,0) as signed) as end_video_location from cs_base_ana where user_id=\"'+user+'\"  order by start_localtime'
		cursor.execute(sql)
		video_logs=cursor.fetchall()
		
		#分开每一次不同的视频观看session
		splited_logs=split_log(video_logs)
		
		#生成视频观看序列
		video_sequence=[]
		for log in splited_logs:
			video_sequence.append(get_video_code(log,int(video_lengths[log[0][0]])))
		
		#生成观看行为序列
		video_behavior_sequence=get_behavior_sequence(video_sequence,video_num)
		
		#生成用户数据专属字典并存入总字典中
		user_behavior_data={'route':video_sequence,'behavior':video_behavior_sequence}
		data[user]=user_behavior_data
		print("第"+str(i+1)+"位学习者编码完成, id:"+user)
		i+=1
	
	print(data)
	data_file=open("cs_encode_data.txt",'w+') 
	print(data,file=data_file)

