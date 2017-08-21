# -*- coding: utf-8 -*-
"""
Created on Fri Aug 18 16:31:06 2017

@author: mxc13
"""
import numpy as np

e, pi, y, pc, m  = np.loadtxt(r"..\data\epiypcomm_Jan92_Feb17.txt").transpose()
data = np.concatenate([pc[:,np.newaxis], e[:,np.newaxis], pi[:,np.newaxis], y[:,np.newaxis],  m[:,np.newaxis]], axis=1)
data.shape

from VECMml import VECM

p = 4
r = 1
var_names = ['pc', 'e', 'pi', 'y', 'm']
shocks = ['commodity', 'target', 'cost-push', 'demand', 'monetary policy']
model = VECM(data, p, r, var_names=var_names, shock_names=shocks)

print('\nReduced form residual covariance matrix Sigma:\n',
      model.Sigma_u)
#print(model.beta)
model.normalize()
print('\nComnpanion matrix form of the VAR:\n', model.companion)
#print(model.beta)
model.get_LR_impact()
print('\nshort run estimates Gamma\n:', model.Gamma)

print('\nlong run matrix XI:\n', model.Xi)

''' reproduce restrictions from Helmut
    where 0 means restriced and 1 means unrestricted
'''
K = model.K
SR = np.ones((K,K))
SR[0,3:] = 0
SR[1,4] = 0
print('\nidentifying short run restrictions:\n', SR)
SR = SR == 1.

LR = np.zeros((K,K), dtype=int)
LR[:,0] = 1
LR[1:,1] = 1
LR[2:,2] = 1
print('\nidentifying long run restrictions:\n', LR)
LR = LR == 1.

model.set_restrictions(SR, LR)

B0inv_guess = np.random.rand(3,3)#np.linalg.cholesky(model.Sigma_u)
#errs = model.restriction_errors(B0inv_guess)
#print(errs)
model.get_B0inv()
#print(model.opt_res)

print('\nResult for B0inv:\n', model.B0inv)

print('\nCompare to cholesky:\n', np.linalg.cholesky(model.Sigma_u))

print('\nResult for Upsilon:\n', model.Xi @ model.B0inv)

irf_fig = model.get_irfs(nsteps=40, B='chol', plot=True, imps=[4])
irf_fig.savefig('irf.pdf')
