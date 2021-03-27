#!/usr/bin/env python3
#
#
# Simple script to find and plot peaks
# To execute:
#   python peaksFinder.py
#
# You can use the interactive matplotlib tools to
# zoom directly from the plot window.

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.signal import find_peaks


# constants
npixels=7926
maxcolumns=1024
LAMBDA = 585.3 # nanometers
d = 4.04 * 1e6 #nanometers (4.04 millimiters)
dataPath = '../Data/'


# read data
data = pd.read_csv(dataPath + 'testData.txt', sep = '\t', header = None, names = ['X', 'Y'])
X=data.X
Y=data.Y
peaks,p=find_peaks(Y, width=5,prominence=100,rel_height=0.5) # TODO: tweak parameters for better precision

# plot data
plt.plot(X,Y)
# plot peaks
plt.plot(peaks,Y[peaks], '.', color='pink')

# loop over peaks
for i in range(len(peaks)):
    # get peak start
    x=p['left_ips'][i]
    # get peak end
    x1=p['right_ips'][i]
    # plot limits for curretn peak
    plt.plot(np.linspace(x,x), np.linspace(np.amin(Y),np.amax(Y)),'--')
    plt.plot(np.linspace(x1,x1), np.linspace(np.amin(Y),np.amax(Y)),'--' )

plt.show()
