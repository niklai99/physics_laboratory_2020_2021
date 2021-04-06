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

    labels=[
        "No polarimeter",
        "Polarimeter config. 1",
        "Polarimeter config. 2"
    ]

    colors = [
        "#0451FF",
        "#ff3504",
        "#00C415"
    ]


    # create figure
    fig, ax = plt.subplots(figsize=(20,9.5))
    

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
                linewidth = 1.5,
                color = colors[i],
                label=labels[i])


    ax.set_title('Zeeman Peak Splitting', fontsize = 24)
    ax.set_xlabel('# pixel', fontsize = 20)
    ax.set_ylabel('ADC counts', fontsize = 20, loc = 'top')
    ax.tick_params(axis = 'both', which = 'major', labelsize = 16, direction = 'out', length = 10)

    ax.set_ylim(bottom = 0, top = 1400)
    ax.set_xlim(left = 3915, right = 7145)

    ax.legend(loc = 'upper left', prop = {'size': 18})

    fig.tight_layout()
    fig.savefig('../Plots/Bon_overlap2.png', dpi = 300, facecolor = 'white')
    plt.show()
 




if __name__ == "__main__":
    main()
