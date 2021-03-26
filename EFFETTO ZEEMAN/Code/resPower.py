#!/usr/bin/python
#%config InlineBackend.figure_format = 'png'
# usage:
# read and plot data:
#   python zeeman_pure.py zeeman_image.zee
#
# + subtract background after computing mean bkg in given range (es: 120-140)
#   python zeeman_pure.py zeeman_image.zee 120 140
#
# + plot Y-projection in given range (es: 80-100)
#   python zeeman_pure.py zeeman_image.zee 120 140 80 100


import sys, getopt
import numpy as np
import matplotlib.pyplot as plt
import struct
import pandas as pd
from matplotlib.colors import ListedColormap


# constants
npixels=7926
maxcolumns=1024
LAMBDA = 585.3 # nanometers
d = 4.04 * 1e6 #nanometers (4.04 millimiters)
dataPath = '../Data/'

# starting/ending points of each peek
p1 = 3525
p2 = 3600
p3 = 3675
p4 = 3750


# read data from txt file
def readData():

    data = pd.read_csv(dataPath + 'testData.txt', sep = '\t', header = None, names = ['X', 'Y'])

    return data


# COMPUTE DELTA X BETWEEN DIFFRACTION PEEKS

# 1) isolate 3 peeks
def display3peeks(data):
    
    Slice = data[(data['X'] >= p1) & (data['X'] <= p4)]

    # create figure
    fig = plt.figure(figsize=(12,6))

    # create axes
    ax = fig.add_subplot(1, 1, 1)

    ax.set_xlim(p1, p4)
    ax.set_ylim(0, np.amax(data['Y']) * (1 + 1/100))

    ax.hist(data['X'], bins = len(data['Y']), weights = data['Y'], histtype = 'step', color = '#0451FF')

    fig.tight_layout()

    return Slice


# 2) search for half-max and compute deltaX
def computeDeltaXru(Slice):

    Y = np.array(Slice['Y'])

    # slice three peeks
    peekOne = Y[:(p2-p1)]
    peekTwo = Y[(p2-p1):(p3-p2)+(p2-p1)]
    peekThree = Y[(p3-p2)+(p2-p1):]

    # find max value for each peek
    maxOne = np.amax(peekOne)
    maxTwo = np.amax(peekTwo)
    maxThree = np.amax(peekThree)
    
    # print(maxOne)
    # print(maxTwo)
    # print(maxThree)

    # find max index for each peek
    indexOne = np.argmax(peekOne)
    indexTwo = np.argmax(peekTwo)
    indexThree = np.argmax(peekThree)

    # print(p1 + indexOne)
    # print(p2 + indexTwo)
    # print(p3 + indexThree)

    # compute half max
    halfOne = maxOne/2
    halfTwo = maxTwo/2
    halfThree = maxThree/2

    # search index for half max
    halfIndexOneLeft = (np.abs(peekOne[:indexOne]-halfOne)).argmin() 
    halfIndexOneRight = (np.abs(peekOne[indexOne:]-halfOne)).argmin() + indexOne 
    halfIndexTwoLeft = (np.abs(peekTwo[:indexTwo]-halfTwo)).argmin() 
    halfIndexTwoRight = (np.abs(peekTwo[indexTwo:]-halfTwo)).argmin() + indexTwo
    halfIndexThreeLeft = (np.abs(peekThree[:indexThree]-halfThree)).argmin() 
    halfIndexThreeRight = (np.abs(peekThree[indexThree:]-halfThree)).argmin() + indexThree

    # compute pixel number related to half maxs
    pixelHalfOneLeft = halfIndexOneLeft + p1
    pixelHalfOneRight = halfIndexOneRight + p1
    pixelHalfTwoLeft = halfIndexTwoLeft + p2
    pixelHalfTwoRight = halfIndexTwoRight + p2
    pixelHalfThreeLeft = halfIndexThreeLeft + p3
    pixelHalfThreeRight = halfIndexThreeRight + p3

    # print(pixelHalfOneLeft)
    # print(pixelHalfOneRight)
    # print(pixelHalfTwoLeft)
    # print(pixelHalfTwoRight)
    # print(pixelHalfThreeLeft)
    # print(pixelHalfThreeRight)

    # average distance between half maxs
    deltaXru = ( (pixelHalfTwoLeft - pixelHalfOneRight) + (pixelHalfThreeLeft - pixelHalfTwoRight) ) / 2

    # FWHF of central peek
    x = pixelHalfTwoRight - pixelHalfTwoLeft

    return deltaXru, x


def computeDeltaLru():

    # approximate formula
    dLru = LAMBDA**2 / (2*d) # nanometers

    return dLru


def computeDeltaLambda(dXru, dLru, x):

    dL = (x * dLru) / dXru

    return dL


def computeResolvingPower(dL):

    R = LAMBDA / dL

    return R


def main():

    data = readData()

    Slice = display3peeks(data)
    dXru, x = computeDeltaXru(Slice)
    dLru = computeDeltaLru()
    dL = computeDeltaLambda(dXru, dLru, x)
    R = computeResolvingPower(dL)

    print('\n')
    print('-\u03BB: ' + format(LAMBDA, '1.1f') + ' nanometers')
    print('-\u0394\u03BB (r.u.): ' + format(dLru, '1.3f') + ' nanometers')
    print('-Peek spacing: ' + format(dXru, '1.0f') + ' pixels')
    print('-FWHF central peek: ' + format(x, '1.0f') + ' pixels')
    print('-\u0394\u03BB: ' + format(dL, '1.3f') + ' nanometers')
    print('-Resolving Power R: ' + format(R, '1.0f'))
    print('\n')

    plt.show()


if __name__ == "__main__":
   main()
