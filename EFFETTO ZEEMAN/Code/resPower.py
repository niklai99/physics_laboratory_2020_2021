# Script to identify and fit interference peaks stored in a txt file.
# In addition, some data analysis is automatically computed
#
# USAGE: python resPower.py plotdata.txt
#  where "plotdata.txt" contains the y-projection of the 2d-histogram
#  that is obtained from a ".zee" binary file using the script zeemanPlot.py
#

import sys
import numpy as np
import matplotlib.pyplot as plt
from math import pi
import pandas as pd
from scipy.signal import find_peaks
from scipy.optimize import curve_fit

# constants
npixels=7926
maxcolumns=1024
LAMBDA = 585.3 # nanometers
d = 4.04 * 1e6 #nanometers (4.04 millimiters)
dataPath = '../Data/'

start = 1400
end = 8000

binFrac=3 # nBins_new = nBins_old / binFrac

# read data from txt file
def readData(fname):

    # read raw data
    data = pd.read_csv(dataPath + fname, sep = '\t', header = None, names = ['X', 'Y'])

    # change bins and get new y
    newY, edge= np.histogram(data.X, weights=data.Y, bins=int(len(data.X)/binFrac))

    # get new x
    newX = []
    for i in range(len(edge)-1):
        newX.append((edge[i]+edge[i+1])/2)

    # save new data in a Pandassssss dataframe
    data = pd.DataFrame(list(zip(newX,newY)), columns=['X','Y'])
    #plt.hist(newData['X'], bins = int(len(newData['X'])), weights = newData['Y'], histtype = 'step', color = '#0451FF')
    print("Number of bins: ", len(newX))
    count =0
    for i in range(len(newY)):
        count+=newY[i]
    print("Counts", count) # note: this is different than root

    return data


# fitting function
def Gauss(x, N, x0, sigma):
    return N/(2*pi)**0.5 / sigma * np.exp(-(x - x0)**2 / (2 * sigma**2))


def findPeaks(newData):

    # use scipy signal to identify peaks
    peaks, p = find_peaks(newData['Y'], width=5, prominence=100, rel_height=0.5)
    print("Found", len(peaks), "peaks")

    fig, ax = plt.subplots(figsize=(12,6))
    fig.tight_layout()

    ax.set_xlim(start, end)
    ax.set_ylim(0, np.amax(newData['Y']) * ( 1 + 5/100 ))


    # plot data
    ax.hist(newData['X'], bins = int(len(newData['X'])), weights = newData['Y'], histtype = 'step', color = '#0451FF')
    # plot peaks
    ax.plot(newData['X'].iloc[peaks], newData['Y'].iloc[peaks], '.', color='red')


    xHalfLeft = []
    xHalfRight = []
    xPlotLeft = []
    xPlotRight = []
    FWHM = []
    Peaks = []
    parFit=[]

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

        # fit current peak
        tr=int((p['right_ips'][i] - p['left_ips'][i])/5)
        xfit=newData['X'].iloc[round(p['left_ips'][i]-tr):round(p['right_ips'][i])+tr]
        yfit=newData['Y'].iloc[round(p['left_ips'][i]-tr):round(p['right_ips'][i])+tr]
        mean0=np.average(xfit)
        std0=np.std(xfit)
        ngau=np.sum(yfit* binFrac)
        par, std = curve_fit(lambda x,mean,stddev: Gauss(x,ngau,mean,stddev),
                             xfit, yfit,
                             p0=[mean0, std0])

        # plot fit
        xth = np.linspace(np.amin(xfit), np.amax(xfit))
        yth = Gauss(xth,ngau,*par)
        diff = yfit-Gauss(xfit,ngau,*par)
        chisq = np.sum(diff**2)/(len(xfit)-2)

        #print("chisq",i, round(abs(chisq-(len(xfit-2)))/ (len(xfit)-2)**0.5 / 2**0.5,2)) # TODO: ricontrollami
        ax.plot(xth, yth,color='black')

        parFit.append([ngau, par[0], par[1]])

    return Peaks, FWHM, xHalfLeft, xHalfRight, xPlotLeft, xPlotRight, parFit


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
def plot3peaks(newData, xPlotLeft, xPlotRight, parFit):

    slices = []
    for i in range(0, len(xPlotLeft) - 2, 3):
        s = newData[(newData['X'] >= xPlotLeft[i]) & (newData['X'] <= xPlotRight[i+2])]
        slices.append(s)

    # create figure and axes array
    fig, ax = plt.subplots(nrows=2, ncols=3, figsize=(12,6), squeeze=False)
    fig.tight_layout()

    h = 0
    count =0
    # iteration over rows
    for j in range(2):
        # iteration over columns
        for i in range(3):

            # check if there are enough peaks
            if(i+h < len(slices)):

                # plot peaks
                ax[j][i].set_xlim(slices[i+h]['X'].iloc[0], slices[i+h]['X'].iloc[-1])
                ax[j][i].set_ylim(0, np.amax(slices[i+h]['Y']) * (1 + 5/100))
                ax[j][i].hist(slices[i+h]['X'], bins = int(len(slices[i+h]['Y'])), weights = slices[i+h]['Y'], histtype = 'step', color = '#0451FF')

                # plot fits
                for k in range(3):
                    xfit=np.linspace(slices[i+h]['X'].iloc[0],slices[i+h]['X'].iloc[-1])
                    yfit=Gauss(xfit, *parFit[count])
                    ax[j][i].plot(xfit,yfit,'--', color='black')
                    count+=1

            else: break

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



def main(fname):

    # read data from file
    data = readData(fname)

    # select data based on requested X range
    newData = data[data['X']>start][data['X']<end]
    newData.reset_index(inplace = True, drop = True)

    # find peaks
    Peaks, FWHM, xHalfLeft, xHalfRight, xPlotLeft, xPlotRight, parFit = findPeaks(newData)
    Spacing = computeSpacing(Peaks)


    # plot peaks
    plot3peaks(newData, xPlotLeft, xPlotRight, parFit)
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
    main(sys.argv[1])
