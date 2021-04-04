import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit


def expFunc(x, a, b):
    return a * np.exp( -b * x )


def fitFunc(data):

    par, cov = curve_fit(f=expFunc, xdata=data.X, ydata=data.Y, sigma=data.errY, absolute_sigma=True)

    residuals = np.array(data.Y) - expFunc(np.array(data.X), *par)
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



    dataAg = pd.read_csv('./testAg.txt', sep = ';', header = None, names = ['X', 'Y', 'errY'])
    dataAg['X'] = dataAg['X'] * 1e-4

    parAg, par_errorAg, chi2Ag = fitFunc(dataAg)
    
    ax.errorbar(x=dataAg.X, y=dataAg.Y, yerr=dataAg.errY, marker = '.', markersize = 15, linewidth = 0, elinewidth = 1, capsize = 1, color = '#0451FF', label = 'Ag Data')
    ax.plot(np.arange(np.amin(dataAg.X), np.amax(dataAg.X), 0.0001), expFunc(np.arange(np.amin(dataAg.X), np.amax(dataAg.X), 0.0001), *parAg), linestyle = '--', linewidth = 2, color = '#FF4B00' , label = 'Ag Fit')

    textI0Ag = 'I$_0$ = ' + format(parAg[0], '1.2f') + ' +/- ' + format(par_errorAg[0], '1.2f') + ' unità di misura'
    textMuAg = '$\mu$ = ' + format(parAg[1], '1.2f') + ' +/- ' + format(par_errorAg[1], '1.2f') + ' unità di misura'
    chisqAg = '$\chi^{2}$ / ndf = ' + format(chi2Ag, '1.2f') + ' / ' + format(len(dataAg.X) - len(parAg), '1.0f')

    ax.text(0.50, 0.20, 'Argento\n' + textI0Ag + '\n' + textMuAg + '\n' + chisqAg, fontsize = 14, color = '#000000', transform = ax.transAxes)



    dataCu = pd.read_csv('./testCu.txt', sep = ';', header = None, names = ['X', 'Y', 'errY'])
    dataCu['X'] = dataCu['X'] * 1e-4

    parCu, par_errorCu, chi2Cu = fitFunc(dataCu)

    ax.errorbar(x=dataCu.X, y=dataCu.Y, yerr=dataCu.errY, marker = '*', markersize = 10, linewidth = 0, elinewidth = 1, capsize = 1, color = '#0451FF', label = 'Cu Data')
    ax.plot(np.arange(np.amin(dataCu.X), np.amax(dataCu.X), 0.0001), expFunc(np.arange(np.amin(dataCu.X), np.amax(dataCu.X), 0.0001), *parCu), linestyle = '-.', linewidth = 2, color = '#FF4B00', label = 'Cu Fit')

    textI0Cu = 'I$_0$ = ' + format(parCu[0], '1.2f') + ' +/- ' + format(par_errorCu[0], '1.2f') + ' unità di misura'
    textMuCu = '$\mu$ = ' + format(parCu[1], '1.2f') + ' +/- ' + format(par_errorCu[1], '1.2f') + ' unità di misura'
    chisqCu = '$\chi^{2}$ / ndf = ' + format(chi2Cu, '1.2f') + ' / ' + format(len(dataCu.X) - len(parCu), '1.0f')

    ax.text(0.50, 0.40, 'Rame\n' + textI0Cu + '\n' + textMuCu + '\n' + chisqCu, fontsize = 14, color = '#000000', transform = ax.transAxes)
    
    plt.legend()

    plt.show()

    return




if __name__ == "__main__":
   main()
