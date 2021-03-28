#!/usr/bin/python
#%config InlineBackend.figure_format = 'png'

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.optimize import curve_fit

# constants
npixels=7926
maxcolumns=1024
LAMBDA = 585.3 # nanometers
d = 4.04 * 1e6 #nanometers (4.04 millimiters)
dataPath = '../Data/'


p = [
        [1950, 2050, 2160, 2260],
        [2260, 2360, 2460, 2560],
        [2560, 2660, 2750, 2850],
        [2850, 2930, 3020, 3110],
        [3110, 3190, 3270, 3360],
        [3360, 3440, 3520, 3600],
        [3600, 3675, 3750, 3825],
        [3825, 3900, 3975, 4050],
        [4050, 4120, 4190, 4260],
        [4260, 4330, 4400, 4465],
        [4465, 4530, 4600, 4665],
        [4665, 4730, 4795, 4860],
        [4860, 4925, 4990, 5050],
        [5050, 5110, 5170, 5230],
        [5230, 5290, 5350, 5410],
        [5410, 5470, 5530, 5590]
    ]



# read data from txt file
def readData():

    data = pd.read_csv(dataPath + 'testData.txt', sep = '\t', header = None, names = ['X', 'Y'])

    return data


# gauss funcction
def gaussian(x, scale, mean, sigma):

    gauss = scale * np.exp( -(x-mean)**2 / (2*sigma**2) )

    return gauss


def gaus_fit(X, Y):
    par, cov = curve_fit(f = gaussian, xdata = X, ydata = Y, p0 = [1, 3700, 20])
    return par, cov


def isolatePeaks(df, p):
    peaks = []
    # fig, ax = plt.subplots(ncols=3, figsize=(12,6))
    for i in range(3):

        # isolate each peak
        # now peaks is a list of (three) dataframes, each dataframe containing data about a single peak
        peaks.append(df.loc[p[i]+27:p[i+1]-27])

        # plot to see if peak isolation worked correctly
        #ax[i].hist(peaks[i]['X'], bins = len(peaks[i]['Y']), weights = peaks[i]['Y'], histtype = 'step', color = '#0451FF')
    
    return peaks


def plot3peaks(slices, p):

    n = len(slices)

    peaks = isolatePeaks(slices[0], p[0])
    par, cov = gaus_fit(peaks[1]['X'], peaks[1]['Y'])

    # create figure and axes array
    fig, ax = plt.subplots(ncols=n, figsize=(12,6), squeeze=False)

    # iteration over columns
    for i in range(n):
        # set plot range for axes
        ax[0][i].set_xlim(slices[i]['X'].iloc[0], slices[i]['X'].iloc[-1])
        ax[0][i].set_ylim(0, np.amax(slices[i]['Y']) * (1 + 5/100))
        # plot the histogram in each axe
        ax[0][i].hist(slices[i]['X'], bins = len(slices[i]['Y']), weights = slices[i]['Y'], histtype = 'step', color = '#0451FF')
        # ax[0][i].plot(peaks[1]['X'], peaks[1]['Y'], linewidth=2, color = '#ff3504')
        ax[0][i].plot(peaks[1]['X'], gaussian(peaks[1]['X'], *par), linewidth=2, color = '#04ff35')


    fig.tight_layout()
    
    return




def main():

    # read data from txt file
    data = readData()

    # from peak-set-delimiters get X and Y data
    # we basically isolate the 3 peaks sets 
    # slices constains portions of dataframe that concern the corresponding set of peaks
    slices = []
    for i in range(len(p)):
        s = data[(data['X'] >= p[i][0]) & (data['X'] <= p[i][-1])]
        slices.append(s)

 
    # ------ PLOTS
    # plot all sets of peaks
    plot3peaks([slices[6]], [p[6]])




    plt.show()
    return


if __name__ == "__main__":
    main()
