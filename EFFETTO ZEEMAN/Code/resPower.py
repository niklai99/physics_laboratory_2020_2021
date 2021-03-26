#!/usr/bin/python
#%config InlineBackend.figure_format = 'png'

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


# constants
npixels=7926
maxcolumns=1024
LAMBDA = 585.3 # nanometers
d = 4.04 * 1e6 #nanometers (4.04 millimiters)
dataPath = '../Data/'

# starting/ending points of each Peak:
# first three peaks set (left)
p1_1 = 1950
p1_2 = 2050
p1_3 = 2160
p1_4 = 2260

# second three peaks set (center)
p2_1 = 3525
p2_2 = 3600
p2_3 = 3675
p2_4 = 3750

# third three peaks set (right)
p3_1 = 5290
p3_2 = 5350
p3_3 = 5410
p3_4 = 5470


# read data from txt file
def readData():

    data = pd.read_csv(dataPath + 'testData.txt', sep = '\t', header = None, names = ['X', 'Y'])

    return data


# COMPUTE DELTA X BETWEEN DIFFRACTION peakS

# 1) isolate 3 peaks
def display3peaks(data):
    
    slice1 = data[(data['X'] >= p1_1) & (data['X'] <= p1_4)]
    slice2 = data[(data['X'] >= p2_1) & (data['X'] <= p2_4)]
    slice3 = data[(data['X'] >= p3_1) & (data['X'] <= p3_4)]

    # create figure
    fig = plt.figure(figsize=(12,6))

    # create axes
    ax1 = fig.add_subplot(1, 3, 1)
    ax2 = fig.add_subplot(1, 3, 2)
    ax3 = fig.add_subplot(1, 3, 3)

    # axis limits
    ax1.set_xlim(p1_1, p1_4)
    ax1.set_ylim(0, np.amax(slice1['Y']) * (1 + 5/100))

    ax2.set_xlim(p2_1, p2_4)
    ax2.set_ylim(0, np.amax(slice2['Y']) * (1 + 5/100))

    ax3.set_xlim(p3_1, p3_4)
    ax3.set_ylim(0, np.amax(slice3['Y']) * (1 + 5/100))

    # show plots
    ax1.hist(slice1['X'], bins = len(slice1['Y']), weights = slice1['Y'], histtype = 'step', color = '#0451FF')
    ax2.hist(slice2['X'], bins = len(slice2['Y']), weights = slice2['Y'], histtype = 'step', color = '#0451FF')
    ax3.hist(slice3['X'], bins = len(slice3['Y']), weights = slice3['Y'], histtype = 'step', color = '#0451FF')

    # titles
    ax1.set_title('Left set of peaks')
    ax2.set_title('Central set of peaks')
    ax3.set_title('Right set of peaks')

    # labels
    ax1.set_xlabel('# pixel')
    ax2.set_xlabel('# pixel')
    ax3.set_xlabel('# pixel')
    ax1.set_ylabel('intensity [a.u.]')
    ax2.set_ylabel('intensity [a.u.]')
    ax3.set_ylabel('intensity [a.u.]')

    fig.tight_layout()

    return slice1, slice2, slice3


