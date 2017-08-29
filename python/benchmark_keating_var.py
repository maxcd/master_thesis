import os
import shutil

import numpy as np
import pandas as pd
import statsmodels.tsa.api as sm

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

os.chdir(r'C:\Users\Max\Documents\Master\Inflation Expectations\git_repository\master_thesis\python')
# repositories for saving results
grafics_dir = r'grafics/choose_var/1992-02_to_2016-6'

# update data file
data_path = r'C:\Users\Max\Documents\Master\Inflation Expectations\data\keating_bel.csv'
shutil.copy(data_path, r'..\data\keating_bel.csv')

# load data
data_raw = pd.read_csv(r"..\data\keating_bel.csv", sep=';', index_col=0)
dates = data_raw.index

# selecting common sample
data = data_raw.loc['1992-02':'2016-07']
nobs = data.shape[0]
print('\nAre there any missings?', pd.isnull(data).any().any(),'.')
