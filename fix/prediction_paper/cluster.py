import os
import numpy as np
import cmath
import re
import math as m
import pandas as pd
import json
import matplotlib.pyplot as plt
import pymysql
import kmedoids
from sklearn.metrics.pairwise import pairwise_distances
from sklearn import preprocessing, metrics

def write_file(str):
#写入文件
    writefile = open("course-v1:TsinghuaX+80512073X+2016_T1_6cluster.txt", 'a+',encoding='utf-8')
    writefile.write(str + '\n')
    writefile.close()

def clustering(distance,k,data,user):
	M,C=kmedoids.kMedoids(distance,k,tmax=10000)
	
	#写入中心点
	write_file('medoids:')
	i=1
	for point_idx in M:
		write_file("第{}类中心点：".format(i))
		write_file("id："+user[point_idx])
		write_file(str(data[user[point_idx]]))
		i+=1
	
	write_file('')
	write_file('clustering result:')
	for label in C:
		write_file("第{0}类：共有{1}个学习者".format(label+1,len(C[label])))	
	
	for label in C:
		write_file('')
		write_file("第{0}类：共有{1}个学习者".format(label+1,len(C[label])))
		for point_idx in C[label]:
			write_file('id:{0}:{1}'.format(user[point_idx],str(data[user[point_idx]])))

if __name__ == '__main__':

	df = pd.read_csv("/home/cuper/python_work/Lab_code/final/final_features_v2.csv", low_memory=False)
	course_id='course-v1:TsinghuaX+80512073X+2016_T1'
	df['user_id'] = df['user_id'].astype('str')
	df = df[(df['course_id']==course_id)]
	test_data = np.array(df[['participations', 'com_threads', 'comments', 'avg_length', 'per_open', 'per_vtotal', 'per_vcompl', 'avg_rep', 'avg_pause']])
	
	nor_data=preprocessing.normalize(test_data, norm='l2')
	
	user=np.array(df[['user_id']])
	user=user.tolist()
	user=[n for a in user for n in a ]
	
	user_data={}	
	i=0
	for row in test_data:
		user_data[user[i]]=np.array(row).tolist()
		i+=1
		
	print(user_data)

	# test_data:distance matrix
	D = pairwise_distances(nor_data, metric='euclidean')
	
	clustering(D,6,user_data,user)
	

