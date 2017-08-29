import os
import shutil

#from datetime import datetime
import numpy as np
import pandas as pd
import statsmodels.tsa.api as sm
from patsy import dmatrix
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

# sub divide data into different categories of variables over whoch to loop to find the best model
var_list = data.columns

price_list = list(var_list[2:4])
rea_list = list(var_list[4:9])
info_list = list(var_list[[0, 1, 9]])
divisia_list = list(var_list[11:16])
usercost_list = list(var_list[16:])

mb = data.mb

A = np.repeat('0', 36).reshape((6,6))
np.fill_diagonal(A, 'e')
A[1, 0] = 'e'
for i in range(1,6): A[i,:i] = 'e'

for a, price_name in enumerate(price_list):
    price = data[price_name]

    for b, rea_name in enumerate(rea_list):
        rea = data[rea_name]

        for c, info_name in enumerate(info_list):
            info = data[info_name]

            for d, div_name in enumerate(divisia_list):
                uc_name = usercost_list[d]
                divisia = data[div_name]
                ucost = data[uc_name]


                X = pd.concat([price, rea, info, divisia, ucost, mb], axis=1)

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

print('\nDone producing', len(price_list)*len(rea_list)*len(info_list)*len(divisia_list) ,'Graphs...\n')
#irfs_analysis.plot()
#plt.show()

#fevd = recVar.fevd(h)
# fevd of the second variable
#fevd_e5 = fevd.decomp[1,:,:]

#from fevdplot import plot_fevd
#from color_table import tableau20

#fevdfig = plot_fevd(fevd_e5, var_names=var_names, title='FEVD of Inflation Expectations (cholesky)')
#fevdname = 'fevd_inf_exp_recursive' + '_' + sample + '_' + 'p' +str(p) + '.pdf'
#print(fevdname)
#fevdfig.savefig(os.path.join(grafics_dir, fevdname))
#plt.show()
