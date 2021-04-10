import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

filename = 'distanceData.txt'


def invSquare(x, x0, a, b):
    return a + b / (x + x0)**2


def fitFunc(X, Y, errY):

    par, cov = curve_fit(
                            f=invSquare, xdata=X, ydata=Y,
                            sigma=errY, absolute_sigma=True,
                            p0=[1, 100, 100]
                        )

    residuals = np.array(Y) - invSquare(np.array(X), *par)
    chi2 = np.sum((residuals / np.array(errY))**2)

    # get parameters error from cov matrix
    par_error = np.zeros(len(par))

    for i in range(len(par)):
        try:
            par_error[i] = cov[i][i]**0.5
        except:
            par_error[i] = 0.00

    return par, par_error, chi2, residuals


def drawPlot(X, Y, errY, par, residuals):

    XMIN = np.amin(X)
    XMAX = np.amax(X)
    DELTA = (XMAX - XMIN)/10
    XPLOT = np.linspace(XMIN-DELTA, XMAX+DELTA)

    fig, ax = plt.subplots(ncols=1, nrows=2, figsize=(12,6),
                           gridspec_kw={'height_ratios': [3, 1]},
                           sharex=True)

    ax[0].errorbar(x=X, y=Y, yerr=errY, marker = '.',
                markersize = 18, linewidth = 0, 
                elinewidth = 1.5, capsize = 1.5, capthick = 1.5,
                color = '#0451FF', label = 'Data')

    ax[0].plot(XPLOT, invSquare(XPLOT, *par), linestyle = '--', linewidth = 2, color = '#FF4B00' , label = 'Fit')


    ax[1].errorbar(x=X, y=residuals, yerr=errY, marker = '.',
                markersize = 18, linewidth = 0, 
                elinewidth = 1.5, capsize = 1.5, capthick = 1.5,
                color = '#0451FF', label = 'Data')

    ax[1].hlines(0, XMIN-DELTA, XMAX+DELTA, color = '#000000', linestyle = 'dashed', linewidth = 1)

    # plot title
    ax[0].set_title('Event Rate over Absorber Distance', fontsize = 24)

    # plot ranges
    ax[0].set_xlim(XMIN-DELTA, XMAX+DELTA)
    ax[0].set_ylim(0, 500)

    # plot labels
    # ax[0].set_xlabel('Distance [cm]', fontsize = 20)
    ax[0].set_ylabel('Rate [Hz]', fontsize = 20, loc = 'center')
    ax[1].set_xlabel('Distance [cm]', fontsize = 20)
    ax[1].set_ylabel('Residuals [Hz]', fontsize = 20, loc = 'center')

    # plot ticks
    ax[0].tick_params(axis = 'both', which = 'major', labelsize = 16, direction = 'out', length = 5)
    ax[1].tick_params(axis = 'both', which = 'major', labelsize = 16, direction = 'out', length = 5)


    return fig, ax



def drawText(ax, par, par_error, chi2, N):

    
    textX0 = 'x$_0$ = ' + format(par[0], '1.2f') + ' +/- ' + format(par_error[0], '1.2f') + ' cm'
    textScale = 'offset = ' + format(par[1], '1.1f') + ' +/- ' + format(par_error[1], '1.1f') + ' Hz'
    textOffset = 'scale = ' + format(par[2], '1.0f') + ' +/- ' + format(par_error[2], '1.0f') + ' Hz cm$^2$'
    chisqAg = '$\chi^{2}$ / ndf = ' + format(chi2, '1.1f') + ' / ' + format(N - len(par), '1.0f')

    ax[0].text(4.2, 440, 'Fit Function', fontsize = 22, fontweight = 'bold', transform=ax[0].transData)
    ax[0].text(4.3, 400, 'y = offset + scale (x + x$_0$)$^{-2}$', fontsize = 18, color = '#000000', transform = ax[0].transData)
    ax[0].text(4.2, 330, 'Fit Parameters', fontsize = 22, fontweight = 'bold', transform=ax[0].transData)
    ax[0].text(4.3, 140, textX0 + '\n' + textScale + '\n' + textOffset + '\n' + chisqAg, fontsize = 18, color = '#000000', transform = ax[0].transData)

    return



def main():

    # read data
    data = pd.read_csv(
                        filename, sep = '\t', header = None,
                        names = ['Dist','Counts', 'Rate', 'errRate']
                    )

    

    par, par_error, chi2, residuals = fitFunc(data.Dist, data.Rate, data.errRate)

    fig, ax = drawPlot(data.Dist, data.Rate, data.errRate, par, residuals)
    
    drawText(ax, par, par_error, chi2, len(data.Dist))

    fig.tight_layout()
    # fig.savefig('../Plots/distance_small.png', dpi = 300, facecolor = 'white')
    plt.show()

    return




if __name__ == "__main__":
   main()