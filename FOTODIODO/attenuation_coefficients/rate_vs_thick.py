# Python script to plot and fit event rates versus barrier thickness.
# A linear fit is computed, in addition to the required exponential fit.

# Usage: python rate_vs_thick.py filename.txt
#  where filename.txt is the name of the file containg data in the following format:
#  [x  x1  y  errY]

# Example: python rate_vs_thick.py data_ag_rate.txt


# TODO:
# 1) normalize y before taking log in the linear fit
# 2) add offset to the exponential fit
# 3) get label from cmd

import sys 
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit


def expFunc(x, a, b):
    # PROBLEM: adding an offset " + c "
    # makes the fit awful 
    return a * np.exp( -b * x ) 

def linFunc(x, m, q):
    return m*x + q



# fit given data and return best fit parameters (with errors)
# and residuals.
# choice==0 -> exponential fit
# choice==1 -> linear fit
def fitFunc(X,Y,errY,choice):

    # fit data according to ~choice~

    if choice==0: # exponential fit

        par, cov = curve_fit(f=expFunc, xdata=X, ydata=Y,
                             sigma=errY, absolute_sigma=True,)

        residuals = np.array(Y) - expFunc(np.array(X), *par)


    elif choice==1: # lienar fit

        Y = np.log(Y)
        errY = errY/Y

        par, cov = curve_fit(f=linFunc, xdata=X, ydata=Y,
                             sigma=errY, absolute_sigma=True)

        # fit goodness
        residuals = np.array(Y) - linFunc(np.array(X), *par)


    chi2 = np.sum((residuals / np.array(errY))**2) 


    # get parameters error from cov matrix
    par_error = np.zeros(len(par))
    for i in range(len(par)):
        try:
            par_error[i] = cov[i][i]**0.5
        except:
            par_error[i] = 0.00


    return par, par_error, chi2, residuals


def makePlot(X,Y,errY,par,residuals,name,choice):

    fig, ax = plt.subplots(ncols=1, nrows=2, figsize=(12,6),
                           gridspec_kw={'height_ratios': [3, 1]},
                           sharex=True)

    # plot data
    ax[0].errorbar(x=X, y=Y, yerr=errY, marker = '.',
                markersize = 15, linewidth = 0, elinewidth = 1, capsize = 1,
                color = '#0451FF', label =  name+'Data')

    # plot fit
    xmin=np.amin(X)
    xmax=np.amax(X)

    deltaX = (xmax-xmin)/10 # edit me to change plot ranges!
    xplot=np.linspace(xmin-deltaX,xmax+deltaX)

    if choice==0:
        ax[0].plot(xplot, expFunc(xplot, *par), linestyle = '--', linewidth = 2,
                   color = '#FF4B00' , label = name+'Exponential Fit')
    elif choice==1:
        ax[0].plot(xplot, linFunc(xplot, *par), linestyle = '--', linewidth = 2,
                   color = '#FF4B00' , label = name+'Linear Fit')



    # plot residuals
    ax[1].errorbar(x=X, y=residuals, yerr=errY, marker='.',
                   markersize=15, linewidth=0, elinewidth=1, capsize=1,
                   color = '#0451FF', label = name+ 'residuals')
    ax[1].plot(xplot, np.linspace(0,0), ':', linewidth=1,
               color='gray')

    # plot customiz
    plt.legend()
    ax[0].set_xlim(xmin-deltaX,xmax+deltaX)

    return fig, ax


# write fit restults on plot for exponential fit
def writeText_exp(ax,par,par_error,chi2,N,name):

    textI0 = 'I$_0$ = ' + format(par[0], '1.2f') + '$\pm$' + format(par_error[0], '1.2f')+ ' Hz'
    textMu = '$\mu$ = ' + format(par[1], '1.2f') + '$\pm$' + format(par_error[1], '1.2f')+ ' $cm^{-1}$'
    chisq = '$\chi^{2}$ / ndf = ' + format(chi2, '1.2f') + ' / ' + format(N - len(par), '1.0f')

    ax[0].text(0.70, 0.40, name+ ' exponential fit'+'\n'+textI0 + '\n' + textMu + '\n' + chisq, fontsize = 14,
            color = '#000000', transform = ax[0].transAxes)


# fixme
def writeText_lin(ax,par,par_error,chi2,N,name):

    textMu = 'mu = -m = ' + format(par[0], '1.2f') + '$\pm$' + format(par_error[0],'1.2f')+'Hz'
    textq = 'q = ' + format(par[1], '1.2f') + '$\pm$' + format(par_error[1],'1.2f')+'Hz'
    chisq = '$\chi^{2}$ / ndf = ' + format(chi2, '1.2f') + ' / ' + format(N - len(par), '1.0f')

    ax[0].text(0.70, 0.40, name+' linear fit' + '\n' + textMu + '\n'+ textq + '\n' + chisq, fontsize = 14,
            color = '#000000', transform = ax[0].transAxes)



def main(arg):

    filename=arg # contains data
    name='Cu' # appears as legend

    # read data
    data = pd.read_csv(filename, sep = '\t', header = None,
                         names = ['X','X1', 'Y', 'errY'])
    data['X'] = data['X'] * 1e-4 # um -> cm 

    # uncomment this line to obtain mu/rho [cm^2/g], instead of mu [cm^-2]
    # note: the plot will still show [cm^-1] as unit of measurment
    # note: untested, might not work

    # data['X'] = data['X1'] 

    # ==== exponential fit =====

    # fit data 
    par_exp, par_error_exp, chi2_exp, residuals_exp = fitFunc(data.X,data.Y,data.errY,0)

    # plot fit
    fig_exp, ax_exp = makePlot(data.X, data.Y, data.errY,par_exp, residuals_exp, name,0)

    # plot text
    writeText_exp(ax_exp, par_exp, par_error_exp, chi2_exp, len(data.X), name)

    fig_exp.tight_layout()


    # ==== linear fit =====

    # fit data
    par_lin, par_error_lin, chi2_lin, residuals_lin = fitFunc(data.X,data.Y,data.errY,1)

    # plot fit
    fig_lin, ax_lin = makePlot(data.X, np.log(data.Y), data.errY/data.Y,par_lin, residuals_lin, name,1)

    # plot text
    writeText_lin(ax_lin, par_lin, par_error_lin, chi2_lin, len(data.X), name)

    fig_lin.tight_layout()


    plt.show()

    return




if __name__ == "__main__":
   main(sys.argv[1])


