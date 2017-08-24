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

# load data
e, cpi, y, pc, m  = np.loadtxt(r"..\data\epiypcomm_Jan92_Feb17.txt").transpose()

# first differenc od cpi as annualized inflatin rate
pi = (cpi[1:] - cpi[:-1]) * 1200

X = np.concatenate([pc[1:,None], e[1:,None],
                    pi[:,None], y[1:,None],
                    m[1:,None]], axis=1)
var_names = ['pc', 'e', 'pi', 'y', 'm']


dates = pd.date_range(start='1992-01', periods=len(endog), freq='M')
pd.DatetimeIndex(dates)
endog = pd.DataFrame(X, columns=var_names)
endog.set_index(dates)



print('\nAre there any missings?', pd.isnull(endog).any().any(),'.')

#select lag order by criteria
lag_crit = sm.VAR(endog, dates=dates, freq='m').select_order()
p = lag_crit['aic']
h = 48

recVar = sm.VAR(endog, dates=dates, freq='m').fit(maxlags=12, ic='aic')
#irfs = recVar.irf(h)
#irfs.plot()
Sigma_u = recVar.sigma_u

fevd = recVar.fevd(h)
# fevd of the second variable
fevd_e5 = fevd.decomp[1,:,:]

from fevd_plot import plot_fevd
from color_table import tableau20
#plot_fevd(fevd_e5, var_names)

fig, ax = plt.subplots()
ax.stackplot(np.arange(h), fevd_e5.T, alpha=0.9, labels=var_names,
             colors=[tableau20[0], tableau20[5], tableau20[13], tableau20[2], tableau20[18]])
ax.set_xlim((0,h-1))
ax.set_ylim((0,1))
ax.set_xlabel('horizon')
ax.legend()
ax.set_title('FEVD of Inflation Expectations (cholesky)')
plt.show()
