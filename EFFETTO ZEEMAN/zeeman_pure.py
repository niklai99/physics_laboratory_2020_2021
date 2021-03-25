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
import matplotlib.colors
import seaborn as sns
import struct
import pandas as pd
from matplotlib.colors import ListedColormap

# constants
npixels=7926
maxcolumns=1024
PIXEL_TO_LAMBDA = 7 #micrometers
LAMBDA = 640 * 1e-3 #micrometers


# compute and subtract background
def doBackgroundOp(bkgfrom,bkgto,hist):

    print("subtracting background")

    ncolumns=np.shape(hist)[1]
    for i in range(npixels):

        bkg=0
        # compute mean background for row i
        for j in range(bkgfrom,bkgto):
            bkg+=hist[i][j]
        bkg/=(bkgto-bkgfrom)

        # subtract background from row i
        for j in range(ncolumns):
                hist[i][j] -= bkg

    # update X-projection
    # TODO: do we really need to update this? Or do we want the Y-projection?
    projx = np.empty([ncolumns]) # array to store projection on the X axis
    for i in range(ncolumns):
        sumpx = 0
        for j in range(npixels):
            sumpx+= hist[j][i]
        projx[i] = sumpx

    return hist, projx



# create figure and axis with given ranges
def makeFig(projMin, projMax, projYmin, projYmax, proj):

    # create figure
    fig = plt.figure(figsize=(12,6))

    # create axes
    ax1 = fig.add_subplot(1, 2, 1)
    ax2 = fig.add_subplot(1, 2, 2)

    # define y range for ax2
    #YMAX = np.amax(proj)
    #YMIN = np.amin(proj)
    YMAX = projYmax
    YMIN = projYmin

    # set plot ranges for ax2
    ax2.set_xlim(projMin, projMax)
    ax2.set_ylim(bottom = YMIN * (1 - 1/100), top = YMAX * (1 + 1/100))

    return fig, ax1, ax2



# read data from file and compute X-projection
def getData(fname):

    # read binary file
    pf = open(fname, "rb")

    # read data by chunks and get ncolumns
    ncolumns = 0
    byte = pf.read(npixels*2)
    while byte:
        ncolumns+=1
        byte = pf.read(npixels*2)
    pf.close()

    print("number of columns", ncolumns)

    # read file by chunks (again) to fill histogram
    pf = open(fname, "rb")

    zhist = np.empty([npixels, ncolumns]) # array to store bin height for 2D hist
    projx = np.empty([ncolumns]) # array to store projection on the X axis

    byte = pf.read(npixels*2) # list to store npixels*2 bits of raw data
    icol=0
    while byte:
        sumpx=0
        intList=[] # list to store npixels short integers (2 bits)
        # loop over bits and ~unpack~ them into short integers
        for i in range(0, len(byte), 2):
            intList.append(struct.unpack('<h', byte[i:i+2])[0])
        # store computed integers in 2D matrix
        for i in range(npixels):
            zhist[i, icol]=intList[i]
            # get X projection
            sumpx+=intList[i]

        # read next line and update counters
        projx[icol] = sumpx
        icol+=1
        byte = pf.read(npixels*2)

    pf.close()
    return zhist,ncolumns,projx



# compute Y-projection
def projectToY(zhist, projYfrom, projYto, ncolumns):

    projy = np.empty(npixels)
    print("projecting from", projYfrom, projYto)

    # for i in range(projYfrom, projYto):
    #     sumy=0
    #     for j in range(ncolumns):
    #         sumy+= zhist[i][j]
    #         projy[i]=sumy

    for i in range(npixels):
        sumy = 0
        for j in range(projYfrom, projYto):
            sumy+=zhist[i][j]
        projy[i]=sumy

    return projy



# COMPUTE DELTA X BETWEEN DIFFRACTION PEEKS

# 1) isolate 3 peeks
def display3peeks(proj):

    # starting/ending points of each peek
    p1 = 3525
    p2 = 3600
    p3 = 3675
    p4 = 3750

    p = [p1, p2, p3, p4]
    
    Y = []
    for i in range(p1, p4, 1):
        Y.append(proj[i])

    deltaX = computeDeltaX(Y, p)

    xhist1D = range(p1, p4, 1)

    # create figure
    fig = plt.figure(figsize=(12,6))

    # create axes
    ax = fig.add_subplot(1, 1, 1)

    ax.set_xlim(p1, p4)
    ax.set_ylim(0, np.amax(Y) * (1 + 1/100))

    ax.hist(xhist1D, bins = len(Y), weights = Y, histtype = 'step', color = '#0451FF')

    fig.tight_layout()

    return deltaX

# 2) search for half-max and compute deltaX
def computeDeltaX(Y, p):

    # unpack relevant pixels
    p1, p2, p3, p4 = p

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
    deltaX = ( (pixelHalfTwoLeft - pixelHalfOneRight) + (pixelHalfThreeLeft - pixelHalfTwoRight) ) / 2

    return deltaX




def main(argv):

    # get file name from command line
    fname = argv[0]
    # read data from file and store 2D matrix and X-projection
    zhist, ncolumns, proj = getData(fname)

    # general data for plot
    xhist1D = np.arange(0, ncolumns)
    projMin = 0
    projMax = ncolumns
    YMIN = np.amin(proj)
    YMAX = np.amax(proj)

    # check if user requested background subtraction
    if len(argv)>=3:
        # read given data
        bkgfrom = int(argv[1]) # starting background point
        bkgto = int(argv[2]) # ending background point

        # compute and subtract background
        zhist, proj = doBackgroundOp(bkgfrom, bkgto, zhist)

        # update plot data
        YMIN = np.amin(proj)
        YMAX = np.amax(proj)

        # check if user requested Y-projection
        if len(argv)==5:
            # read given data
            projYfrom = int(argv[3]) # starting projection point
            projYto = int(argv[4]) # ending projection point

            # get projection
            proj = projectToY(zhist, projYfrom, projYto, ncolumns)

            # make 3peeks plot and compute deltaX between peeks
            deltaX = display3peeks(proj)

            # convert pixels to micrometers (?)
            deltaLambda = deltaX * PIXEL_TO_LAMBDA

            # compute resolving power
            R = LAMBDA/deltaLambda
            print('Potere risolvente: ' + format(R, '1.6f'))

            # override plot data
            xhist1D = range(0, npixels)
            projMin = 0
            projMax = npixels
            YMIN = 0
            YMAX = np.amax(proj)


    # make 2D hist data arrays
    x = np.arange(0,npixels+1,1)
    y = np.arange(0,ncolumns+1,1)

    # create a white-to-blue linear colormap
    cmap = ListedColormap([[1-x, 1-x/2, 1, 1] for x in np.arange(0,1,0.05)])

    # prepare plot
    fig, ax1, ax2 = makeFig(projMin, projMax, YMIN, YMAX, proj)

    # 2D histogram
    ax1.pcolormesh(y, x, zhist, cmap = cmap, shading='flat')

    # 1D histogram: x projection
    ax2.hist(xhist1D, bins = len(proj), weights=proj, histtype='step', color = '#0451FF')

    fig.tight_layout()
    plt.show()



if __name__ == "__main__":
   main(sys.argv[1:])
