import numpy as np

# constants
npixels = 7926

# compute and subtract background
def doBackgroundOp(bkgfrom, bkgto, hist):

    print("subtracting background")

    ncolumns=np.shape(hist)[1]
    for i in range(npixels):

        bkg=0
        # compute mean background for row i
        for j in range(bkgfrom, bkgto):
            bkg += hist[i][j]
        bkg /= (bkgto-bkgfrom)

        # subtract background from row i
        for j in range(ncolumns):
                hist[i][j] -= bkg

    # update X-projection
    projx = np.empty([ncolumns]) # array to store projection on the X axis
    for i in range(ncolumns):
        sumpx = 0
        for j in range(npixels):
            sumpx += hist[j][i]
        projx[i] = sumpx

    return hist, projx


# compute Y-projection
def projectToY(zhist, projYfrom, projYto, ncolumns):

    projy = np.empty(npixels)
    print("projecting from", projYfrom, projYto)

    for i in range(npixels):
        sumy = 0
        for j in range(projYfrom, projYto):
            sumy+=zhist[i][j]
        projy[i]=sumy

    return projy