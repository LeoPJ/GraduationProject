import os
import numpy as np
import cmath
import re
import math as m
import pandas as pd
import json
import matplotlib.pyplot as plt
import pymysql
from sklearn.cluster import AgglomerativeClustering
from sklearn.metrics import silhouette_score

def write_file(str):
#写入文件
    writefile = open("high_result_computer_Cos6.txt", 'a+',encoding='utf-8')
    writefile.write(str + '\n')
    writefile.close()


if __name__ == '__main__':
	#读取编码数据
	f=open('/home/cuper/python_work/GraduationProject/toPaper/encode/computer_encode_data.txt', 'r')
	data=eval(f.read())
	print(len(data))

	#连接数据库
	db = pymysql.connect("localhost","root","hh0326lpj","videos" )
	cursor = db.cursor()
	#获取视频个数
	sql='select count(distinct seq) from computer_mining'
	cursor.execute(sql)
	length=cursor.fetchall()
	video_num=length[0][0]
	#统计视频观看覆盖率,区分高低覆盖率学习者	
	low_user=[]
	high_user=[]
	sql='select user_id,count(distinct seq) as watched_num from computer_mining group by user_id'
	cursor.execute(sql)
	watched_video_num=cursor.fetchall()
	for row in watched_video_num:
		if(row[1])/video_num<=0.05:
			low_user.append(row[0])
		else:
			high_user.append(row[0])
	print(low_user)
	print(high_user)
	
	#读取距离矩阵
	low_sim=np.load("/home/cuper/python_work/GraduationProject/toPaper/similarity/low_cover_sim_computer_Cos1.npy")
	high_sim=np.load("/home/cuper/python_work/GraduationProject/toPaper/similarity/high_cover_sim_computer_Cos6.npy")
	# ~ low_selecting_sim=np.load("/home/cuper/python_work/GraduationProject/fix/similarity/low_cover_selecting_dist_Cos1.npy")
	
	#利用轮廓系数确定聚类个数
	# ~ silhouette_low=[]
	# ~ silhouette_high=[]
	# ~ num=range(2,20)
	# ~ for k in num:
		# ~ clustering_low = AgglomerativeClustering(n_clusters=k,affinity='precomputed',linkage='average').fit(low_sim)
		# ~ silhouette_low.append(silhouette_score(low_sim, clustering_low.labels_, metric='precomputed'))
		
		# ~ clustering_high = AgglomerativeClustering(n_clusters=k,affinity='precomputed',linkage='average').fit(high_sim)
		# ~ silhouette_high.append(silhouette_score(high_sim, clustering_high.labels_, metric='precomputed'))
	
	# ~ plt.plot(num,silhouette_low,marker="+",color='red',label="low_coverage")
	# ~ plt.plot(num,silhouette_high,marker="x",color='blue',linestyle='--',label="high_coverage")
	# ~ plt.xlabel("n_clusters")
	# ~ plt.ylabel("silhouette_score")
	# ~ plt.title("Choosing number for best clustering quality\nLesson:computer")
	# ~ plt.legend()
	# ~ plt.xticks(np.array(num))
	
	#标记轮廓系数最大值点
	# ~ a=np.array(silhouette_low)
	# ~ amax_indx=np.argmax(a)
	# ~ plt.plot(amax_indx+2,a[amax_indx],'o')
	# ~ ashow_max='['+str(amax_indx+2)+','+str(round(a[amax_indx],3))+']'
	# ~ plt.annotate(ashow_max,xytext=(amax_indx+2,a[amax_indx]),xy=(amax_indx+2,a[amax_indx]))
	
	# ~ b=np.array(silhouette_high)
	# ~ bmax_indx=np.argmax(b)
	# ~ plt.plot(bmax_indx+2,b[bmax_indx],'o')
	# ~ bshow_max='['+str(bmax_indx+2)+','+str(round(b[bmax_indx],3))+']'
	# ~ plt.annotate(bshow_max,xytext=(bmax_indx+2,b[bmax_indx]),xy=(bmax_indx+2,b[bmax_indx]))
	
	# ~ ax = plt.gca()
	# ~ #设置上边和右边无边框
	# ~ ax.spines['right'].set_color('none')
	# ~ ax.spines['top'].set_color('none')
	# ~ plt.show()   
	
	
	#根据轮廓系数确定的聚类个数进行聚类和结果记录，用函数write_file()写入文档
	clustering = AgglomerativeClustering(n_clusters=2,
		affinity='precomputed',
		linkage='average').fit(high_sim)
	
	n_cluster=clustering.n_clusters_
	
	cluster_result=[]
	for i in range(0,n_cluster):
		cluster_result.append([])
	write_file('聚类结果：共聚为{}类'.format(n_cluster))
	label=clustering.labels_
	print(label)
	j=0
	for index in label:
		cluster_result[index].append(high_user[j])
		j+=1

	for i in range(0,n_cluster):
		write_file('第{0}类：共有{1}个学习者'.format(i+1,len(cluster_result[i])))
		for user in cluster_result[i]:
			write_file('id:{0} 行为序列:{1}'.format(user,str(data[user]['behavior'])))
	

				
		

