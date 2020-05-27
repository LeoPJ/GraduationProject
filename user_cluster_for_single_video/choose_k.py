import pandas as pd
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import matplotlib.font_manager as mfm
 
# ~ df_features = pd.read_csv(r'data_nor.csv',encoding='utf-8') # 读入数据
# ~ X = df_features.iloc[:, [0,1,2,3,4,5,6,7]].values
# ~ #df_features = pd.read_csv("data_nor.csv",sep= "\s+|\t+|\s+\t+|\t+\s+",header=0)
# ~ print(df_features)
# ~ '利用SSE选择k'
# ~ SSE = []  # 存放每次结果的误差平方和
# ~ for k in range(1,20):
    # ~ estimator = KMeans(n_clusters=k)  # 构造聚类器
    # ~ estimator.fit(X)
# ~ #   estimator.fit(df_features[['0','1','2','3','4','5','6','7']])
    # ~ SSE.append(estimator.inertia_) # estimator.inertia_获取聚类准则的总和

#SSE=[3.0, 1.5025205706573934, 0.964178701985966, 0.715467232838420168, 0.507094140447025748, 0.403510534121262069, 0.3020715826182855814]#hc
SSE=[2.9999999999999996, 1.0003485086327717, 0.501077425356168, 0.1408326987700918, 0.06903825325378132, 0.02241081590664066, 0.00873447784040722]
X = range(1,8)
plt.xlabel('k')
plt.ylabel('SSE')
plt.plot(X,SSE,'o-')
zhfont1 = mfm.FontProperties(fname='/usr/share/wine/fonts/simsun.ttc')
plt.title('肘部法则寻找最佳K值',fontproperties=zhfont1)
plt.show()
