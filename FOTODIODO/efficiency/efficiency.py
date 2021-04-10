import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit


def main():


    fig = plt.figure(figsize=(18,6))


    ax1 = fig.add_subplot(1, 2, 1)
    ax2 = fig.add_subplot(1, 2, 2)


    dataAg = pd.read_csv('Ag2.txt', sep = '\t', header = None, names = ['X', 'Y','errY'])

    
    ax1.errorbar(dataAg.X, dataAg.Y, dataAg.errY, marker = '.', linewidth = 1, linestyle = ':', elinewidth = 1, capsize = 1, color = '#0451FF', label = 'Ag Data')
    dataCu = pd.read_csv('Cu2.txt', sep = '\t', header = None, names = ['X', 'Y','errY'])
    leg1 = ax1.legend()
    ax1.add_artist(leg1)
    ax2.errorbar(dataCu.X, dataCu.Y, dataCu.errY, marker = '.', linewidth = 1, linestyle = ':', elinewidth = 1, capsize = 1, color = 'Red', label = 'Cu Data')
    
    ax1.set_xlabel('Spessore [$\mu$m]', fontsize = 18, loc = 'center')
    ax1.set_ylabel('Efficienza relativa', fontsize = 18, loc = 'top')
    

    ax2.set_xlabel('Spessore [$\mu$m]', fontsize = 18, loc = 'center')
    ax2.set_ylabel('Efficienza relativa', fontsize = 18, loc = 'top')

    plt.legend()
    plt.show()

    return



if __name__ == "__main__":
    main()
