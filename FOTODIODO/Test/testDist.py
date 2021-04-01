import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit


def invSquare(x, x0, a, b):
    return a + b / (x+x0)**2


def fitFunc(data):

    par, cov = curve_fit(f=invSquare, xdata=data.X, ydata=data.Y, p0=[1, 100, 100])

    residuals = np.array(data.Y) - invSquare(np.array(data.X), *par)
    chi2 = np.sum((residuals / np.array(1))**2)

    # get parameters error from cov matrix
    par_error = np.zeros(len(par))

    for i in range(len(par)):
        try:
            par_error[i] = cov[i][i]**0.5
        except:
            par_error[i] = 0.00

    return par, par_error, chi2



def main():

    fig, ax = plt.subplots(ncols=1, figsize=(12,6))
    fig.tight_layout()


    data = pd.read_csv('./testDist.txt', sep = ';', header = None, names = ['X', 'Y'])

    par, par_error, chi2 = fitFunc(data)
    
    ax.plot(data.X, data.Y, marker = '.', markersize = 15, linewidth = 0, color = '#0451FF', label = 'Data')
    ax.plot(np.arange(np.amin(data.X), np.amax(data.X), 0.01), invSquare(np.arange(np.amin(data.X), np.amax(data.X), 0.01), *par), linestyle = '--', linewidth = 2, color = '#FF4B00' , label = 'Fit')

    textX0 = 'x$_0$ = ' + format(par[0], '1.4f') + ' +/- ' + format(par_error[0], '1.4f') + ' unità di misura'
    textScale = 'scale = ' + format(par[1], '1.4f') + ' +/- ' + format(par_error[1], '1.4f') + ' unità di misura'
    textOffset = 'offset = ' + format(par[2], '1.4f') + ' +/- ' + format(par_error[2], '1.4f') + ' unità di misura'
    chisqAg = '$\chi^{2}$ / ndf = ' + format(chi2, '1.2f') + ' / ' + format(len(data.X) - len(par), '1.0f')

    ax.text(0.50, 0.50, textX0 + '\n' + textScale + '\n' + textOffset + '\n' + chisqAg, fontsize = 14, color = '#000000', transform = ax.transAxes)

    
    plt.legend()

    plt.show()

    return



if __name__ == "__main__":
    main()