# 2) search for half-max and compute deltaX
def computeDeltaXru(slice1, slice2, slice3):

    Y1 = np.array(slice1['Y'])
    Y2 = np.array(slice2['Y'])
    Y3 = np.array(slice3['Y'])

    # slice three peaks
    peakOne1 = Y1[:(p1_2-p1_1)]
    peakTwo1 = Y1[(p1_2-p1_1):(p1_3-p1_2)+(p1_2-p1_1)]
    peakThree1 = Y1[(p1_3-p1_2)+(p1_2-p1_1):]

    peakOne2 = Y2[:(p2_2-p2_1)]
    peakTwo2 = Y2[(p2_2-p2_1):(p2_3-p2_2)+(p2_2-p2_1)]
    peakThree2 = Y2[(p2_3-p2_2)+(p2_2-p2_1):]

    peakOne3 = Y3[:(p3_2-p3_1)]
    peakTwo3 = Y3[(p3_2-p3_1):(p3_3-p3_2)+(p3_2-p3_1)]
    peakThree3 = Y3[(p3_3-p3_2)+(p3_2-p3_1):]

    # find max value for each Peak
    maxOne1 = np.amax(peakOne1)
    maxTwo1 = np.amax(peakTwo1)
    maxThree1 = np.amax(peakThree1)

    maxOne2 = np.amax(peakOne2)
    maxTwo2 = np.amax(peakTwo2)
    maxThree2 = np.amax(peakThree2)

    maxOne3 = np.amax(peakOne3)
    maxTwo3 = np.amax(peakTwo3)
    maxThree3 = np.amax(peakThree3)

    # find max index for each Peak
    indexOne1 = np.argmax(peakOne1)
    indexTwo1 = np.argmax(peakTwo1)
    indexThree1 = np.argmax(peakThree1)

    indexOne2 = np.argmax(peakOne2)
    indexTwo2 = np.argmax(peakTwo2)
    indexThree2 = np.argmax(peakThree2)

    indexOne3 = np.argmax(peakOne3)
    indexTwo3 = np.argmax(peakTwo3)
    indexThree3 = np.argmax(peakThree3)

    indexMax = [indexTwo1 + p1_2, indexTwo2 + p2_2, indexTwo3 + p3_2]

    # compute half max
    halfOne1 = maxOne1/2
    halfTwo1 = maxTwo1/2
    halfThree1 = maxThree1/2

    halfOne2 = maxOne2/2
    halfTwo2 = maxTwo2/2
    halfThree2 = maxThree2/2

    halfOne3 = maxOne3/2
    halfTwo3 = maxTwo3/2
    halfThree3 = maxThree3/2

    # search index for half max
    halfIndexOneLeft1 = (np.abs(peakOne1[:indexOne1]-halfOne1)).argmin() 
    halfIndexOneRight1 = (np.abs(peakOne1[indexOne1:]-halfOne1)).argmin() + indexOne1 
    halfIndexTwoLeft1 = (np.abs(peakTwo1[:indexTwo1]-halfTwo1)).argmin() 
    halfIndexTwoRight1 = (np.abs(peakTwo1[indexTwo1:]-halfTwo1)).argmin() + indexTwo1
    halfIndexThreeLeft1 = (np.abs(peakThree1[:indexThree1]-halfThree1)).argmin() 
    halfIndexThreeRight1 = (np.abs(peakThree1[indexThree1:]-halfThree1)).argmin() + indexThree1

    halfIndexOneLeft2 = (np.abs(peakOne2[:indexOne2]-halfOne2)).argmin() 
    halfIndexOneRight2 = (np.abs(peakOne2[indexOne2:]-halfOne2)).argmin() + indexOne2 
    halfIndexTwoLeft2 = (np.abs(peakTwo2[:indexTwo2]-halfTwo2)).argmin() 
    halfIndexTwoRight2 = (np.abs(peakTwo2[indexTwo2:]-halfTwo2)).argmin() + indexTwo2
    halfIndexThreeLeft2 = (np.abs(peakThree2[:indexThree2]-halfThree2)).argmin() 
    halfIndexThreeRight2 = (np.abs(peakThree2[indexThree2:]-halfThree2)).argmin() + indexThree2

    halfIndexOneLeft3 = (np.abs(peakOne3[:indexOne3]-halfOne3)).argmin() 
    halfIndexOneRight3 = (np.abs(peakOne3[indexOne3:]-halfOne3)).argmin() + indexOne3 
    halfIndexTwoLeft3 = (np.abs(peakTwo3[:indexTwo3]-halfTwo3)).argmin() 
    halfIndexTwoRight3 = (np.abs(peakTwo3[indexTwo3:]-halfTwo3)).argmin() + indexTwo3
    halfIndexThreeLeft3 = (np.abs(peakThree3[:indexThree3]-halfThree3)).argmin() 
    halfIndexThreeRight3 = (np.abs(peakThree3[indexThree3:]-halfThree3)).argmin() + indexThree3

    # compute pixel number related to half maxs
    pixelHalfOneLeft1 = halfIndexOneLeft1 + p1_1
    pixelHalfOneRight1 = halfIndexOneRight1 + p1_1
    pixelHalfTwoLeft1 = halfIndexTwoLeft1 + p1_2
    pixelHalfTwoRight1 = halfIndexTwoRight1 + p1_2
    pixelHalfThreeLeft1 = halfIndexThreeLeft1 + p1_3
    pixelHalfThreeRight1 = halfIndexThreeRight1 + p1_3

    pixelHalfOneLeft2 = halfIndexOneLeft2 + p2_1
    pixelHalfOneRight2 = halfIndexOneRight2 + p2_1
    pixelHalfTwoLeft2 = halfIndexTwoLeft2 + p2_2
    pixelHalfTwoRight2 = halfIndexTwoRight2 + p2_2
    pixelHalfThreeLeft2 = halfIndexThreeLeft2 + p2_3
    pixelHalfThreeRight2 = halfIndexThreeRight2 + p2_3

    pixelHalfOneLeft3 = halfIndexOneLeft3 + p3_1
    pixelHalfOneRight3 = halfIndexOneRight3 + p3_1
    pixelHalfTwoLeft3 = halfIndexTwoLeft3 + p3_2
    pixelHalfTwoRight3 = halfIndexTwoRight3 + p3_2
    pixelHalfThreeLeft3 = halfIndexThreeLeft3 + p3_3
    pixelHalfThreeRight3 = halfIndexThreeRight3 + p3_3


    # average distance between half maxs (probably wrong path to follow, according to Lunardon)
    # deltaXru = ( (pixelHalfTwoLeft - pixelHalfOneRight) + (pixelHalfThreeLeft - pixelHalfTwoRight) ) / 2

    # average distance between peaks (probably better path to follow)
    deltaXru1 = ( ((indexTwo1+p1_2) - (indexOne1+p1_1)) + ((indexThree1+p1_3) - (indexTwo1+p1_2)) ) / 2
    deltaXru2 = ( ((indexTwo2+p2_2) - (indexOne2+p2_1)) + ((indexThree2+p2_3) - (indexTwo2+p2_2)) ) / 2
    deltaXru3 = ( ((indexTwo3+p3_2) - (indexOne3+p3_1)) + ((indexThree3+p3_3) - (indexTwo3+p3_2)) ) / 2

    deltaXru = [deltaXru1, deltaXru2, deltaXru3]

    # FWHF of central Peak
    x1 = pixelHalfTwoRight1 - pixelHalfTwoLeft1
    x2 = pixelHalfTwoRight2 - pixelHalfTwoLeft2
    x3 = pixelHalfTwoRight3 - pixelHalfTwoLeft3

    x = [x1, x2, x3]

    return deltaXru, x, indexMax


