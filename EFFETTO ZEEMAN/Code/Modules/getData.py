import struct
import numpy as np

# constants
npixels = 7926

# read data from file and compute X-projection
def getData(fname, dataPath):

    with open(dataPath + fname, "rb") as pf:
        # read data by chunks and get ncolumns
        ncolumns = 0
        byte = pf.read(npixels*2)
        while byte:
            ncolumns+=1
            byte = pf.read(npixels*2)
    print("number of columns", ncolumns)

    with open(dataPath + fname, "rb") as pf:
        zhist = np.empty([npixels, ncolumns]) # array to store bin height for 2D hist
        projx = np.empty([ncolumns]) # array to store projection on the X axis

        byte = pf.read(npixels*2) # list to store npixels*2 bits of raw data
        icol=0
        while byte:
            sumpx=0
            intList = [struct.unpack('<h', byte[i:i+2])[0] for i in range(0, len(byte), 2)]
            # store computed integers in 2D matrix
            for i in range(npixels):
                zhist[i, icol] = intList[i]
                # get X projection
                sumpx += intList[i]

            # read next line and update counters
            projx[icol] = sumpx
            icol += 1
            byte = pf.read(npixels*2)

    return zhist, ncolumns, projx