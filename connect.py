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

def load_log(logs,i,j):
	behavior=[]
	while True:
		behavior.append(logs[i])
		i=i+1
		if i>j:break
	return behavior

# ~ def behavior_analysis(behavior):
	# ~ i=0
	# ~ while True:
		# ~ if i+1>=len(behavior):
			# ~ break
		# ~ else:
			# ~ if behavior[i][1]!=behavior[i+1][1]: #变倍速,编码为1
				# ~ behavior_list.append([behavior[i][5],1])
			# ~ elif behavior[i][3]!=behavior[i+1][2] and abs(behavior[i][5]-behavior[i+1][4])<1:#暂停，编码为2
				# ~ behavior_list.append([behavior[i][5],2])
			# ~ elif behavior[i][5]-behavior[i+1][4]>1:#后退，编码为3
				# ~ behavior_list.append([behavior[i][5],3])
			# ~ elif behavior[i][5]-behavior[i+1][4]<-1:#前进，编码为4
				# ~ behavior_list.append([behavior[i][5],4])
			# ~ else:#unknown behavior，编码为5
				# ~ behavior_list.append([behavior[i][5],5])
		# ~ i=i+1
# ~ def behavior_analysis(behavior):
	# ~ i=0
	# ~ while True:
		# ~ if i+1>=len(behavior):
			# ~ break
		# ~ else:
			# ~ behavior_list.append([behavior[i][5],behavior[i+1][4]-behavior[i][5]])
		# ~ i=i+1
		
def behavior_analysis(behavior):
	i=0
	while True:
		if i+1>=len(behavior):
			break
		elif str2time(behavior[i+1][2])-str2time(behavior[i][3])<385 and str2time(behavior[i+1][2])-str2time(behavior[i][3])>0:
			behavior_list.append([str2time(behavior[i+1][2])-str2time(behavior[i][3]),behavior[i+1][4]-behavior[i][5]])
		i=i+1


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

behavior_list=[]
k=0
for user in user_list:
	#筛选所有该用户的日志
	sql="select distinct watch_os, watch_rate, start_localtime, end_localtime, start_video_location, end_video_location from for_single_video where user_id="+user+" order by start_localtime"
	cursor.execute(sql)
	logs=cursor.fetchall()
	# ~ for row in logs:
		# ~ print(row)
		# ~ print('\n')
	
	#分开每次观看行为
	i=0
	j=0
	watch_behaviors=[]
	while True:
		if i==j:
			j=j+1
		else:
			if logs[j][0]!=logs[j-1][0] or str2time(logs[j][2])-str2time(logs[j-1][3])>385:
				watch_behaviors.append(load_log(logs,i,j-1))
				i=j
			else:
				j=j+1
		
		if j>=len(logs):
			watch_behaviors.append(load_log(logs,i,j-1))						
			break;
			
	# ~ for row in watch_behaviors:	
		# ~ print(row)
		# ~ print('\n')
	
	#对每次观看中的行为分析
	for behavior in watch_behaviors:
		behavior_analysis(behavior)
	
	k=k+1
	if k%100==0:
		print(k)


	

print(behavior_list)
output = open('data.txt','w+')
for row in behavior_list:
	output.write(str(row[0]))
	output.write('\t')
	output.write(str(row[1]))
	output.write('\n')      
output.close()

behavior_list=np.array(behavior_list)
plt.scatter(behavior_list[:,0],behavior_list[:,1])
zhfont1 = mfm.FontProperties(fname='/usr/share/wine/fonts/simsun.ttc')
plt.xlabel('视频时间轴',fontproperties=zhfont1)
plt.ylabel('跳转时间',fontproperties=zhfont1)

plt.show()

# 关闭数据库连接
db.close()
