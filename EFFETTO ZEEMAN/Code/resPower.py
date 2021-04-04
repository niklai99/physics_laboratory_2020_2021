# Script to identify and fit interference peaks stored in a txt file.
# In addition, some data analysis is automatically computed
#
# USAGE: python resPower.py plotdata.txt
#  where "plotdata.txt" contains the y-projection of the 2d-histogram
#  that is obtained from a ".zee" binary file using the script zeemanPlot.py
#  If the program crashes, change the number of bins or the parameters used
#  when calling ~find_peaks~
#

import sys
import numpy as np
import matplotlib.pyplot as plt
from math import pi
import pandas as pd
from scipy.signal import find_peaks
from scipy.optimize import curve_fit
from scipy.interpolate import UnivariateSpline

# constants
npixels=7926
maxcolumns=1024
LAMBDA = 585.3 # nanometers
d = 4.04 * 1e6 #nanometers (4.04 millimiters)
dataPath = '../Data/'

start = 4000
end = 7000

binFrac=4 # nBins_new = nBins_old / binFrac

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
    # print("Number of bins: ", len(newX))
    # count =0
    # for i in range(len(newY)):
    #     count+=newY[i]
    # print("Counts", count) # note: this is different than root

    return data


# fitting function
def Gauss(x, N, x0, sigma):
    return N/(2*pi)**0.5 / sigma * np.exp(-(x - x0)**2 / (2 * sigma**2))


def findPeaks(newData):

    # use scipy signal to identify peaks
    #peaks, p = find_peaks(newData['Y'], width=20, prominence=200, rel_height=0.5)
    peaks, p = find_peaks(newData['Y'], width = 6,prominence=50, rel_height=0.5)
    print("Found", len(peaks), "peaks")

    fig, ax = plt.subplots(figsize=(12,6))
    fig.tight_layout()

    ax.set_xlim(start, end)
    ax.set_ylim(0, np.amax(newData['Y']) * ( 1 + 5/100 ))


    # plot data
    ax.hist(newData['X'], bins = int(len(newData['X'])), weights = newData['Y'], histtype = 'step', color = '#0451FF')
    # plot peaks
    # ax.plot(newData['X'].iloc[peaks], newData['Y'].iloc[peaks], '.', color='red')


    xHalfLeft = []
    xHalfRight = []
    xPlotLeft = []
    xPlotRight = []
    FWHM = []
    Peaks = []
    parFit=[]

    # ATTENTION ===============
    # While technically all peaks are caused by Zeeman splitting, we need to distinguish the 
    # distance between the Zeeman splitting and the interfererence splitting. 
    # Therefore, we adopt the convention of naming the left Zeeman peak "interference peak"
    # while the right peak will be referred to as "Zeeman peak". 
    # All peaks will be stored inside the lists ~Peaks~ and ~parFit~, as we did in Boff.
    # We then implement two new lists to keep track of the interference peaks' indexes (~intP~)
    # and the Zeeman peaks' indexes (~zeeP~).
    # The actual position of the interference peak can be computed as average of the zeeman peaks, 
    # if needed.
    intP=[]
    zeeP=[]

    # loop over peaks
    isLastZeeman=True # true if last peak is a Zeeman peak => next peak will be a interference peak
    for i in range(len(peaks)):

        # get fit data
        trL=+int((p['right_ips'][i] - p['left_ips'][i])/2)
        trR=-int((p['right_ips'][i] - p['left_ips'][i])/5)
        trR=trL
        xfit=newData['X'].iloc[round(p['left_ips'][i]-trL):round(p['right_ips'][i])+trR]
        #yfit=newData['Y'].iloc[round(p['left_ips'][i]-trL):round(p['right_ips'][i])+trR]
        yfit=newData['Y'].iloc[round(p['left_ips'][i]-trL):round(p['right_ips'][i])+trR]

        # initial parameters
        mean0=np.average(xfit)
        std0=np.std(xfit)

        # normalization parameter
        ngau=np.sum(yfit* binFrac)

        # fit current peak
        par, std = curve_fit(lambda x,mean,stddev: Gauss(x,ngau,mean,stddev),
                             xfit, yfit,
                             p0=[mean0, std0])


        halfMax = Gauss(par[0],ngau,*par) /2

        # compute halfMax pixels
        spline = UnivariateSpline(xfit, Gauss(xfit,ngau,*par) - halfMax , s = 0)
        r1, r2 = spline.roots() # find the roots
        #r1=np.amin(xfit)
        #r2=np.amax(xfit)

        #ax.vlines(x=r1, ymin=0, ymax = np.amax(newData['Y']) * ( 1 + 5/100 ), color = "blue", alpha = 0.3)
        #ax.vlines(x=r2, ymin=0, ymax = np.amax(newData['Y']) * ( 1 + 5/100 ), color = "blue", alpha = 0.3)

        FWHM.append(r2-r1)
        Peaks.append(par[0])
        xHalfLeft.append(r1)
        xHalfRight.append(r2)
        xPlotLeft.append(par[0] - 5*(r2-r1))
        xPlotRight.append(par[0] + 5*(r2-r1))

        # chi2
        diff = yfit-Gauss(xfit,ngau,*par)
        chisq = np.sum(diff**2)/(len(xfit)-2)
        #print("chisq",i, round(abs(chisq-(len(xfit-2)))/ (len(xfit)-2)**0.5 / 2**0.5,2)) # TODO: ricontrollami

       # plot fit
        #xth = np.linspace(np.amin(xfit),np.amax(xfit), 100)
        xth = np.linspace(xPlotLeft[-1],xPlotRight[-1], 100)
        yth = Gauss(xth,ngau,*par)


        # plot gaussian fit
        if isLastZeeman:
            ax.plot(xth, yth, color='green')
        else:
            ax.plot(xth, yth, color='red')

        # save parameters
        parFit.append([ngau, par[0], par[1]])

        if isLastZeeman:
            # this is an interference peak
            intP.append(i)
            isLastZeeman=False
        else:
            # this is a Zeeman peak
            zeeP.append(i)
            isLastZeeman=True

    return Peaks, FWHM, xHalfLeft, xHalfRight, xPlotLeft, xPlotRight, parFit, intP, zeeP


