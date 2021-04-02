#!/usr/bin/python
#
# usage:
# read and plot data:
#   python zeemanPlot.py zeeman_image.zee
#
# + subtract background after computing mean bkg in given range (es: 120-140)
#   python zeemanPlot.py zeeman_image.zee 120 140
#
# + plot Y-projection in given range (es: 80-100)
#   python zeemanPlot.py zeeman_image.zee 120 140 80 100
#
# + save Y-projection in fname.txt
#   python zeemanPlot.py zeeman_image.zee 120 140 80 100 fname.txt


import sys, getopt
import numpy as np
import matplotlib.pyplot as plt
import struct
from matplotlib.colors import ListedColormap

from Modules.getData import getData
from Modules.bgSubtraction import doBackgroundOp, projectToY

# constants
npixels=7926
maxcolumns=1024
PIXEL_TO_LAMBDA = 7 #micrometers
LAMBDA = 585.3 * 1e-3 #micrometers
dataPath = '../Data/'



# create figure and axis with given ranges
def makeFig(projMin, projMax, projYmin, projYmax, proj):

    # create figure
    fig = plt.figure(figsize=(12,6))

    # create axes
    ax1 = fig.add_subplot(1, 2, 1)
    ax2 = fig.add_subplot(1, 2, 2)

    # define y range for ax2
    YMAX = projYmax
    YMIN = projYmin

    # set plot ranges for ax2
    ax2.set_xlim(projMin, projMax)
    ax2.set_ylim(bottom = YMIN * (1 - 1/100), top = YMAX * (1 + 1/100))

    return fig, ax1, ax2




def main(argv):

    # get file name from command line
    fname = argv[0]

    # read data from file and store 2D matrix and X-projection
    zhist, ncolumns, proj = getData(fname, dataPath)

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
        if len(argv)>=5:
            # read given data
            projYfrom = int(argv[3]) # starting projection point
            projYto = int(argv[4]) # ending projection point

            # get projection
            proj = projectToY(zhist, projYfrom, projYto, ncolumns)
            print("Entries", np.sum(proj))

            # override plot data
            xhist1D = range(0, npixels)
            projMin = 0
            projMax = npixels
            YMIN = 0
            YMAX = np.amax(proj)

            # save data for analysis
            #print("saving file", name)
            if len(argv)==6:
                name = argv[5]
                print("saving file", name)
                np.savetxt(fname = dataPath + name, X = np.c_[xhist1D, proj], delimiter = '\t')
            # np.savetxt(fname = dataPath + 'spettro2d_Boff.txt', X = np.c_[xhist1D, proj], delimiter = '\t')


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
