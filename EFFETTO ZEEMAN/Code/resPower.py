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

# starting/ending points of each peak:
# each sub-list represents a 3-peaks set
# example: 
# [1st peak starts, 1st peak ends/2nd peak start, 2nd peak ends/3rd peak starts, 3rd peak ends]
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

    data = pd.read_csv(dataPath + 'off.txt', sep = '\t', header = None, names = ['X', 'Y'])

    return data


# (almost) automated plotting 
def plot3peaks(slices):

    n = len(slices)

    # if the list has less than 3 elemnts we plot a single row of plots
    if n <= 3:

        # create figure and axes array
        fig, ax = plt.subplots(ncols=n, figsize=(12,6), squeeze=False)

        # iteration over columns
        for i in range(n):
            # set plot range for axes
            ax[0][i].set_xlim(slices[i]['X'].iloc[0], slices[i]['X'].iloc[-1])
            ax[0][i].set_ylim(0, np.amax(slices[i]['Y']) * (1 + 5/100))
            # plot the histogram in each axe
            ax[0][i].hist(slices[i]['X'], bins = len(slices[i]['Y']), weights = slices[i]['Y'], histtype = 'step', color = '#0451FF')



    # if the list has 4 or more elements we need two rows of plots (even case) (please no odd lengths haha lol)
    elif (n > 3) & (n%2 == 0):

        # create figure and axes array
        fig, ax = plt.subplots(nrows=int(np.sqrt(n)), ncols=int(np.sqrt(n)), figsize=(12,6), squeeze=False)

        h = 0
        # iteration over rows
        for j in range(int(np.sqrt(n))):
            # iteration over columns
            for i in range(int(np.sqrt(n))):
                # set plot range for axes
                ax[j][i].set_xlim(slices[i+h]['X'].iloc[0], slices[i+h]['X'].iloc[-1])
                ax[j][i].set_ylim(0, np.amax(slices[i+h]['Y']) * (1 + 5/100))
                # plot the histogram in each axe
                ax[j][i].hist(slices[i+h]['X'], bins = len(slices[i+h]['Y']), weights = slices[i+h]['Y'], histtype = 'step', color = '#0451FF')
            h += int(np.sqrt(n))


    fig.tight_layout()
    
    return



def computeSpacingFWHM(df, p):

    peaks = []
    maxs = []
    halfMaxs = []

    # iteration over each peak
    for i in range(3):

        # isolate each peak
        # now peaks is a list of (three) dataframes, each dataframe containing data about a single peak
        peaks.append(df.loc[p[i]:p[i+1]])

        # we want now to find the maximum value, in other words, the height of the peak
        # now maxs is a list of (three) dataframes, each dataframe containing X and Y of the single peak
        maxs.append(peaks[i][ peaks[i]['Y'] == np.amax(peaks[i]['Y']) ])

        # we want to compute the half-maximum
        halfMaxs.append(maxs[i].copy())
        halfMaxs[i]['Y'] = halfMaxs[i]['Y']/2

        # now we want to compute the X values corresponding to half-max values
        halfValue = halfMaxs[i]['Y'].iloc[0]
        maxIndex = int(maxs[i]['X'].iloc[0])
        halfMaxs[i]['X1'] = (   np.abs(   peaks[i]['Y'].loc[:maxIndex] - halfValue   )   ).argmin() + p[i]
        halfMaxs[i]['X2'] = (   np.abs(   peaks[i]['Y'].loc[maxIndex:] - halfValue   )   ).argmin() + maxIndex


    # now we want to compute the average distance between peaks
    C1 = maxs[1]['X'].iloc[0] - maxs[0]['X'].iloc[0]
    C2 = maxs[2]['X'].iloc[0] - maxs[1]['X'].iloc[0]
    deltaXru = (C1 + C2) / 2

    # finally compute FWHM of the central peak
    FWHM = (halfMaxs[1]['X2'] - halfMaxs[1]['X1']).iloc[0]
    
    # we also want to return the position of central peak max
    maxPosition = int(maxs[1]['X'].iloc[0])

    
    # the following plots are test plots to see whether things are working or not

    # fig, ax = plt.subplots(ncols=1)
    # fig.tight_layout()
    # ax.hist(df['X'], bins = len(df['X']), weights =df['Y'], histtype = 'step', color = '#0451FF')

    # fig, ax = plt.subplots(ncols=3)
    # fig.tight_layout()
    # for i in range(3):
    #     ax[i].hist(peaks[i]['X'], bins = len(peaks[i]['X']), weights = peaks[i]['Y'], histtype = 'step', color = '#0451FF')
    

    return maxPosition, deltaXru, FWHM


