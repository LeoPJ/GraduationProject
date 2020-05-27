import pymysql
import time
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.font_manager as mfm
import os
from itertools import chain
import networkx as nx
from Class_GraphMatrix import Graph_Matrix

def str2time(a1):
	# 先转换为时间数组
	timeArray = time.strptime(a1, "%Y-%m-%d %H:%M:%S")
	# 转换为时间戳
	timeStamp = int(time.mktime(timeArray))
	return timeStamp

def create_undirected_matrix(my_graph):
	nodes = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']

	matrix = [[0, 1, 1, 1, 1, 1, 0, 0],  # a
			  [0, 0, 1, 0, 1, 0, 0, 0],  # b
			  [0, 0, 0, 1, 0, 0, 0, 0],  # c
			  [0, 0, 0, 0, 1, 0, 0, 0],  # d
			  [0, 0, 0, 0, 0, 1, 0, 0],  # e
			  [0, 0, 1, 0, 0, 0, 1, 1],  # f
			  [0, 0, 0, 0, 0, 1, 0, 1],  # g
			  [0, 0, 0, 0, 0, 1, 1, 0]]  # h

	my_graph = Graph_Matrix(nodes, matrix)
	print(my_graph)
	return my_graph

def create_directed_matrix(my_graph,nodes,matrix):
	# ~ nodes = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
	# ~ inf = float('inf')
	# ~ matrix = [[0, 2, 1, 3, 9, 4, inf, inf],  # a
			  # ~ [inf, 0, 4, inf, 3, inf, inf, inf],  # b
			  # ~ [inf, inf, 0, 8, inf, inf, inf, inf],  # c
			  # ~ [inf, inf, inf, 0, 7, inf, inf, inf],  # d
			  # ~ [inf, inf, inf, inf, 0, 5, inf, inf],  # e
			  # ~ [inf, inf, 2, inf, inf, 0, 2, 2],  # f
			  # ~ [inf, inf, inf, inf, inf, 1, 0, 6],  # g
			  # ~ [inf, inf, inf, inf, inf, 9, 8, 0]]  # h

	my_graph = Graph_Matrix(nodes, matrix)
	print(my_graph)
	return my_graph

def create_directed_graph_from_edges(my_graph):
	nodes = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
	edge_list = [('A', 'F', 9), ('A', 'B', 10), ('A', 'G', 15), ('B', 'F', 2),
				 ('G', 'F', 3), ('G', 'E', 12), ('G', 'C', 10), ('C', 'E', 1),
				 ('E', 'D', 7)]

	my_graph = Graph_Matrix(nodes)
	my_graph.add_edges_from_list(edge_list)
	print(my_graph)

	# my_graph.DepthFirstSearch()
	#
	# draw_directed_graph(my_graph)

	return my_graph



def draw_undircted_graph(my_graph):
	G = nx.Graph()  # 建立一个空的无向图G
	for node in my_graph.vertices:
		G.add_node(str(node))
	for edge in my_graph.edges:
		G.add_edge(str(edge[0]), str(edge[1]))

	print("nodes:", G.nodes())  # 输出全部的节点
	print("edges:", G.edges())  # 输出全部的边
	print("number of edges:", G.number_of_edges())  # 输出边的数量
	nx.draw(G, with_labels=True)
	plt.savefig("undirected_graph.png")
	plt.show()


def draw_directed_graph(my_graph):
	G = nx.DiGraph()  # 建立一个空的无向图G
	for node in my_graph.vertices:
		G.add_node(str(node))
	# for edge in my_graph.edges:
	# G.add_edge(str(edge[0]), str(edge[1]))
	G.add_weighted_edges_from(my_graph.edges_array)

	print("nodes:", G.nodes())  # 输出全部的节点
	print("edges:", G.edges())  # 输出全部的边
	print("number of edges:", G.number_of_edges())  # 输出边的数量
	nx.draw(G, with_labels=True)
	#plt.savefig("directed_graph.png")
	plt.show()




we = [([0] * 59) for i in range(59)]

# 打开数据库连接
db = pymysql.connect("localhost","root","hh0326lpj","videos" )
 
# 使用cursor()方法获取操作游标 
cursor = db.cursor()
 
sql = "SELECT distinct user_id FROM cj_analysis"
# 执行SQL语句
cursor.execute(sql)
# 获取所有记录列表
user_id = cursor.fetchall()

user_list=[]
k=0

for row in user_id:
	user_list.append(row[0])
# ~ print(user_list)
print(len(user_list))


for user in user_list:
	sql="select distinct seq,start_localtime from cj_analysis where user_id=\'"+user+"\' order by start_localtime"
	
	cursor.execute(sql)
	logs=cursor.fetchall()
	
	# ~ for row in logs:
		# ~ print(row)

	for i in range(0,len(logs)-1):
		if logs[i][0]!=logs[i+1][0]:
			if str2time(logs[i+1][1])-str2time(logs[i][1])<1800:
				we[logs[i][0]][logs[i+1][0]]+=1
	if k%100==0:
		print(k)
	# ~ if k>1000:
		# ~ break
	k+=1

for row in we:
	print(row)

print(we)



inf = float('inf')
for i in range(0,59):
	for j in range(0,59):
		if we[i][j]<70 and i!=j:
			we[i][j]=inf
			
for row in we:
	print(row)

print(we)

nodes=[]
for i in range(0,59):
	nodes.append(str(i))
print(nodes)

my_graph = Graph_Matrix()
created_graph = create_directed_matrix(my_graph,nodes,we)
draw_directed_graph(created_graph)
