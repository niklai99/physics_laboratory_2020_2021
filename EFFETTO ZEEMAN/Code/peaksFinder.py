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
from scipy.optimize import curve_fit
from scipy.stats import norm
from math import pi


# constants
npixels=7926
maxcolumns=1024
LAMBDA = 585.3 # nanometers
d = 4.04 * 1e6 #nanometers (4.04 millimiters)
dataPath = '../Data/'


# read data
data = pd.read_csv(dataPath + 'testData.txt', sep = '\t', header = None, names = ['X', 'Y'])
<<<<<<< Updated upstream
X=data.X
Y=data.Y
peaks, p=find_peaks(Y, width=5,prominence=100,rel_height=0.5) # TODO: tweak parameters for better precision
=======
X=np.array(data.X)
Y=np.array(data.Y)
peaks,p=find_peaks(Y, width=5,prominence=100,rel_height=0.5)
#peaksH4,pH4=find_peaks(Y, width=5,prominence=100,rel_height=0.25)
#print(len(peaks), len(peaksH4))
>>>>>>> Stashed changes

# plot data
#plt.plot(X,Y)
Y_e = np.empty(len(Y))
for i in range(len(Y)):
    Y_e[i]=Y[i]**0.5
plt.hist(X,weights=Y,  histtype = 'step', bins=len(Y))
# plot peaks
plt.plot(peaks,Y[peaks], '.', color='pink')

# loop over peaks
for i in range(len(peaks)):
    # get peak start
    x=p['left_ips'][i]
    startPos=np.where(X==int(x))[0][0]
    # get peak end
    x1=p['right_ips'][i]
    endPos=np.where(X==int(x1))[0][0]

    #deltaPos=int((endPos-startPos)/1)
    deltaPos=0
    #print(startPos,endPos)
    # plot limits for curretn peak
    plt.plot(np.linspace(x,x), np.linspace(np.amin(Y),np.amax(Y)),'--')
    plt.plot(np.linspace(x1,x1), np.linspace(np.amin(Y),np.amax(Y)),'--' )

    def gaussian(x, amplitude, mean, stddev):
        return amplitude * np.exp(-(x - mean)**2 / 2 / stddev**2)
    def Gauss(x, N, x0, sigma):
        return N/(2*pi)**0.5 / sigma * np.exp(-(x - x0)**2 / (2 * sigma**2))

    xfit = X[startPos:endPos]
    yfit = Y[startPos:endPos]
    yfit_e=Y_e[startPos:endPos]
    mean0=np.average(xfit)
    std0=np.std(xfit)
    ngau=np.sum(yfit)
    par, std = curve_fit(lambda x,mean,stddev: Gauss(x,ngau,mean,stddev),
                         xfit, yfit, sigma=yfit_e, absolute_sigma=True,
                         p0=[mean0, std0])
    xth = np.linspace(x,x1)
    yth = Gauss(xth,ngau,*par)
    diff = yfit-Gauss(xfit,ngau,*par)
    chisq = np.sum(diff**2)/(len(xfit)-2)
    print(abs(chisq-(len(xfit-2)))/ (len(xfit)-2)**0.5 / 2**0.5)
    plt.plot(xth, yth,color='black')

plt.show()