def computeDeltaLru():

    # approximate formula
    dLru = LAMBDA**2 / (2*d) # nanometers

    return dLru


def computeDeltaLambda(dXru, dLru, FWHM):

    dL = (np.array(FWHM) * dLru) / np.array(dXru) # nanometers

    return dL


def computeResolvingPower(dL):

    R = LAMBDA / np.array(dL)

    return R


def computeRMS(R, avgR):

    MSE = np.sum( (np.array(R) - avgR)**2 ) / (len(R) - 1)
    RMSE = np.sqrt(MSE)

    return RMSE


# ABERRATION ANALYSIS 
def spacingTrend(peakPositions, peakSpacing, peakFWHM):

    # create figure
    fig = plt.figure(figsize=(12,6))

    # create axes
    ax1 = fig.add_subplot(1, 2, 1)
    ax2 = fig.add_subplot(1, 2, 2)

    # show plots
    ax1.plot(peakPositions, peakSpacing, marker = '.', markersize = 15, linewidth = 1, color = '#0451FF')
    ax2.plot(peakPositions, peakFWHM, marker = '.', markersize = 15, linewidth = 1, color = '#0451FF')

    # titles
    ax1.set_title('Peak spacing over Position')
    ax2.set_title('FWHM over Position')

    # labels
    ax1.set_xlabel('Peak position [# pixel]')
    ax2.set_xlabel('Peak position [# pixel]')
    ax1.set_ylabel('Peak spacing [# pixel]')
    ax2.set_ylabel('FWHM [# pixel]')

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

    # lists to hold positions, spacings and FWHMs
    peakPositions = []
    peakSpacing = []
    peakFWHM = []

    # iteration over each slice 
    for i in range(len(p)):

        # call the computeSpacingFWHM function
        # here we pass every slice we have
        # if needed, it is possibile to use less slices (one or three) for approximate analysis
        maxPosition, dXru, FWHM = computeSpacingFWHM(slices[i], p[i])

        # append stuff
        peakPositions.append(maxPosition)
        peakSpacing.append(dXru)
        peakFWHM.append(FWHM)


    # ------ PLOTS
    # plot all sets of peaks
    plot3peaks(slices)

    # plot trends
    spacingTrend(peakPositions, peakSpacing, peakFWHM)
    # ------ 

    # ------ RESOLVING POWER
    # compute deltaLambda(r.u.)
    dLru = computeDeltaLru()

    # compute deltaLambda for each set of peaks
    dL = computeDeltaLambda(peakSpacing, dLru, peakFWHM)

    # compute the resolving power for each set of peaks and the average of the three
    R = computeResolvingPower(dL)
    avgR = np.average(R)
    R_e = computeRMS(R, avgR)
    avgR_e = R_e / np.sqrt(len(R))
    # ------

    # ------ PRINTING
    # print relevant results
    print('\n')
    print('- \u03BB: ' + format(LAMBDA, '1.1f') + ' nanometers')
    print('- \u0394\u03BB (r.u.): ' + format(dLru, '1.3f') + ' nanometers')
    print('- Average Peak spacing: ' + format(np.average(peakSpacing), '1.0f') + ' pixels')
    print('- Average FWHF central Peak: ' + format(np.average(FWHM), '1.0f') + ' pixels')
    print('- Average \u0394\u03BB: ' + format(np.average(dL), '1.3f') + ' nanometers')
    print('- Average Resolving Power R: ' + format(avgR, '1.0f') + ' +/- ' + format(avgR_e, '1.0f'))
    print('- Resolving Power precision: ' + format(100 * avgR_e/avgR, '1.2f') + '%') 
    print('\n')

    

    plt.show()

    return
    
 



if __name__ == "__main__":
    main()
