# Script to identify and fit interference peaks stored in a txt file.
# In addition, some data analysis is automatically computed
#
# USAGE: python resPower.py plotdata.txt
#  where "plotdata.txt" contains the y-projection of the 2d-histogram
#  that is obtained from a ".zee" binary file using the script zeemanPlot.py
#

import sys
import numpy as np
import matplotlib.pyplot as plt
from math import pi
import pandas as pd
from scipy.signal import find_peaks
from scipy.optimize import curve_fit
from scipy.interpolate import UnivariateSpline

# constants
LAMBDA = 585.3 # nanometers
d = 4.04 * 1e6 #nanometers (4.04 millimiters)
dataPath = '../Data/'

start = 3000
end = 7480

binFrac=3 # nBins_new = nBins_old / binFrac


# read data from txt file
def readData(fname):

    # read raw data
    data = pd.read_csv(dataPath + fname, sep = '\t', header = None, names = ['X', 'Y'])

    # change bins and get new y
    newY, edge= np.histogram(data.X, weights=data.Y, bins=int(len(data.X)/binFrac))

    # get new x
    newX = []
    for i in range(len(edge)-1):
        newX.append((edge[i]+edge[i+1])/2)

    # save new data in a Pandassssss dataframe
    data = pd.DataFrame(list(zip(newX,newY)), columns=['X','Y'])

    return data


# fitting function
def Gauss(x, N, x0, sigma):
    return N/(2*pi)**0.5 / sigma * np.exp(-(x - x0)**2 / (2 * sigma**2))


def findPeaks(newData):

    # use scipy signal to identify peaks
    peaks, p = find_peaks(newData['Y'], width=5, prominence=100, rel_height=0.5)
    print("Found", len(peaks), "peaks")

    fig, ax = plt.subplots(figsize=(20,9.5))
    axin1 = ax.inset_axes([3250, 900, (end-start)/2, 600], transform=ax.transData)
    # 

    ax.set_xlim(start, end)
    ax.set_ylim(0, np.amax(newData['Y']) * ( 1 + 5/100 ))


    # plot data
    ax.hist(newData['X'], bins = int(len(newData['X'])), weights = newData['Y'], histtype = 'step', color = '#0451FF')


    xHalfLeft = []
    xHalfRight = []
    xPlotLeft = []
    xPlotRight = []
    FWHM = []
    Peaks = []
    parFit=[]

    

    # loop over peaks
    for i in range(len(peaks)):

        # get fit data
        tr=int((p['right_ips'][i] - p['left_ips'][i])/5)
        xfit=newData['X'].iloc[round(p['left_ips'][i]-tr):round(p['right_ips'][i])+tr]
        yfit=newData['Y'].iloc[round(p['left_ips'][i]-tr):round(p['right_ips'][i])+tr]

        # initial parameters
        mean0=np.average(xfit)
        std0=np.std(xfit)

        # normalization parameter
        ngau=np.sum(yfit*binFrac)

        # fit current peak
        par, cov = curve_fit(lambda x,mean,stddev: Gauss(x,ngau,mean,stddev),
                             xfit, yfit,
                             p0=[mean0, std0])


        halfMax = Gauss(par[0],ngau,*par) / 2

        # compute halfMax pixels
        spline = UnivariateSpline(xfit, Gauss(xfit,ngau,*par) - halfMax , s = 0)
        r1, r2 = spline.roots() # find the roots

        # ax.vlines(x=r1, ymin=0, ymax = np.amax(newData['Y']) * ( 1 + 5/100 ), color = "blue", alpha = 0.3)
        # ax.vlines(x=r2, ymin=0, ymax = np.amax(newData['Y']) * ( 1 + 5/100 ), color = "blue", alpha = 0.3)

        FWHM.append(r2-r1)
        Peaks.append(par[0])
        xHalfLeft.append(r1)
        xHalfRight.append(r2)
        xPlotLeft.append(par[0] - 2*(r2-r1))
        xPlotRight.append(par[0] + 2*(r2-r1))

        # chi2
        diff = yfit-Gauss(xfit,ngau,*par)
        chisq = np.sum(diff**2)/(len(xfit)-2)
        #print("chisq",i, round(abs(chisq-(len(xfit-2)))/ (len(xfit)-2)**0.5 / 2**0.5,2)) # TODO: ricontrollami


        
        # plotting data
        xth = np.linspace(xPlotLeft, xPlotRight, 100)
        yth = Gauss(xth,ngau,*par)

        # plot gaussian fit
        # ax.plot(xth, yth, color='#FF4B00', alpha = 0.8, linestyle = 'dashed')

        

        # save parameters
        parFit.append([ngau, par[0], par[1]])


    slices = []
    for i in range(0, len(xPlotLeft) - 2, 3):
        s = newData[(newData['X'] >= xPlotLeft[i]) & (newData['X'] <= xPlotRight[i+2])]
        slices.append(s)

    
    axin1.plot(np.linspace(xPlotLeft[9], xPlotRight[9], 100), Gauss(np.linspace(xPlotLeft[9], xPlotRight[9], 100),*parFit[9]), color='#FF4B00', alpha = 0.8, linestyle = 'dashed')
    axin1.plot(np.linspace(xPlotLeft[10], xPlotRight[10], 100), Gauss(np.linspace(xPlotLeft[10], xPlotRight[10], 100),*parFit[10]), color='#FF4B00', alpha = 0.8, linestyle = 'dashed')
    axin1.plot(np.linspace(xPlotLeft[11], xPlotRight[11], 100), Gauss(np.linspace(xPlotLeft[11], xPlotRight[11], 100),*parFit[11]), color='#FF4B00', alpha = 0.8, linestyle = 'dashed')
    # axin1.hlines(Gauss(xHalfLeft[10],*parFit[10]), xHalfLeft[10], xHalfRight[10], color = 'red', linestyle = 'solid')
    axin1.hist(slices[3]['X'], bins = int(len(slices[3]['Y'])), weights = slices[3]['Y'], histtype = 'step', color = '#0451FF')
    axin1.set_xlim(slices[3]['X'].iloc[0], slices[3]['X'].iloc[-1])
    axin1.set_ylim(0, np.amax(slices[3]['Y']) * (1 + 5/100))

    return Peaks, FWHM, xHalfLeft, xHalfRight, xPlotLeft, xPlotRight, parFit, ax, fig


