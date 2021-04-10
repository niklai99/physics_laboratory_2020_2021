import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit


def main():

    fig, ax = plt.subplots(ncols=1, figsize=(12,6))


    dataAg = pd.read_csv('Ag2.txt', sep = '\t', header = None, names = ['X', 'Y','errY'])

    
    ax.errorbar(dataAg.X, dataAg.Y, dataAg.errY, marker = '.', linewidth = 1, linestyle = ':', elinewidth = 1, capsize = 1, color = '#0451FF', label = 'Ag Data')
    

    dataCu = pd.read_csv('Cu2.txt', sep = '\t', header = None, names = ['X', 'Y','errY'])

    ax.errorbar(dataCu.X, dataCu.Y, dataCu.errY, marker = '.', linewidth = 1, linestyle = ':', elinewidth = 1, capsize = 1, color = 'Red', label = 'Cu Data')
    
 
    
    ax.set_xlabel('Spessore [$\mu$m]', fontsize = 18, loc = 'center')
    ax.set_ylabel('Efficienza relativa', fontsize = 18, loc = 'top')

    plt.legend()
    plt.show()

    return



if __name__ == "__main__":
    main()
