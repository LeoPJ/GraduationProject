import random
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import os
import cmath
import re
import math as m
import pandas as pd
import json
import pymysql
import kmedoids
import scipy
from sklearn.metrics.pairwise import pairwise_distances
import matplotlib.font_manager as mfm
from sklearn import preprocessing, metrics


def clustering(distance,k,data,user):
	M,C=kmedoids.kMedoids(distance,k,tmax=10000)
	
	#写入中心点
	write_file('medoids:')
	i=1
	for point_idx in M:
		write_file("第{}类中心点：".format(i))
		write_file("id："+user[point_idx])
		write_file("行为序列："+str(data[point_idx]))
		i+=1
	
	write_file('')
	write_file('clustering result:')
	for label in C:
		write_file("第{0}类：共有{1}个学习者".format(label+1,len(C[label])))	
	
	for label in C:
		write_file('')
		write_file("第{0}类：共有{1}个学习者".format(label+1,len(C[label])))
		for point_idx in C[label]:
			write_file('id:{0}:{1}'.format(user[point_idx],str(data[point_idx])))

def generate_uniform_points(data):
    mins = np.argmin(data, axis=0)
    maxs = np.argmax(data, axis=0)

    num_dimensions = data.shape[1]
    num_datapoints = data.shape[0]

    reference_data_set = np.zeros((num_datapoints,num_dimensions))
    for i in range(num_datapoints):
        for j in range(num_dimensions):
            reference_data_set[i][j] = random.uniform(data[mins[j]][j],data[maxs[j]][j])

    return reference_data_set

def ref_gap(num):

    num_dimensions = 2
    num_datapoints = num
    
    gaps=[]
    for k in range(1,11):
	    gap_sum=0
	    for r in range(0,20):
		    #生成随机点
		    reference_data_set = np.zeros((num_datapoints,num_dimensions))
		    for i in range(num_datapoints):
		        for j in range(num_dimensions):
		            reference_data_set[i][j] = random.uniform(0,1)
		    # ~ print(reference_data_set)
		    
		    #计算随机点的距离矩阵
		    distance = pairwise_distances(reference_data_set, metric='euclidean')
		    # ~ plt.scatter(reference_data_set[:,0],reference_data_set[:,1])
		    # ~ plt.show()
		    
		    #聚类
		    M,C=kmedoids.kMedoids(distance,k,tmax=10000)
		    #计算Gap
		    D=0
		    for label in C:
			    dist_sum=0
			    temp=C[label].copy()
				
			    for point_idx in C[label]:
				    for item in temp:
					    dist_sum=distance[item][point_idx]+dist_sum
					
			    D=D+dist_sum/(2*len(C[label]))
			
		    gap_sum+=D
		
	    gaps.append(np.log(gap_sum/20))
    return gaps


def gap(distance,k):
	M,C=kmedoids.kMedoids(distance,k,tmax=10000)

	D=0
	for label in C:
		dist_sum=0
		temp=C[label].copy()
		
		for point_idx in C[label]:
			for item in temp:
				dist_sum=distance[item][point_idx]+dist_sum
			
		D=D+dist_sum/(2*len(C[label]))
	
	return np.log(D)
			

if __name__ == '__main__':
	
	df = pd.read_csv("/home/cuper/python_work/Lab_code/final/final_features_v2.csv", low_memory=False)
	course_id='course-v1:TsinghuaX+80512073X+2016_TS'
	df['user_id'] = df['user_id'].astype('str')
	df = df[(df['course_id']==course_id)]
	test_data = np.array(df[['participations', 'com_threads', 'comments', 'avg_length', 'per_open', 'per_vtotal', 'per_vcompl', 'avg_rep', 'avg_pause']])
	test_data=preprocessing.normalize(test_data, norm='l2')
	
	ref_data=generate_uniform_points(test_data)
	ref_data=preprocessing.normalize(ref_data, norm='l2')

	# test_data:distance matrix
	D = pairwise_distances(test_data, metric='euclidean')

	# ref_data:distance matrix
	ref_D = pairwise_distances(ref_data, metric='euclidean')
	
	Gaps_sum=[]

	for j in range(0,10):	
		gaps=[]
		for i in range(2,11):
			gaps.append(gap(D,i))
		print(gaps)
	
		ref_gaps=[]
		for i in range(2,11):
			ref_gaps.append(gap(ref_D,i))
		print(ref_gaps)
		
		Gap=[]
		for i in range(0,9):
			Gap.append(ref_gaps[i]-gaps[i])
		print(Gap)
		
		Gaps_sum.append(Gap)
	
	print(Gaps_sum)
	
	c=np.array(Gaps_sum)
	print(c)
	
	avg=c.mean(axis=0)
	avg_sum=avg.tolist()
	print(avg_sum)
	
	x=[2,3,4,5,6,7,8,9,10]
	
	#绘Gap图
	# ~ plt.plot(x,gap_high_Cos,label='analysis')
	# ~ plt.plot(x,ref_gaps,label='reference')
	# ~ plt.xlabel('K')
	# ~ plt.ylabel('logWk')
	# ~ plt.legend()
	# ~ plt.show()
	plt.plot(x,avg_sum)
	plt.xlabel('K')
	plt.ylabel('Gaps')
	plt.xticks(x)
	plt.grid()
	plt.show()
	
	
