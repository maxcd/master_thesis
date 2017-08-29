from color_table import tableau20
import matplotlib.pyplot as plt
import numpy as np
def plot_fevd(fevd_table, var_names=None, title=None):

    if var_names is None:
        var_names = np.arange(fevd_table.shape[1])

    h = len(fevd_table)
    hatches = ['/', 'o', '*', '//', '+']
    fig, ax = plt.subplots()
    stacks = ax.stackplot(np.arange(h), fevd_table.T, alpha=0.7, labels=var_names,
                 edgecolor='black',
                 colors=[tableau20[0], tableau20[5], tableau20[13], tableau20[2], tableau20[18]])

    for stack, hatch in zip(stacks, hatches):
        stack.set_hatch(hatch)

    ax.set_xlim((0,h-1))
    ax.set_ylim((0,1))
    ax.set_xlabel('horizon')
    ax.set_ylabel('%')
    ax.legend(loc='upper center', bbox_to_anchor=(0.982, 0.85),
              ncol=1, fancybox=True)
    # legend below: bbox_to_anchor=(0.5, -0.05)
    ax.set_title(title)

    return fig