def computeSpacing(Peaks, intP, zeeP):

    C = [] # store distance between interference peaks
    zee_dist = [] # store distance between zeeman peaks
    Spacing = [] # average between previous and next (interference) peaks

    for i in range(1, len(Peaks)):
        # compute distance only between interference peaks
        if i in intP[:]:
            # compute average between 2 zeeman peaks
            avgCurrent=(Peaks[i]+Peaks[i+1])/2
            avgPrevious=(Peaks[i-2]+Peaks[i-1])/2
            # store distance
            C.append(avgCurrent -avgPrevious)

        # compute distance only between zeeman peaks
        if i in zeeP[:]:
            # compute distance between 2 zeeman peaks
            d=Peaks[i]-Peaks[i-1]
            # store distance
            zee_dist.append(d)


    # FIXME: are we counting the same distance multiple times?
    # can't we just take the average of C? 
    for i in range(1, len(C)):
        Spacing.append((C[i] + C[i-1]) / 2)

    # Possible fix: 
    avgSpacing = np.average(C) # average interference distance
    avgSpacingZee = np.average(zee_dist) # average zeeman distance

    return avgSpacing, avgSpacingZee


def main(fname):

    # read data from file
    data = readData(fname)

    # select data based on requested X range
    newData = data[(data['X']>start) & (data['X']<end)]
    newData.reset_index(inplace = True, drop = True)

    # find peaks
    Peaks, FWHM, xHalfLeft, xHalfRight, xPlotLeft, xPlotRight, parFit, intP, zeeP= findPeaks(newData)

    # compute spacing between peaks
    Spacing, Spacing_zee = computeSpacing(Peaks, intP, zeeP)

    plt.show()

    return




if __name__ == "__main__":
    main(sys.argv[1])
