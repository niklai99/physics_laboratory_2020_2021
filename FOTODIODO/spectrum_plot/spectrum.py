import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from math import pi
from scipy.optimize import curve_fit, fmin

# ===== constants 

# peak positions
p60_xmin= 460 # 60kEv peak starts here
p60_xmax= 520 # 60kEv peak ends here
p60_en = 59.54 # 60kEv peak precise energy 
p26_en = 26.34 # 26kEv peak precise energy
p14_en=13.95
p18_en=17.75
p17_en = 16.84
p21_en=20.78

#p60esc_en=p60_en-1.8 # escape peak

# probabilities
p14_pr=11.60
p17_pr=2.451
p18_pr=11.83
p21_pr=2.94
p26_pr=2.40
p60_pr=35.78
#p60esc_pr=0
peaks=     [p14_en,p18_en,p21_en,p26_en,p60_en]
#peaks_prob=[p14_pr,p17_en,p18_pr,p26_pr,p60_pr]


def gauss(X,N,mean,sigma):
    return N/((2*pi)**0.5 * sigma) * np.exp( -(X-mean)**2/(2*sigma**2) )


# fit 60keV peak for X calibration
def peak_fitting(data,p_xmin,p_xmax):

    # find peak
    p_Y=data.Y[data.X>p_xmin] [data.X<p_xmax]
    p_X=data.X[data.X>p_xmin] [data.X<p_xmax]

    # fit peak
    par,cov=curve_fit(lambda X, mean, sigma: gauss(X,np.sum(p_Y),mean,sigma), 
                      p_X, p_Y,
                      #sigma=np.sqrt(p_Y), absolute_sigma=True,
                      p0=[np.average(p_X), np.std(p_X)])

    # plot fit
    # fig,_=plt.subplots()
    # xplt=np.linspace(np.amin(p_X), np.amax(p_X))
    # plt.plot(xplt, gauss(xplt,sum(p_Y),*par), color='tomato')
    # plt.hist(p_X,weights=p_Y,histtype='step',bins=len(p_X))
    # plt.title("Calibration - 60keV Histogram")
    # fig.tight_layout()
    
    return par,cov,sum(p_Y)


def main():

    # get histogram data
    Y = np.loadtxt("data")
    X = np.arange(-1,1023) # TODO: change 1023 --> len(data)-1?
    # store data with Pandas
    data=pd.DataFrame({'X': X, 'Y': Y})
    # data['Y']=Y


    # ==== x calibration ====

    # fit 60 keV peak
    par60, cov60, N = peak_fitting(data, p60_xmin, p60_xmax)

    # get gaussian fit maximum 
    # NB: max = - min
    print("============ Axis calibration")
    max_list = fmin(lambda X: -gauss(X, N, *par60), x0=[500]) 
    print("xmax:", max_list[0])

    # get calibration scale factor
    calib = p60_en / max_list[0]

    # calibrate x values
    data.X = data.X * calib 
    #data.Y=data.Y/np.sum(data.Y)

    # plot calibrated histogram
    fig, ax = plt.subplots(figsize = (20, 9.5))

    ax.hist(data.X, weights=data.Y, bins=len(data.X),
               histtype = 'step', color = '#0451FF', linewidth = 1.5)

    
    # plot settings
    ax.set_title('Am-241 Spectrum', fontsize = 24)
    ax.set_xlabel('Energy [keV]', fontsize = 20)
    ax.set_ylabel('ADC counts', fontsize = 20, loc = 'top')
    ax.tick_params(axis = 'both', which = 'major', labelsize = 16, direction = 'out', length = 5)
    ax.set_xlim(left = 9, right = 80)


    fig.tight_layout()
    # fig.savefig('../Plots/am_spectrum.png', dpi = 300, facecolor = 'white')
    plt.show()

    return



if __name__ == "__main__":
   main()


