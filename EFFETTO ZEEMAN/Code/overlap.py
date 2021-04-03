# Script to overlap multiple histograms.
from scipy.signal import savgol_filter
import numpy as np
import matplotlib.pyplot as plt
from math import pi
import pandas as pd

binFrac=5 # nBins_new = nBins_old / binFrac

def readData(fname):

    # read raw data
    data = pd.read_csv('../Data/' + fname,
                       sep = '\t',
                       header = None,
                       names = ['X', 'Y'])

    # change bins and get new y
    newY, edge= np.histogram(data.X, weights=data.Y,
                             bins=int(len(data.X)/
                                      binFrac)
                             )

    # get new x
    newX = []
    for i in range(len(edge)-1):
        newX.append((edge[i]+edge[i+1])/2)

    # save new data in a Pandassssss dataframe
    data = pd.DataFrame(list(zip(newX,newY)),
                        columns=['X','Y'])

    return data


def main():

    # You can choose which histograms to show
    # by (un)commenting the required entries
    # in ~names~.
    # TODO: define a ~color~ list

    # --- Bon_g + Bon_gp --- #
    names=[
        "bon_g.txt",
        # comment like this!
        "bon_gp.txt",
        "bon_gp2.txt",
    ]


    # create figure
    fig, ax = plt.subplots(figsize=(12,6))
    fig.tight_layout()

    data=[] # store all datasets

    # loop over requested names
    for i in range(len(names)):

        # get current dataset
        data.append(readData(names[i]))

        # plot histograms
        ax.hist(data[i]['X'],
                bins = len(data[i]['X']),
                weights = savgol_filter(data[i]['Y'],11,3),
                histtype = 'step',
                label=names[i])

    plt.legend()
    plt.show()
 




if __name__ == "__main__":
    main()
