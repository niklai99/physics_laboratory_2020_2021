import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.interpolate import UnivariateSpline

# file names
fDistance = 'distance.txt'
fEnergy = 'energy.txt'
fCu = 'Cu.txt'
fAg = 'Ag.txt'


def lin(x, a, b):
    return a*x + b

def inv1(x, a, b):
    return a + b/x

def inv2(x, a, b, c):
    return a + b/(c + x)

def invSq(x, a, b):
    return a + b/x**2

def invCub(x, a, b):
    return a + b/x**3


# read data from file
def readData(filename):

    data = pd.read_csv(
                        filename, sep = '\t', header = None,
                        names = ['X', 'Y','errY']
                    )

    return data


# compute plot ranges
def computeRange(data, xFactor = 10, yFactor = 10):

    XMIN = np.amin(data.X)
    XMAX = np.amax(data.X)
    YMIN = np.amin(data.Y)
    YMAX = np.amax(data.Y)

    DELTAX = (XMAX - XMIN)/xFactor
    DELTAY = (YMAX - YMIN)/yFactor

    rangeX = [XMIN - DELTAX, XMAX + DELTAX]
    rangeY = [YMIN - DELTAY, YMAX + DELTAY]

    return rangeX, rangeY


def FIT(data, func):

    par, cov = curve_fit(f=func, xdata=data.X, ydata=data.Y, sigma=data.errY, absolute_sigma=True)
    
    return par, cov


# make plot
def makePlot(dataDistance, dataEnergy, dataCu, dataAg):

    # create figure and axes
    fig, ax = plt.subplots(ncols = 3,figsize = (24,9.5))
    newAx = ax[1].twinx()

    # create suptitle of the figure
    # fig.suptitle('Efficiency Curves', fontsize = 24)

    # make plots
    ax[0].errorbar(
                    dataDistance.X, dataDistance.Y, dataDistance.errY, 
                    marker = '.', markersize = 18, linewidth = 0, 
                    elinewidth = 1.5, capsize = 1.5, capthick = 1.5,
                    color = '#000000', label = 'Distance Data'
                )
    
    ax[1].errorbar(
                    dataAg.X, dataAg.Y, dataAg.errY, 
                    marker = '.', markersize = 18, linewidth = 0, 
                    elinewidth = 1.5, capsize = 1.5, capthick = 1.5,
                    color = '#0451FF', label = 'Ag Absorber'
                )

    newAx.errorbar(
                    dataCu.X, dataCu.Y, dataCu.errY, 
                    marker = '.', markersize = 18, linewidth = 0, 
                    elinewidth = 1.5, capsize = 1.5, capthick = 1.5,
                    color = '#FF4B00', label = 'Cu Absorber')


    ax[2].errorbar(
                    dataEnergy.X, dataEnergy.Y, dataEnergy.errY, 
                    marker = '.', markersize = 18, linewidth = 0, 
                    elinewidth = 1.5, capsize = 1.5, capthick = 1.5,
                    color = '#000000', label = 'Energy data'
                )


    titles = [
        'Distance',
        'Thickness',
        'Energy'
    ]

    units = [
        ' [cm]',
        ' [\u03BCm]',
        ' [keV]'
    ]


    # PLOT CONFIGURATIONS
    for i in range(len(titles)):
        # set titles
        ax[i].set_title('Efficiency over ' + titles[i], fontsize = 24)

        # set axis labels
        ax[i].set_ylabel('Efficiency \u03B5', fontsize = 18)
        ax[i].set_xlabel(titles[i] + units[i], fontsize = 18)

        # set axis ticks
        ax[i].tick_params(axis = 'both', which = 'major', labelsize = 18, direction = 'out', length = 5)
        newAx.tick_params(axis = 'both', which = 'major', labelsize = 18, direction = 'out', length = 5)

    # set yaxis parameters 
    newAx.set_ylabel('Cu Efficiency \u03B5', fontsize = 18, loc = 'center', color = '#FF4B00')
    newAx.tick_params(axis='y', labelcolor='#FF4B00')
    ax[1].set_ylabel('Ag Efficiency \u03B5', fontsize = 18, loc = 'center', color = '#0451FF')
    ax[1].tick_params(axis='y', labelcolor='#0451FF')

    # set plot ranges for distance data
    rangeX, rangeY = computeRange(dataDistance, 10, 0.3)
    ax[0].set_xlim(*rangeX)
    ax[0].set_ylim(*rangeY)

    # perform linear fit on distace data
    par, _ = FIT(dataDistance, lin)
    XFIT = np.linspace(rangeX[0], rangeX[-1], 500)
    fit = lin(XFIT, *par)
    ax[0].plot(XFIT, fit, color = '#000000', linestyle = 'dashed')

    # set plot ranges for Ag data
    XMIN = np.amin(dataAg.X)
    XMAX = np.amax(dataCu.X)
    YMIN = np.amin(dataAg.Y)
    YMAX = np.amax(dataAg.Y)
    DELTAX = (XMAX - XMIN)/15
    DELTAY = (YMAX - YMIN)/10
    rangeX = [XMIN - DELTAX, XMAX + DELTAX]
    rangeY = [YMIN - DELTAY, YMAX + DELTAY]
    ax[1].set_xlim(*rangeX)
    ax[1].set_ylim(*rangeY)
    
    # perform inverse fit on Ag data
    par, _ = FIT(dataAg, invSq)
    XFIT = np.linspace(rangeX[0], rangeX[-1], 500)
    fit = invSq(XFIT, *par)
    ax[1].plot(XFIT, fit, color = '#0451FF', linestyle = 'dashed')

    # set plot ranges for Cu data
    YMIN = np.amin(dataCu.Y)
    YMAX = np.amax(dataCu.Y)
    DELTAY = (YMAX - YMIN)/10
    rangeY = [YMIN - DELTAY, YMAX + DELTAY]
    newAx.set_ylim(*rangeY)

    # perform inverse fit on Cu data
    par, _ = FIT(dataCu, invCub)
    XFIT = np.linspace(rangeX[0], rangeX[-1], 500)
    fit = invCub(XFIT, *par)
    newAx.plot(XFIT, fit, color = '#FF4B00', linestyle = 'dashed')


    # set plot ranges for energy data
    rangeX, rangeY = computeRange(dataEnergy, 10, 10)
    ax[2].set_xlim(*rangeX)
    ax[2].set_ylim(*rangeY)

    # perform fit on energy data
    XFIT = np.linspace(rangeX[0], rangeX[-1], 500)
    spline = UnivariateSpline(dataEnergy.X, dataEnergy.Y, w=1/dataEnergy.errY**2, k = 1, s = 0)
    ax[2].plot(XFIT, spline(XFIT), color = '#000000', linestyle = 'dashed')


    # set legend
    h1, l1 = ax[1].get_legend_handles_labels()
    h2, l2 = newAx.get_legend_handles_labels()
    ax[1].legend(h1+h2, l1+l2, loc='best', prop={'size':18})


    return fig, ax



def main():

    # get dataframes
    dataDistance = readData(fDistance)
    dataEnergy = readData(fEnergy)
    dataCu = readData(fCu)
    dataAg = readData(fAg)


    fig, ax = makePlot(dataDistance, dataEnergy, dataCu, dataAg)
    
    fig.tight_layout()

    # save figure
    # fig.savefig('../Plots/efficiency.png', dpi = 300, facecolor = 'white')
    plt.show()

    return




if __name__ == "__main__":
    main()