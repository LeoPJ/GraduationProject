import time
def str2time(a1):
	# 先转换为时间数组
	timeArray = time.strptime(a1, "%Y-%m-%d %H:%M:%S")
	# 转换为时间戳
	timeStamp = int(time.mktime(timeArray))
	return timeStamp

a1 = "2019-5-10 23:40:00"
a2="2019-5-11 23:40:12"
print(str2time(a2)-str2time(a1))
