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
h = 6.626 *1e-34
c = 299792458
muB = 9.274 * 1e-24
mj = 1
B = 0.522 #tesla
errB = B * 1/100
LAMBDA = 585.3 # nanometers
d = 4.04 * 1e6 #nanometers (4.04 millimiters)
dataPath = '../Data/'

start = 4260
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


def findPeaks(newData):

    # use scipy signal to identify peaks
    #peaks, p = find_peaks(newData['Y'], width=20, prominence=200, rel_height=0.5)
    Peaks, p = find_peaks(newData['Y'], width = 6,prominence=50, rel_height=0.5)
    print("Found", len(Peaks), "peaks")

    fig, ax = plt.subplots(figsize=(12,6))
    fig.tight_layout()

    ax.set_xlim(start, end)
    ax.set_ylim(0, np.amax(newData['Y']) * ( 1 + 5/100 ))


    # plot data
    ax.hist(newData['X'], bins = int(len(newData['X'])), weights = newData['Y'], histtype = 'step', color = '#0451FF')
    # plot peaks
    # ax.plot(newData['X'].iloc[peaks], newData['Y'].iloc[peaks], '.', color='red')


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
    for i in range(len(Peaks)):

        if isLastZeeman:
            # this is an interference peak
            intP.append(i)
            isLastZeeman=False
        else:
            # this is a Zeeman peak
            zeeP.append(i)
            isLastZeeman=True

    return Peaks, intP, zeeP


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

    for i in range(1, len(C)):
        Spacing.append((C[i] + C[i-1]) / 2)


    return Spacing, zee_dist



def computeDeltaLru():

    # approximate formula
    dLru = LAMBDA**2 / (2*d) # nanometers

    return dLru


def computeDeltaLambda(dXru, dLru, dXzee):
    
    dLzee = 0.5*(np.array(dXzee) * dLru) / np.array(dXru) # nanometers

    return dLzee


def computeDeltaE(dLzee):

    dE = 1e9*h*c * np.array(dLzee)/LAMBDA**2

    return dE


def computeLande(dE):

    Lande = np.array(dE) / (muB*mj*B)

    return Lande


def computeRMS(X, avgX):

    MSE = np.sum( (np.array(X) - avgX)**2 ) / (len(X) - 1)
    RMSE = np.sqrt(MSE)

    return RMSE


def computeLandeError(Lande, dE, dE_err):

    Lande_e = np.array(Lande)*np.sqrt( (dE_err/np.array(dE))**2 + (1/100)**2 )

    return np.array(Lande_e)


# function to select n elements and skip m elements
def select_skip(iterable, select, skip):
    return [x for i, x in enumerate(iterable) if i % (select+skip) < select]


def main(fname):

    # read data from file
    data = readData(fname)

    # select data based on requested X range
    newData = data[(data['X']>start) & (data['X']<end)]
    newData.reset_index(inplace = True, drop = True)

    # find peaks
    Peaks, intP, zeeP= findPeaks(newData)

    # compute spacing between peaks
    Spacing, Spacing_zee = computeSpacing(Peaks, intP, zeeP)

    # avoid statistical dependence in data 
    newSpacing = select_skip(Spacing, 1, 2)
    newSpacing_zee = select_skip(Spacing_zee[1:-1], 1, 2)

    dLru = computeDeltaLru()

    dLzee = computeDeltaLambda(newSpacing, dLru, newSpacing_zee)
    dLzee_avg = np.average(dLzee)
    dLzee_e = computeRMS(dLzee, dLzee_avg)
    dLzee_avg_e = dLzee_e / np.sqrt(len(dLzee)-1)

    dE = computeDeltaE(dLzee)
    dE_avg = np.average(dE)
    dE_e = computeRMS(dE, dE_avg)
    dE_avg_e = dE_e / np.sqrt(len(dE)-1)

    Lande = computeLande(dE)
    Lande_e = computeLandeError(Lande, dE, dE_e) # a list
    Lande_avg = np.average(Lande, weights=Lande_e**-2)
    Lande_avg_e = np.sqrt(1 / np.sum(Lande_e**-2))

    print('\n' + ' - \u0394\u03BB_zee = ' + format(dLzee_avg, '1.3f') + ' +/- ' + format(dLzee_avg_e, '1.3f') + ' nanometers')
    print('\n' + ' - \u0394E_zee = ' + format(dE_avg, '1.3f') + ' +/- ' + format(dE_avg_e, '1.3f') + ' joules')
    print('\n' + ' - Lande factor gL = ' + format(Lande_avg, '1.4f') + ' +/- ' + format(Lande_avg_e, '1.4f'))
    print('\n' + ' - Precision = ' + format(Lande_avg_e/Lande_avg * 100, '1.2f') + '%')
    print('\n' + ' - Compatibility with 1 = ' + format((Lande_avg - 1)/Lande_avg_e, '1.2f'))


    # plt.show()

    return

 


if __name__ == "__main__":
    main(sys.argv[1])