def computeSpacing(Peaks):

    C = []
    Spacing = []

    for i in range(1, len(Peaks)):
        C.append(Peaks[i] - Peaks[i-1])

    for i in range(1, len(C)):
        Spacing.append((C[i] + C[i-1]) / 2)

    return Spacing


# plot 16 triplets of peeks
# probably useless
def plot3peaks(newData, xPlotLeft, xPlotRight, parFit):

    slices = []
    for i in range(0, len(xPlotLeft) - 2, 3):
        s = newData[(newData['X'] >= xPlotLeft[i]) & (newData['X'] <= xPlotRight[i+2])]
        slices.append(s)

    # create figure and axes array
    fig, ax = plt.subplots(nrows=2, ncols=4, figsize=(12,6), squeeze=False)
    fig.tight_layout()

    h = 0
    count =0
    # iteration over rows
    for j in range(2):
        # iteration over columns
        for i in range(4):

            # check if there are enough peaks
            if(i+h < len(slices)):

                # plot peaks
                ax[j][i].set_xlim(slices[i+h]['X'].iloc[0], slices[i+h]['X'].iloc[-1])
                ax[j][i].set_ylim(0, np.amax(slices[i+h]['Y']) * (1 + 5/100))
                ax[j][i].hist(slices[i+h]['X'], bins = int(len(slices[i+h]['Y'])), weights = slices[i+h]['Y'], histtype = 'step', color = '#0451FF')

                # plot fits
                for k in range(3):
                    xfit=np.linspace(slices[i+h]['X'].iloc[0],slices[i+h]['X'].iloc[-1])
                    yfit=Gauss(xfit, *parFit[count])
                    ax[j][i].plot(xfit,yfit,'--', color='black')
                    count+=1

            else: break

        h += 4

    return


def computeDeltaLru():

    # approximate formula
    dLru = LAMBDA**2 / (2*d) # nanometers

    return dLru


# function to select n elements and skip m elements
def select_skip(iterable, select, skip):
    return [x for i, x in enumerate(iterable) if i % (select+skip) < select]


def computeDeltaLambda(dXru, dLru, FWHM):
    
    dL = (np.array(FWHM) * dLru) / np.array(dXru) # nanometers

    return dL


def computeResolvingPower(dL):

    R = LAMBDA / np.array(dL)

    return R


def computeRMS(R, avgR):

    MSE = np.sum( (np.array(R) - avgR)**2 ) / (len(R) - 1)
    RMSE = np.sqrt(MSE)

    return RMSE



# ABERRATION ANALYSIS 
def spacingTrend(peakPositions, peakSpacing, peakFWHM):

    # create figure
    fig = plt.figure(figsize=(12,6))

    # create axes
    ax1 = fig.add_subplot(1, 2, 1)
    ax2 = fig.add_subplot(1, 2, 2)

    spline1 = UnivariateSpline(peakPositions, peakSpacing, k = 2)
    spline2 = UnivariateSpline(peakPositions, peakFWHM, k = 2)
    xs = np.linspace(peakPositions[0], peakPositions[-1], 500)

    # show plots
    ax1.plot(peakPositions, peakSpacing, marker = '.', markersize = 18, linewidth = 0, color = '#0451FF')
    ax1.plot(xs, spline1(xs), marker = '.', markersize = 0, linewidth = 2, linestyle = 'dashed', color = '#0451FF')
    ax2.plot(peakPositions, peakFWHM, marker = '.', markersize = 18, linewidth = 0, color = '#0451FF')
    ax2.plot(xs, spline2(xs), marker = '.', markersize = 0, linewidth = 2, linestyle = 'dashed', color = '#0451FF')

    # titles
    ax1.set_title('Peak spacing over Position', fontsize = 24)
    ax2.set_title('FWHM over Position', fontsize = 24)

    # labels
    ax1.set_xlabel('Peak position [# pixel]', fontsize = 18)
    ax2.set_xlabel('Peak position [# pixel]', fontsize = 18)
    ax1.set_ylabel('Peak spacing [# pixel]', fontsize = 18)
    ax2.set_ylabel('FWHM [# pixel]', fontsize = 18)

    ax1.tick_params(axis = 'both', which = 'major', labelsize = 16, direction = 'out', length = 5)
    ax2.tick_params(axis = 'both', which = 'major', labelsize = 16, direction = 'out', length = 5)

    fig.tight_layout()
    # fig.savefig('../Plots/test2.png', dpi = 300, facecolor = 'white')

    return



