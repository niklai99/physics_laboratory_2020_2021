import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit


def main():

    # create figure and axes 
    fig, ax1 = plt.subplots(ncols=1, figsize=(12,6))

    # read data
    dataAg = pd.read_csv('Ag2.txt', sep = '\t', header = None, names = ['X', 'Y','errY'])
    dataCu = pd.read_csv('Cu2.txt', sep = '\t', header = None, names = ['X', 'Y','errY'])
    
    # plot data
    ax1.errorbar(dataAg.X, dataAg.Y, dataAg.errY, marker = '.', linewidth = 1, linestyle = 'dashed', elinewidth = 1, capsize = 1, color = '#0451FF', label = 'Ag data')
    ax1.set_xlabel('Spessore [$\mu$m]', fontsize = 16, loc = 'center')
    ax1.set_ylabel('Efficienza relativa', fontsize = 16, loc = 'top',color = '#0451FF')
    ax1.tick_params(axis='y', labelcolor='#0451FF')
    
    ax2 = ax1.twinx()
    ax2.errorbar(dataCu.X, dataCu.Y, dataCu.errY, marker = '.', linewidth = 1, linestyle = 'dashed', elinewidth = 1, capsize = 1, color = '#FF0451', label = 'Cu data')
    ax2.set_ylabel('Efficienza relativa', fontsize = 16, loc = 'bottom',color = '#FF0451')
    ax2.tick_params(axis='y', labelcolor='#FF0451')

    # set legend 
    h1, l1 = ax1.get_legend_handles_labels()
    h2, l2 = ax2.get_legend_handles_labels()
    ax1.legend(h1+h2, l1+l2, loc='best', prop={'size':16})
    
    #fig.tight_layout()
    plt.show()

    # save figure
    #fig.savefig('efficiency.jpg', dpi = 300)

    return



if __name__ == "__main__":
    main()
