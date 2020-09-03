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
import matplotlib.font_manager as mfm
import pymysql
import matplotlib
import time
import math


high_sim=np.load("/home/cuper/python_work/GraduationProject/fix/similarity/high_cover_sim_Cos4.npy")
m,n=high_sim.shape
for i in range(0,m):
	for j in range(0,n):
		if i==j:
			pass
		else:
			if high_sim[i][j]>1:
				high_sim[i][j]=1
			high_sim[i][j]=math.acos(high_sim[i][j])/math.pi

np.save('high_cover_distance_Cos4.npy',high_sim)
