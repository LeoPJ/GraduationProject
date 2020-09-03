# ~ from pyclustering.cluster.kmedoids import kmedoids
# ~ from pyclustering.cluster import cluster_visualizer
# ~ from pyclustering.utils import read_sample
# ~ from pyclustering.samples.definitions import FCPS_SAMPLES
# ~ import pandas as pd
# ~ import numpy as np
# ~ from sklearn import preprocessing, metrics

# ~ df = pd.read_csv("/home/cuper/python_work/Lab_code/final/final_features_v2.csv", low_memory=False)
# ~ course_id='course-v1:TsinghuaX+80512073X+2016_TS'
# ~ df['user_id'] = df['user_id'].astype('str')
# ~ df = df[(df['course_id']==course_id)]
# ~ test_data = np.array(df[['participations', 'com_threads', 'comments', 'avg_length', 'per_open', 'per_vtotal', 'per_vcompl', 'avg_rep', 'avg_pause']])
# ~ test_data=preprocessing.normalize(test_data, norm='l2')
# ~ test_data=test_data.tolist()
# ~ print(test_data)

# ~ # 导入待聚类的样本点。
# ~ # 这里我打印了一下这些数据，整个sample就是一个二维的列表（甚至没有用到numpy包），共有800行（也就是800个数据点），每一行是一个长度为2的列表（就是TWO_DIAMONDS二维数据），列表中的两个数的数据类型为float。导入自己数据进行聚类时可参考这个格式。
# ~ sample = test_data

# ~ # 设定随机的初始中心点索引。
# ~ # 这里中心点的数据类型是一个int类型的列表，列表中每个值代表每一类中心点的索引。注意该列表的长度已经代表了你要聚类的类别个数，也就是说len(initial_medoids)=k。
# ~ initial_medoids = [1,10,4, 500]

# ~ # 创建K-Medoids算法的实例。
# ~ # 这里就创建了kmedoids类的一个对象，__init__函数被调用，这里传入了前两个参数，后面的参数保持默认状态。
# ~ kmedoids_instance = kmedoids(sample, initial_medoids)

# ~ # 进行聚类分析并获取聚类结果。
# ~ kmedoids_instance.process()
# ~ clusters = kmedoids_instance.get_clusters()

# ~ # 打印分配好的聚类结果。
# ~ # 这里的clusters为一个k（本示例k=2）行列表，每一行列表里嵌套一个索引列表，列表里是对应簇中所有点的索引值（int型）。
# ~ print(clusters)

# ~ # 打印各簇中心点。
# ~ # 此段代码官方示例中没有，是我自己为了看一下get_medoids()函数而加的，得到的结果是medoids为一个长度为k的列表，每个元素对应每个簇的中心点的索引值（int型）。
# ~ medoids = kmedoids_instance.get_medoids()
# ~ print(medoids)

# ~ #聚类的可视化，用了模块里的自带功能。
# ~ visualizer = cluster_visualizer()
# ~ visualizer.append_clusters(clusters, sample)
# ~ visualizer.show()

from pyclustering.cluster.kmeans import kmeans, kmeans_visualizer
from pyclustering.cluster.kmedoids import kmedoids
from pyclustering.cluster.center_initializer import kmeans_plusplus_initializer
from pyclustering.cluster.elbow import elbow
from pyclustering.utils import read_sample
from pyclustering.samples.definitions import SIMPLE_SAMPLES
import pandas as pd
import numpy as np
from sklearn import preprocessing, metrics
import matplotlib.pyplot as plt

df = pd.read_csv("/home/cuper/python_work/Lab_code/final/final_features_v2.csv", low_memory=False)
course_id ='course-v1:TsinghuaX+34000888X+2016_TS'
df['user_id'] = df['user_id'].astype('str')
df = df[(df['course_id']==course_id)]
test_data = np.array(df[['participations', 'com_threads', 'comments', 'avg_length', 'per_open', 'per_vtotal', 'per_vcompl', 'avg_rep', 'avg_pause']])
nor_data=preprocessing.normalize(test_data, norm='l2')
sample=nor_data.tolist()


kmin, kmax = 1, 10
elbow_instance = elbow(sample, kmin, kmax)
elbow_instance.process()

amount_clusters = elbow_instance.get_amount()  # most probable amount of clusters
wce = elbow_instance.get_wce()  # total within-cluster errors for each K

print(amount_clusters)
print(wce)

# perform cluster analysis using K-Means algorithm
centers_data = kmeans_plusplus_initializer(sample, amount_clusters,
                                      amount_candidates=kmeans_plusplus_initializer.FARTHEST_CENTER_CANDIDATE).initialize()
centers_index = kmeans_plusplus_initializer(sample, amount_clusters,
                                      amount_candidates=kmeans_plusplus_initializer.FARTHEST_CENTER_CANDIDATE).initialize(return_index=True)
print(centers_data)
print(centers_index)


kmeans_instance = kmeans(sample, centers_data)
kmeans_instance.process()
kmeans_clusters = kmeans_instance.get_clusters()
kmeans_centers = kmeans_instance.get_centers()
for row in kmeans_centers:
	print(row)
print('*********K-Means结果*********')
i=1
for cluster in kmeans_clusters:
	print("第%d类个数：%d"%(i,len(cluster)))
	i+=1


kmedoids_instance = kmedoids(sample, centers_index, itermax=10000)
kmedoids_instance.process()
kmedoids_clusters = kmedoids_instance.get_clusters()
kmedoids_medoids = kmedoids_instance.get_medoids()
for item in kmedoids_medoids:
	print(sample[item])
print('*********K-Medoids结果*********')
i=1
for cluster in kmedoids_clusters:
	print("第%d类个数：%d"%(i,len(cluster)))
	i+=1

x=list(range(1,10))
plt.plot(x,wce)
plt.xlabel('K')
plt.ylabel('error')
plt.xticks(x)
plt.grid()
plt.show()
	
