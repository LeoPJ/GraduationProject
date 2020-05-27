import pymysql
import time
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.font_manager as mfm
import os
from itertools import chain
import json

f = open('ENGdata.txt', 'r')
data = eval(f.read())
cluster_sta=data

# ~ print(cluster_sta)
# ~ print(cluster_sta['anonymous_id-anonymous_id-c7150a5a5a6ddcdca40a5588b1fc734f'])

# ~ print(str(type(cluster_sta)))

# ~ t1=json.dumps(cluster_sta,ensure_ascii=False)
# ~ print(str(type(t1)))

# ~ print(t1)


# ~ del cluster_sta['968361']
# ~ del cluster_sta['400758']
# ~ del cluster_sta['2490333']
# ~ del cluster_sta['2048264']
# ~ del cluster_sta['anonymous_id-anonymous_id-376bee5a65e0530d055c64ec7228727e']
# ~ del cluster_sta['2529622']
# ~ del cluster_sta['3058341']
# ~ del cluster_sta['279691']


# ~ del cluster_sta['2024908']
# ~ del cluster_sta['3058341']
# ~ del cluster_sta['1544321']
# ~ del cluster_sta['1992458']
# ~ del cluster_sta['2618680']
# ~ del cluster_sta['3697332']
# ~ del cluster_sta['2740371']
# ~ del cluster_sta['3058341']
# ~ del cluster_sta['2024908']
del cluster_sta['2651376']
del cluster_sta['279691']
del cluster_sta['3058341']


user_seq=[]
i=0
for k,v in cluster_sta.items():
	if len(v)!=1 or (len(v)==1 and v[0][1]=='A'):
		dic={'no':i,"INPATIENT_NO":k,"ONE_HOT":v}
		user_seq.append(dic)
		i+=1

print(user_seq)
print(type(user_seq))
jsonArr=json.dumps(user_seq,ensure_ascii=False)
print(type(jsonArr))

filename='./sequence_clustering/data/ENG/ENG(code1e)_users.json'
with open(filename,'w') as f:
	json.dump(user_seq,f,ensure_ascii=False)
	
print(len(user_seq))

	
