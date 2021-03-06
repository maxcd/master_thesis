# -*- coding: utf-8 -*-
"""
Created on Mon Aug 21 16:54:09 2017

@author: mxc13
"""

import numpy as np
import pandas as pd
import os 

os.chdir(r"C:\Users\mxc13.FU-BERLIN\Desktop\inflation expectations\master_thesis\python")

data = pd.read_csv(r'../data/monthly_preferred_1.csv', sep=';', index_col=0)
data = data[['e5', 'cpi', 'l_rgdp', 'l_pnfuel', 'l_dm2m']]
mask = pd.isnull(data)
index = mask.sum(axis=0)
index = np.argmax(index)
selector = ~mask[index]
# include one more to be able to take take differences
selector['1991-12-01'] = True
data = data[selector]

data = data.values

np.savetxt('..\data\epiypcomm_Jan92_Feb17.txt', data)
