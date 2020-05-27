import pymysql
import time
import matplotlib.pyplot as plt
import matplotlib.font_manager as mfm
import numpy as np
import matplotlib
import os
from itertools import chain
import csv

def tomysql(sql):
#执行mysql语句专用器
	
	# 打开数据库连接
	db = pymysql.connect("localhost","root","hh0326lpj","videos" )
	
	# 使用cursor()方法获取操作游标 
	cursor = db.cursor()
	
	cursor.execute(sql)
	data=cursor.fetchall()
	
	return data

def tomysqlrds(sql):
#执行mysql语句专用器
	
	# 打开数据库连接
	db = pymysql.connect("rm-bp18o58u9fiwi31az1o.mysql.rds.aliyuncs.com","cuper","hh0326lpjMySQL","video" )
	
	# 使用cursor()方法获取操作游标 
	cursor = db.cursor()
	
	cursor.execute(sql)
	data=cursor.fetchall()
	
	return data


def str2time(a1):
#字符串时间转时间戳	
	
	# 先转换为时间数组
	timeArray = time.strptime(a1, "%Y-%m-%d %H:%M:%S")
	# 转换为时间戳
	timeStamp = int(time.mktime(timeArray))
	return timeStamp


def get_user_list(course_name):
#从数据库中获取用户列表，返回一个列表
	if course_name=='ENG':
		cn='ENG_ana'
	elif course_name=='dt':
		cn='dt_ana'
	elif course_name=='cy':
		cn='cy_ana'
	elif course_name=='cs':
		cn='cs_base_ana'
	
	sql = "SELECT distinct user_id FROM "+cn
	user_id = tomysql(sql)
	
	user_list=[]
	for row in user_id:
		user_list.append(row[0])
	# ~ print(user_list)
	print(len(user_list))
	
	#user_id现存于字符串列表user_list中
	return user_list
	
def get_video_length(course_name):
#从数据库中获取视频长度信息，返回一个字典
	if course_name=='ENG':
		cn='engl_video'
	elif course_name=='dt':
		cn='dt_video'
	elif course_name=='cy':
		cn='cye_video'
	elif course_name=='cs':
		cn='cs_video'
	
	sql='select seq,video_length from '+cn
	length = tomysql(sql)
	
	video_length={}
	for row in length:
		video_length[row[0]]=row[1]
	
	return video_length

def plot_hist(dicts):
	x=[]
	for num in dicts.values():
		x.append(num)
	
	data=np.array(x) 
	# 设置matplotlib正常显示中文和负号
	matplotlib.rcParams['font.sans-serif']=['SimHei']   # 用黑体显示中文
	matplotlib.rcParams['axes.unicode_minus']=False     # 正常显示负号
	
	plt.hist(data, bins=20, normed=0, facecolor="blue", edgecolor="black")
	
	zhfont1 = mfm.FontProperties(fname='/usr/share/wine/fonts/simsun.ttc')
	plt.xlabel('观看视频范围个数',fontproperties=zhfont1)
	plt.ylabel('频数',fontproperties=zhfont1)
	plt.title('课程：大学计算机基础 用户观看视频覆盖范围分布',fontproperties=zhfont1)

	plt.show()
		
def load_log(logs,i,j):
	behavior=[]
	while True:
		behavior.append(logs[i])
		i=i+1
		if i>j:break
	return behavior

# ~ def get_user_log():
# ~ dtuser_list=get_user_list('dt')
# ~ dtvideo_length=get_video_length('dt')
# ~ print(dtuser_list)
# ~ print(dtvideo_length)
# ~ print(len(dtvideo_length))

# ~ csuser_list=get_user_list('cs')
# ~ csvideo_length=get_video_length('cs')
# ~ print(csuser_list)
# ~ print(csvideo_length)
# ~ print(len(csvideo_length))



#user_vnum=tomysqlrds("select user_id,count(distinct video_id) from video_log9 where course_id='course-v1:GIT+1400000003+2017_T2' group by user_id")
user_vnum=tomysql("select user_id,count(distinct video_id) from `C++` group by user_id")
user_video_num={}
for row in user_vnum:
	user_video_num[row[0]]=row[1]

# ~ with open('/media/cuper/TOSHIBA EXT/xuetang_data/fgvideo_num/jr.csv', 'r') as f:
	# ~ reader = csv.reader(f)
	# ~ for row in reader:
		# ~ user_video_num[str(row[0])]=int(row[1])

print(user_video_num)
plot_hist(user_video_num)

video_number=110
first_col_user=[]
for k,v in user_video_num.items():
	if v<video_number/20:
		first_col_user.append(k)
print(len(first_col_user))


#dt start_date=2016-10-10 09:00:00
# ~ #end_date=2016-12-31 00:30:00

# ~ #金融学
# ~ start=str2time('2016-02-22 08:00:00')
# ~ end=str2time('2016-07-30 00:00:00')


# ~ #马原
# ~ start=str2time('2016-09-12 08:00:00')
# ~ end=str2time('2016-12-11 23:30:00')

# ~ #模电
# ~ start=str2time('2016-09-19 09:00:00')
# ~ end=str2time('2016-12-23 09:00:00')

# ~ #财经
# ~ start=str2time('2016-03-04 09:00:00')
# ~ end=str2time('2016-06-25 00:00:00')

#C++
start=str2time('2016-02-22 00:00:00')
end=str2time('2016-08-31 00:00:00')

# ~ #电路
# ~ start=str2time('2016-09-12 08:00:00')
# ~ end=str2time('2016-12-28 00:00:00')

# ~ #大物
# ~ start=str2time('2018-03-31 08:00:00')
# ~ end=str2time('2018-07-25 22:00:00')

# ~ #毛概
# ~ start=str2time('2017-09-05 19:00:00')
# ~ end=str2time('2017-12-25 23:30:00')

# ~ #ENG
# ~ start=str2time('2016-02-22 08:00:00')
# ~ end=str2time('2016-06-01 12:00:00')

# ~ cs_base:start=str2time('2018-09-16 08:00:00')
# ~ end=str2time('2018-12-23 23:30:00')

week=[]
t=start
while True:
	week.append(0)
	t+=604800
	if t>end:
		break
print(len(week))



k=0
for user in first_col_user:
	
	sql='select video_id,watch_os,start_localtime,end_localtime,cast(round(start_video_location,0) as signed) as start_video_location, cast(round(end_video_location,0) as signed) as end_video_location from `C++` where user_id=\"'+user+'\"  order by start_localtime'
	logs=tomysql(sql)
	
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
			
	for row in watch_behaviors:	
		ins=int((str2time(row[0][2])-start)/604800)
		if ins>=0 and ins<len(week):
			week[ins]+=1
	
	k+=1
	if k%100==0:
		print(k)
print(week)



# ~ week1=[11797, 30588, 11455, 24334, 27148, 23672, 22991, 22369, 24316, 28491, 27755, 19779, 11377, 14837, 1420]

waters = range(1,len(week)+1)
plt.bar(waters,week)

zhfont1 = mfm.FontProperties(fname='/usr/share/wine/fonts/simsun.ttc')
plt.xlabel('周数',fontproperties=zhfont1)
plt.ylabel('观看人数',fontproperties=zhfont1)


plt.title('课程：C++ 少量学习者的周次学习人数分布',fontproperties=zhfont1)

plt.show()

#模电：[453, 238, 129, 312, 406, 524, 461, 306, 262, 258, 292, 279, 256, 246]
