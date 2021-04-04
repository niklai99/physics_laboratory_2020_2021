import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.signal import find_peaks
from scipy.optimize import curve_fit

# constants
npixels=7926
maxcolumns=1024
LAMBDA = 585.3 # nanometers
d = 4.04 * 1e6 #nanometers (4.04 millimiters)
dataPath = '../Data/'

start = 2020
end = 5640


# read data from txt file
def readData():

    data = pd.read_csv(dataPath + 'off.txt', sep = '\t', header = None, names = ['X', 'Y'])

    return data


def findPeaks(newData):

    peaks, p = find_peaks(newData['Y'], width=5, prominence=100, rel_height=0.5)

    fig, ax = plt.subplots(figsize=(12,6))
    fig.tight_layout()

    ax.set_xlim(start, end)
    ax.set_ylim(0, np.amax(newData['Y']) * ( 1 + 5/100 ))


    # plot data
    ax.hist(newData['X'], bins = len(newData['X']), weights = newData['Y'], histtype = 'step', color = '#0451FF')
    # plot peaks
    ax.plot(newData['X'].iloc[peaks], newData['Y'].iloc[peaks], '.', color='red')


    xHalfLeft = []
    xHalfRight = []
    xPlotLeft = []
    xPlotRight = []
    FWHM = []
    Peaks = []

    # loop over peaks
    for i in range(len(peaks)):

        # get peak start
        xl = newData['X'].iloc[round(p['left_ips'][i])]
        xHalfLeft.append(xl)
        # get peak end
        xr = newData['X'].iloc[round(p['right_ips'][i])]
        xHalfRight.append(xr)

        y = p['width_heights'][i]
        
        FWHM.append(xr-xl)

        xm = newData['X'].iloc[peaks[i]]
        Peaks.append(xm)

        d1 = xm - xl
        d2 = xr - xm

        xPlotLeft.append(xm - 5*d1)
        xPlotRight.append(xm + 5*d2)

        # plot limits for current peak
        ax.vlines(x=xl, ymin=0, ymax = np.amax(newData['Y']) * ( 1 + 5/100 ), color = "blue", alpha = 0.3)
        ax.vlines(x=xr, ymin=0, ymax = np.amax(newData['Y']) * ( 1 + 5/100 ), color = "blue", alpha = 0.3)
        ax.hlines(y=y, xmin=xl, xmax=xr, color = "C1", alpha = 0.3)

        # ax.vlines(x=xm - 2*d1, ymin=0, ymax = np.amax(newData['Y']) * ( 1 + 5/100 ), color = "red", alpha = 0.3)
        # ax.vlines(x=xm + 2*d2, ymin=0, ymax = np.amax(newData['Y']) * ( 1 + 5/100 ), color = "red", alpha = 0.3)

        # ax.vlines(x=xm - 5*d1, ymin=0, ymax = np.amax(newData['Y']) * ( 1 + 5/100 ), color = "green", alpha = 0.3)
        # ax.vlines(x=xm + 5*d2, ymin=0, ymax = np.amax(newData['Y']) * ( 1 + 5/100 ), color = "green", alpha = 0.3)


    return Peaks, FWHM, xHalfLeft, xHalfRight, xPlotLeft, xPlotRight


def computeSpacing(Peaks):

    C = []
    Spacing = []

    for i in range(1, len(Peaks)):
        C.append(Peaks[i] - Peaks[i-1])

    for i in range(1, len(C)):
        Spacing.append((C[i] + C[i-1]) / 2)

    return Spacing


# plot 16 triplets of peeks
# probably useless
def plot3peaks(newData, xPlotLeft, xPlotRight):

    slices = []
    for i in range(0, len(xPlotLeft) - 2, 3):
        s = newData[(newData['X'] >= xPlotLeft[i]) & (newData['X'] <= xPlotRight[i+2])]
        slices.append(s)

    # create figure and axes array
    fig, ax = plt.subplots(nrows=4, ncols=4, figsize=(12,6), squeeze=False)
    fig.tight_layout()

    h = 0
    # iteration over rows
    for j in range(4):
        # iteration over columns
        for i in range(4):
            # set plot range for axes
            ax[j][i].set_xlim(slices[i+h]['X'].iloc[0], slices[i+h]['X'].iloc[-1])
            ax[j][i].set_ylim(0, np.amax(slices[i+h]['Y']) * (1 + 5/100))
            # plot the histogram in each axe
            ax[j][i].hist(slices[i+h]['X'], bins = len(slices[i+h]['Y']), weights = slices[i+h]['Y'], histtype = 'step', color = '#0451FF')
        h += 4

    return


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

    data = readData()

    newData = data.loc[start:end]
    newData.reset_index(inplace = True, drop = True)

    Peaks, FWHM, xHalfLeft, xHalfRight, xPlotLeft, xPlotRight = findPeaks(newData)

    Spacing = computeSpacing(Peaks)


    plot3peaks(newData, xPlotLeft, xPlotRight)
    spacingTrend(Peaks[1:-1], Spacing, FWHM[1:-1])


    # ------ RESOLVING POWER
    # compute deltaLambda(r.u.)
    dLru = computeDeltaLru()

    # compute deltaLambda for each set of peaks
    dL = computeDeltaLambda(Spacing, dLru, FWHM[1:-1])

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
    print('- Average Peak spacing: ' + format(np.average(Spacing), '1.0f') + ' pixels')
    print('- Average FWHF central Peak: ' + format(np.average(FWHM), '1.0f') + ' pixels')
    print('- Average \u0394\u03BB: ' + format(np.average(dL), '1.3f') + ' nanometers')
    print('- Average Resolving Power R: ' + format(avgR, '1.0f') + ' +/- ' + format(avgR_e, '1.0f'))
    print('- Resolving Power precision: ' + format(100 * avgR_e/avgR, '1.2f') + '%') 
    print('\n')


    plt.show()

    return




if __name__ == "__main__":
    main()