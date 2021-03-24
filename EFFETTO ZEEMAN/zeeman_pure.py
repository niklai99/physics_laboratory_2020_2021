#!/usr/bin/python

import sys, getopt
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors
import seaborn as sns
import struct
import pandas as pd

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

    # plot
    fig,ax = plt.subplots(ncols=2)
    x = np.arange(0,npixels+1,1)
    y = np.arange(0,ncolumns+1,1)
    # python is super dumb so y = rows and x = columns
    ax[0].pcolormesh(y,x, zhist, shading='flat')

    # ax[1].bar(np.arange(0,ncolumns), projx,
    #              width=1.0, color='royalblue')

    ax[1].hist(np.arange(0,ncolumns), bins = 150, weights=projx, histtype='step')

    ax[1].set_ylim(460000,500000)
    plt.show()





if __name__ == "__main__":
   main(sys.argv[1:])