def computeDeltaLru():

    # approximate formula
    dLru = LAMBDA**2 / (2*d) # nanometers

    return dLru


def computeDeltaLambda(dXru, dLru, x):

    dL = (np.array(x) * dLru) / np.array(dXru) # nanometers

    return dL


def computeResolvingPower(dL):

    R = LAMBDA / np.array(dL)

    return R


# ABERRATION ANALYSIS (more datapoints needed ---> we have to consider more than three sets [10 will do fine!])
def spacingTrend(dXru, x, indexMax):

    # create figure
    fig = plt.figure(figsize=(12,6))

    # create axes
    ax1 = fig.add_subplot(1, 2, 1)
    ax2 = fig.add_subplot(1, 2, 2)

    # show plots
    ax1.plot(indexMax, dXru, marker = '.', markersize = 15, linewidth = 1, color = '#0451FF')
    ax2.plot(x, dXru, marker = '.', markersize = 15, linewidth = 1, color = '#0451FF')

    # titles
    ax1.set_title('Peak spacing over Position')
    ax2.set_title('Peak spacing over FWHM')

    # labels
    ax1.set_xlabel('Peak position [# pixel]')
    ax2.set_xlabel('FWHM [# pixel]')
    ax1.set_ylabel('Peak spacing [# pixel]')
    ax2.set_ylabel('Peak spacing [# pixel]')

    fig.tight_layout()

    return


def main():

    # read data from txt file
    data = readData()

    # isolate three set of three peaks each
    slice1, slice2, slice3 = display3peaks(data)

    # compute deltaX(r.u.) and FWHM of the central Peak for each set 
    dXru, x, indexMax = computeDeltaXru(slice1, slice2, slice3)

    # compute deltaLambda(r.u.)
    dLru = computeDeltaLru()

    # compute deltaLambda for each set of peaks
    dL = computeDeltaLambda(dXru, dLru, x)

    # compute the resolving power for each set of peaks and the average of the three
    R = computeResolvingPower(dL)
    avgR = np.average(R)

    # print relevant results
    print('\n')
    print('- \u03BB: ' + format(LAMBDA, '1.1f') + ' nanometers')
    print('- \u0394\u03BB (r.u.): ' + format(dLru, '1.3f') + ' nanometers')
    print('- Average Peak spacing: ' + format(np.average(dXru), '1.0f') + ' pixels')
    print('- Average FWHF central Peak: ' + format(np.average(x), '1.0f') + ' pixels')
    print('- Average \u0394\u03BB: ' + format(np.average(dL), '1.3f') + ' nanometers')
    print('- Average Resolving Power R: ' + format(avgR, '1.0f'))
    print('\n')

    spacingTrend(dXru, x, indexMax)
    plt.show()


if __name__ == "__main__":
    main()
