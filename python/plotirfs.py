import numpy as np
import matplotlib.pyplot as plt

def plot_irfs(irf_mat, lower_ci, upper_ci, imps=None, resps=None, var_names=None, shock_names=None
              , title=None):
    if imps is None:
        imps = np.arange(irf_mat.shape[1])

    if resps is None:
        resps = np.arange(irf_mat.shape[2])

    n_imp = len(imps)
    n_res = len(resps)
    nsteps = irf_mat.shape[0]

    if var_names is None:
        var_names = str(np.arange(n_res))

    if shock_names is None:
        shock_names = str(np.arange(n_res))

    fig, axes = plt.subplots(n_res, n_imp)

    if n_imp == 1: axes = axes[:,np.newaxis]

    for ri, r in enumerate(resps):
        for ii, i in enumerate(imps):
            if ri==0 : axes[ri,ii].set_title(shock_names[i])
            x = irf_mat[:,r,i]
            if upper_ci is not None: ci_u = upper_ci[:,r, i]
            if lower_ci is not None: ci_l = lower_ci[:,r, i]
            if shock_names[i] == 'mon. pol':
                x = -1*x
                ci_u = -1*ci_u
                ci_l = -1*ci_l
            axes[ri,ii].plot(np.zeros(nsteps), 'k:')
            axes[ri,ii].plot(x, label=var_names[r])

            axes[ri,ii].fill_between(np.arange(49), ci_l, ci_u, alpha=0.3)

            if ri < len(resps)-1: axes[ri,ii].get_xaxis().set_visible(False)
            if ii==0: axes[ri,ii].set_ylabel(var_names[r])

    if title is not None: fig.suptitle(title)
    plt.tight_layout()
    return fig
