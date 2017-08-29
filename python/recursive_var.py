# -*- coding: utf-8 -*-
"""
Created on Thu Aug 24 13:12:08 2017

@author: mxc13
"""

import os
from datetime import datetime
import numpy as np
import pandas as pd
import statsmodels.tsa.api as sm
from patsy import dmatrix
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# repositories for saving results
grafics_dir = r'grafics'

# load data
e, cpi, y, pc, m  = np.loadtxt(r"..\data\epiypcomm_Jan92_Feb17.txt").transpose()

# first differenc od cpi as annualized inflatin rate
pi = (cpi[1:] - cpi[:-1]) * 12

X = np.concatenate([pc[1:,None], e[1:,None],
                    cpi[1:,None], y[1:,None],
                    m[1:,None]], axis=1)
var_names = ['pc', 'e', 'log cpi', 'log r gdp', 'log Dm2m']
shock_names = ['com. price', 'infl.-target', 'cost-push', 'demand', 'mon. pol']

dates = pd.date_range(start='1992-01', periods=len(X), freq='M')
pd.DatetimeIndex(dates)
endog = pd.DataFrame(X, columns=var_names)
endog.set_index(dates)

print('\nAre there any missings?', pd.isnull(endog).any().any(),'.')

#select lag order by criteria
lag_crit = sm.VAR(endog, dates=dates, freq='m').select_order()
p = lag_crit['aic']
h = 48
sample_split = '2007'

recVar = sm.VAR(endog, dates=dates, freq='m').fit(maxlags=p)

' gather some infos about the specification for saving'
sample = [str(recVar.dates.min()).split()[0], str(recVar.dates.max()).split()[0]]
sample = '_to_'.join(sample)
lags = ': '.join(['lags', str(p)])
info = ', '.join([sample, lags])

irfs_analysis = recVar.irf(h)

from plotirfs import plot_irfs
rec_irfs = plot_irfs(irfs_analysis.irfs, imps=[2, 3, 4], resps=[2, 3, 4],
                     shock_names=shock_names, var_names=var_names,
                     title=info)
filename = 'irf_recursive' + '_' + sample +  '_' + 'p' +str(p) + '.pdf'
rec_irfs.savefig(os.path.join(grafics_dir, filename))

#irfs_analysis.plot()
#plt.show()

fevd = recVar.fevd(h)
# fevd of the second variable
fevd_e5 = fevd.decomp[1,:,:]

from fevdplot import plot_fevd
from color_table import tableau20

fevdfig = plot_fevd(fevd_e5, var_names=var_names, title='FEVD of Inflation Expectations (cholesky)')
fevdname = 'fevd_inf_exp_recursive' + '_' + sample + '_' + 'p' +str(p) + '.pdf'
print(fevdname)
fevdfig.savefig(os.path.join(grafics_dir, fevdname))
#plt.show()
