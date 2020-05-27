import os
import numpy as np
import Levenshtein
import cmath
from sklearn.cluster import KMeans
import re
from sklearn.mixture import GaussianMixture
import math as m
import pandas as pd
import json
import matplotlib.pyplot as plt

def getW(dicts):
    """
    利用 polar 距离 获得相似矩阵
    :param data: 样本集合
    :return:
    """
    Matrix = np.zeros((len(dicts), len(dicts)))
    for i, no_i in enumerate(dicts):
        for j, no_j in enumerate(dicts):
            if i == j:
                pass
            else:
                Matrix[i][j] = get_sim(dicts[no_i], dicts[no_j],1)

    return Matrix

def getD(W):
    """
    获得度矩阵
    :param W:  相似度矩阵
    :return:   度矩阵
    """
    D = np.diag(sum(W))
    return D

def getL(D, W):
    """
    获得拉普拉斯矩阵
    :param W: 相似度矩阵
    :param D: 度矩阵
    :return: 拉普拉斯矩阵
    """
    return D - W

def getEigen(L):
    """
    从拉普拉斯矩阵获得特征(映射)矩阵
    :param L: 拉普拉斯矩阵
    :return:
    """
    eigval, eigvec = np.linalg.eig(L)
    # 取特征向量的前 4 个，但第一个都一样，可以去掉
    ix = np.argsort(eigval)[0:4]
    return eigvec[:, ix]

def k_gram(seq,k):
	seq_list=[]
	if k>len(seq):
		return seq_list
	else:
		for i in range(0,len(seq)-k+1):
			seq_list.append(seq[i:i+k])

	return seq_list

def get_bing(list1,list2):
	t=[]
	for row in list1:
	    if row not in t:
	        t.append(row)
	        
	for row in list2:
		if row not in t:
			t.append(row)
	
	return t

def get_jiao(list1,list2):
	t=[]
	
	for row in list1:
		if row in list2 and row not in t:
			t.append(row)
	
	return t

def get_Jaccard(list1,list2,k):
	l1=k_gram(list1,k)
	l2=k_gram(list2,k)

	# ~ print(l1)
	# ~ print(l2)
	
	return len(get_jiao(l1,l2))/len(get_bing(l1,l2))

def find_index(lists, find):
    """
    在lists里面，找出find在lists的索引
    :param lists: 列表
    :param find: 列表中的一个元素
    :return: 一个在lists里面，找出find在lists的索引列表
    """
    flag = 0
    list_index = []
    for n in range(lists.count(find)):
        sec = flag
        flag = lists[flag:].index(find)
        list_index.append(flag + sec)
        flag = list_index[-1:][0] + 1
    return list_index

def get_sim(list1,list2,k):
	l1=k_gram(list1,k)
	l2=k_gram(list2,k)

	# ~ print(l1)
	# ~ print(l2)
	
	
	t=get_bing(l1,l2)
	
	c1=[]
	c2=[]
	
	for l in t:
		num1=0
		num2=0
		for row in l1:
			if row==l:
				num1+=1
		for row in l2:
			if row==l:
				num2+=1
		c1.append(num1/len(l1))
		c2.append(num2/len(l2))
	
	# ~ print(c1)
	# ~ print(c2)
	
	sum1=0
	sum_c1=0
	sum_c2=0
	for i in range(0,len(c1)):
		sum1+=c1[i]*c2[i]
		sum_c1+=c1[i]**2
		sum_c2+=c2[i]**2
	
	# ~ print(sum1)
	# ~ print(sum_c1)
	# ~ print(sum_c2)

	cos=sum1/((sum_c1**0.5)*(sum_c2**0.5))

	return cos

def write_file(str):
    """
    写入文件
    :param str: 字符串
    :return: 无
    """
    writefile = open("./out/ENG/ENG_output_code3.txt", 'a+',encoding='utf-8')
    writefile.write(str + '\n')
    writefile.close()


f=open('./data/ENG_data_code3.txt', 'r')
data=eval(f.read())

print(data)
print(len(data))

W=getW(data)
for row in W:
	print(row)
D = getD(W)
L = getL(D, W)
eigvec = getEigen(L).astype(float)


SSE=[]
m=0
for cluster_num in range(2,10):
	#print((cluster_num - 50)/150,cluster_num)
	print(m)

	# 使用kmeans 聚类 
	clf = KMeans(n_clusters=cluster_num,init='k-means++',max_iter=10000)
	s = clf.fit(eigvec)
	C = s.labels_
	SSE.append(clf.inertia_)

    # 写入聚类结果
	write_file("*********【分{}类】*********".format(cluster_num))
	for i in range(cluster_num):
		cluster_index = find_index(list(C),i)

		tem_list = []
		for index in cluster_index:
			for row in list(enumerate(data)):
				if index==row[0]:
					user_id=row[1]
					break
			tem_list.append(data[user_id])
		write_file("…………【第{}类】…………".format(i+1),)
		for print_str in tem_list:
			write_file(str(print_str))
			write_file('---------------------------------')
		write_file('==================================================================')
	
	print(m)
	m+=1


#肘部法则找k值
X = range(2,10)
plt.xlabel('k')
plt.ylabel('SSE')
plt.plot(X,SSE,'o-')
plt.show()

# ~ print(data['3166971'])
# ~ print(data['2916280'])


# ~ print(get_sim(data['3166971'],data['2916280'],4))
# ~ print(get_sim(data['35012'],data['3166971'],1))

# ~ print(get_Jaccard(data['3166971'],data['2916280'],2))
