#!/usr/bin/python

import sys, getopt
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors
import seaborn as sns
import struct
import pandas as pd
from matplotlib.colors import ListedColormap

def makeFig(ncolumns, projx):

    # create figure
    fig = plt.figure(figsize=(12,6))

    # create axes
    ax1 = fig.add_subplot(1, 2, 1)
    ax2 = fig.add_subplot(1, 2, 2)

    # define y range for ax2
    YMAX = np.amax(projx)
    YMIN = np.amin(projx)

    # set plot ranges for ax2
    ax2.set_xlim(left = 0, right = ncolumns-1)
    ax2.set_ylim(bottom = YMIN * (1 - 1/100), top = YMAX * (1 + 1/100))

    return fig, ax1, ax2

def main(argv):

    # read data from command line
    fname = argv[0]


    # features not supported yet
    bkgfrom = -1
    bkgto = -1
    projYfrom = -1
    projYto = -1
    hrname = ''


    # constants
    npixels=7926
    maxcolumns=1024

    # -------- GET DATA --------

    # read binary file
    pf = open(fname, "rb")

    # read data by chunks and store ncolumns
    # NB: needed in Root but redundant with matplotlib
    # TODO: remove this
    ncolumns = 0
    byte = pf.read(npixels*2)
    while byte:
        ncolumns+=1
        byte = pf.read(npixels*2)
    pf.close()

    print("number of columns", ncolumns)

    # read file by chunks (again) to fill histogram
    pf = open(fname, "rb")
    icol = 0

    zhist = np.empty([npixels, ncolumns]) # array to store bin height for 2D hist
    projx = np.empty([ncolumns]) # array to store projection on the X axis

    byte = pf.read(npixels*2) # list to store npixels*2 bits of raw data
    icol = 0
    while byte:
        sumpx=0
        intList=[] # list to store npixels short integers (2 bits)
        # loop over bits and ~unpack~ them into short integers
        for i in range(0, len(byte), 2):
            intList.append(struct.unpack('<h', byte[i:i+2])[0])
        # store computed integers in 2D matrix
        for i in range(npixels):
            zhist[i, icol]=intList[i]
            sumpx+=intList[i]

        # read next line and update counters
        projx[icol] = sumpx
        icol+=1
        byte = pf.read(npixels*2)

    pf.close()

    # -------- ----------- --------


    # -------- MAKE PLOTS --------

    # create and set figure and axes
    fig, ax1, ax2 = makeFig(ncolumns, projx)

    # make data arrays
    x = np.arange(0,npixels+1,1)
    y = np.arange(0,ncolumns+1,1)


    # create a white-to-blue linear colormap
    cmap = ListedColormap([[1-x, 1-x/2, 1, 1] for x in np.arange(0,1,0.05)])
    

    # 2D histogram
    # python is super dumb so y = rows and x = columns
    ax1.pcolormesh(y, x, zhist, cmap = cmap, shading='flat')


    # 1D histogram: x projection 
    ax2.hist(np.arange(0, ncolumns), bins = ncolumns, weights=projx, histtype='step', color = '#0451FF')

    plt.show()





if __name__ == "__main__":
   main(sys.argv[1:])
