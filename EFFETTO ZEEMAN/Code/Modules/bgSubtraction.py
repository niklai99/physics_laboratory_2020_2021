import numpy as np

# constants
npixels = 7926

# compute and subtract background
def doBackgroundOp(bkgfrom, bkgto, hist):

    print("subtracting background from ", bkgfrom , "to", bkgto)
    if(bkgto >= len(hist[0])-1): bkgto=len(hist[0])-2

    ncolumns=np.shape(hist)[1]
    for i in range(npixels):

        bkg=0
        # compute mean background for row i
        for j in range(bkgfrom-1, bkgto):
            bkg += hist[i][j+1]
        bkg /= (bkgto-bkgfrom)
        #print(bkg)

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
