import os
import shutil

import numpy as np
import pandas as pd
import statsmodels.tsa.api as sm

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

os.chdir(r'C:\Users\Max\Documents\Master\Inflation Expectations\git_repository\master_thesis\python')
# repositories for saving results
grafics_dir = r'grafics/benchmark'

# update data file
data_path = r'C:\Users\Max\Documents\Master\Inflation Expectations\data\keating_bel.csv'
shutil.copy(data_path, r'..\data\keating_bel.csv')

# load data
data_raw = pd.read_csv(r"..\data\keating_bel.csv", sep=';', index_col=0)
dates = data_raw.index

# selecting common sample
data = data_raw.loc['1992-02':'2016-07']
nobs = data.shape[0]

var_list = data.columns

X = data[['l_cpi', 'u',  mb], axis=1)

var_names = [price_name, rea_name, info_name, div_name, uc_name, 'mb']
shock_names = ['cost push', 'demand', 'pcom/infl.target', 'mon. pol', 'finance cost', 'mon. base']


#select lag order by criteria
#p = sm.VAR(X, dates=dates, freq='m').select_order(disp=0)['aic']
#print(p)
h = 48
recVar = sm.VAR(X, dates=X.index, freq='m').fit(maxlags=15, ic='aic')
ASigma = np.linalg.cholesky(recVar.sigma_u)
# save the lag length
p = recVar.k_ar

' gather some infos about the specification for saving'
sample = [str(recVar.dates.min()).split()[0], str(recVar.dates.max()).split()[0]]
sample = '_to_'.join(sample)
lags = ': '.join(['lags', str(p)])
info_string = ', '.join([sample, lags])

irfs_analysis = recVar.irf(h)
ci_lower, ci_upper = recVar.irf_errband_mc(T=48)

from plotirfs import plot_irfs
rec_irfs = plot_irfs(irfs_analysis.irfs, ci_lower, ci_upper, imps=[0, 1, 3], resps=[0, 1, 2, 3, 4, 5],
                     shock_names=shock_names, var_names=var_names,
                     title=info_string)

var_name_string = '-'.join(var_names)
filename = var_name_string + '_' + sample +  '_' + 'p' +str(p) + '.pdf'
rec_irfs.savefig(os.path.join(grafics_dir, filename))
plt.close()