def main(fname):

    # read data from file
    data = readData(fname)

    # select data based on requested X range
    newData = data[(data['X']>start) & (data['X']<end)]
    newData.reset_index(inplace = True, drop = True)

    # find peaks
    Peaks, FWHM, xHalfLeft, xHalfRight, xPlotLeft, xPlotRight, parFit, ax, fig = findPeaks(newData)

    FWHM_avg = np.average(FWHM)

    # select only relevant FWHMs (select one, skip two, ignoring the first and the last peak)
    fullW = select_skip(FWHM[1:-1], 1, 2)
    fullW_avg = np.average(fullW)
    fullW_e = computeRMS(fullW, fullW_avg)
    fullW_avg_e = fullW_e / np.sqrt(len(fullW))

    # compute spacing between peaks
    Spacing = computeSpacing(Peaks)
    Spacing_avg = np.average(Spacing)

    # compute only relevant spacing means
    dXru = select_skip(Spacing, 1, 2)
    dXru_avg = np.average(dXru)
    dXru_e = computeRMS(dXru, dXru_avg)
    dXru_avg_e = dXru_e / np.sqrt(len(dXru))

    # plot peaks
    # plot3peaks(newData, xPlotLeft, xPlotRight, parFit)

    # plot trends
    # spacingTrend(select_skip(Peaks[1:-1], 1, 2), dXru, fullW)
    spacingTrend(Peaks[1:-1], Spacing, FWHM[1:-1])


    # ------ RESOLVING POWER
    # compute deltaLambda(r.u.)
    dLru = computeDeltaLru()

    # compute deltaLambda for each set of peaks
    dL = computeDeltaLambda(dXru, dLru, fullW)
    dL_avg = np.average(dL)
    dL_e = computeRMS(dL, dL_avg)
    dL_avg_e = dL_e / np.sqrt(len(dL))

    # compute the resolving power for each set of peaks and the average of the three
    R = computeResolvingPower(dL)
    avgR = np.average(R)
    R_e = computeRMS(R, avgR)
    avgR_e = R_e / np.sqrt(len(R))
    # ------


    # ax.text(0.05, 0.75, 
    #         'Average $\Delta x_{r.u.}$ = ' + format(dXru_avg, '1.0f') + ' $\pm$ ' + format(dXru_avg_e, '1.0f') + ' pixels' + '\n'
    #         'Average FWHM = ' + format(fullW_avg, '1.0f') + ' $\pm$ ' + format(fullW_avg_e, '1.0f') + ' pixels' + '\n'
    #         'Average $\Delta\lambda$ = ' + format(dL_avg, '1.4f')  + ' $\pm$ ' + format(dL_avg_e, '1.4f') + ' nanometers' + '\n'
    #         'Average Resolving Power R = ' + format(avgR, '1.0f') + ' $\pm$ ' + format(avgR_e, '1.0f'), 
    #         fontsize = 18, color = '#000000', transform = ax.transAxes)

    ax.set_title('Interference Peaks', fontsize = 24)
    ax.set_xlabel('# pixel', fontsize = 20)
    ax.set_ylabel('ADC counts', fontsize = 20, loc = 'top')
    ax.tick_params(axis = 'both', which = 'major', labelsize = 16, direction = 'out', length = 10)
    ax.set_ylim(top = 1600)

    

    

    # ------ PRINTING
    # print relevant results
    print('\n')
    print('- \u03BB: ' + format(LAMBDA, '1.1f') + ' nanometers')
    print('- \u0394\u03BB (r.u.): ' + format(dLru, '1.3f') + ' nanometers')
    print('- Average Peak spacing: ' + format(Spacing_avg, '1.0f') + ' pixels')
    print('- Average FWHM central Peak: ' + format(FWHM_avg, '1.0f') + ' pixels')
    print('- Average \u0394\u03BB: ' + format(dL_avg, '1.3f') + ' nanometers')
    print('- Average Resolving Power R: ' + format(avgR, '1.0f') + ' +/- ' + format(avgR_e, '1.0f'))
    print('- Resolving Power precision: ' + format(100 * avgR_e/avgR, '1.2f') + '%') 
    print('\n')

    fig.tight_layout()
    # fig.savefig('../Plots/test3.png', dpi = 300, facecolor = 'white')
    plt.show()

    return




if __name__ == "__main__":
    main(sys.argv[1])
