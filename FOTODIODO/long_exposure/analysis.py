import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from math import pi
from scipy.optimize import curve_fit, fmin

# ===== constants 

# peak positions
p60_xmin= 440 # 60kEv peak starts here
p60_xmax= 540 # 60kEv peak ends here
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

def gauss1(X,N,mean,sigma):
    return N * np.exp( -(X-mean)**2/(2*sigma**2) )

# There are many ways to do a multi-peak fit that I can think of.
# Here, I compute 4 different gaussian USING ALWAYS EVERY x value and
# return the sum squared of the 4 values (which is the quantity that we want 
# to to minimize).
# Alterantive: compute only ONE FIT at a time based on the x value and return 
# only that gaussian value. However, given the proximity of the two peaks at 
# 14 and 17 keV, I prefer the first approach.
def multi_gauss(X,N0,N1,N2,N3,N4,sigmaNoise, sigmaEn,k):

    N=[N0,N1,N2,N3,N4]
    v=0
    for i in range(len(peaks)):
        mean = peaks[i]

        if(i!=len(peaks)-1):
            sigma=compute_sigma(sigmaNoise,sigmaEn,mean)
        else: sigma=np.sqrt(sigmaNoise**2 + (sigmaEn*np.sqrt(mean))**2+k )

        v+=gauss(X,N[i],mean,sigma)
        #v += N[i]* np.exp( -(X-mean)**2/(2*sigma**2) )

    return v

# different k for each energy, does not converge :(
def multi_gauss1(X,N0,N1,N2,N3,N4,sn,se0,se1,se2,se3,se4):

    N=[N0,N1,N2,N3,N4]
    se=[se0,se1,se2,se3,se4]
    v=0
    for i in range(len(peaks)):
        mean = peaks[i]
        sigma = np.sqrt(sn**2+(se[i]*np.sqrt(mean))**2) 
        v += N[i]* np.exp( -(X-mean)**2/(2*sigma**2) )

    # v1 = N1/((2*pi)**0.5 * sigma1) * np.exp( -(X-mean1)**2/(2*sigma1**2) )
    return v


# compute sigma for gauss fit
def compute_sigma(sigma_noise,sigma_alfa,energy):
    return np.sqrt(sigma_noise**2 + sigma_alfa**2*energy)


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

    return par,cov,sum(p_Y)



def main():

    # get histogram data
    Y = np.loadtxt("data")
    X = np.arange(-1,1023) # TODO: change 1023 --> len(data)-1?
    # store data with Pandas
    data=pd.DataFrame({'X': X, 'Y': Y})

    # fit 60 keV peak
    par60, cov60, N = peak_fitting(data,p60_xmin,p60_xmax)
    print(par60)
    print(cov60)
    print(N)

    # ==== x calibration ====

    # get gaussian fit maximum 
    # NB: max = - min
    # print("============ Axis calibration"
    max_list= fmin(lambda X: -gauss(X,N,*par60), x0=[500]) 
    # print("xmax:", max_list[0])

    # get calibration scale factor
    calib=p60_en/max_list[0]

    # calibrate x values
    data.X = data.X*calib 
    

    # plot calibrated histogram
    fig, ax = plt.subplots(ncols=1, nrows=2, figsize=(20,9.5),
                           gridspec_kw={'height_ratios': [3, 1]},
                           sharex=True)

    ax[0].hist(data.X,weights=data.Y, bins=len(data.X),
               histtype = 'step', color = '#0451FF', linewidth = 1.5)



    # ==== multi-peak fit ====
    
    # start from x>10
    xmin=12
    Xn=np.array(data.X[data.X>12])
    Yn=np.array(data.Y[data.X>12])

    # multi-peak fit 
    par,cov=curve_fit(multi_gauss,Xn,Yn,)
                      #sigma=np.sqrt(Yn),absolute_sigma=True,
                      #p0=[p14_pr,p18_pr,p21_pr,p26_pr,p60_pr,1,1,0])


    # plot sum of fits
    xgr = np.linspace(np.amin(data.X),np.amax(data.X),1000)
    ygr = multi_gauss(xgr,*par)
    ax[0].plot(xgr,ygr,color='#FF0000', linewidth = 2, zorder = 10, label = 'Multi-peak fit')

    # plot residuals
    diff = Yn - multi_gauss(Xn,*par)
    ax[1].plot(Xn, diff,'.', color='#0451FF')
    ax[1].hlines(0, 0, np.amax(Xn), color = '#000000', linestyle = 'dashed', linewidth = 1)


    # print fit results
    chisq=0
    for i in range(len(diff)):
        if Yn[i]!=0: chisq+=diff[i]**2/Yn[i]

    print("\n============ Fit results")
    print("chisq/ndf",round(chisq,2),"/",len(Xn)-len(par)) # FIXME: error!

    print("sigma noise", round(par[len(peaks)],4))
    print("alfa", round(par[len(peaks)+1],2))
    print("extra (60keV)", round(par[len(peaks)+2],2))



    # ==== plot all gaussians ====

    colors = [
        '#00C415',
        '#8E00C4',
        '#FF8900',
        '#FF00D9'
    ]
    # loop over all peaks except for 60 keV which 
    # will be plotted later

    xgr1 = np.linspace(9,35,1000)
    for i in range(len(peaks)-1):
        
        # compute sigma_i from fit results
        sigma=compute_sigma(par[len(peaks)],par[len(peaks)+1],peaks[i])
        # compute y_i using fit results
        y=gauss(xgr1,par[i],peaks[i], sigma)

        # plot current peak
        ax[0].plot(xgr1,y, '--', color = colors[i], label = format(peaks[i], '1.1f')+' keV peak fit')

        # print peak normalization coefficient
        print("peak:",peaks[i],"keV\t","N:",round(par[i],2))


    # plot 60 keV peak
    sigma=np.sqrt(compute_sigma(par[len(peaks)],par[len(peaks)+1],p60_en)**2+par[-1])
    y=gauss(xgr,par[len(peaks)-1],peaks[-1], sigma)
    ax[0].plot(xgr,y,'--', color = '#006FFF', label = format(peaks[-1], '1.1f')+' keV peak fit')


    # plot config
    ax[0].set_title('Multi-Peak Fit', fontsize = 24)

    # ax[0].set_xlabel('Energy [keV]', fontsize = 20)
    ax[0].set_ylabel('ADC counts', fontsize = 20, loc = 'top')
    ax[1].set_xlabel('Energy [keV]', fontsize = 20)
    ax[1].set_ylabel('Residuals', fontsize = 20, loc = 'center')

    ax[0].tick_params(axis = 'both', which = 'major', labelsize = 16, direction = 'out', length = 5)
    ax[1].tick_params(axis = 'both', which = 'major', labelsize = 16, direction = 'out', length = 5)

    ax[0].set_xlim(left = 9, right = 70)

    ax[0].legend(prop = {'size': 18}, loc = 'best', ncol = 1, frameon = True, fancybox = False, framealpha = 0.5)


    # text 
    N1 = format(peaks[0], '1.1f') + ' keV peak:    N = ' + format(par[0], '1.0f') 
    N2 = format(peaks[1], '1.1f') + ' keV peak:    N = ' + format(par[1], '1.0f') 
    N3 = format(peaks[2], '1.1f') + ' keV peak:    N = ' + format(par[2], '1.0f') 
    N4 = format(peaks[3], '1.1f') + ' keV peak:    N = ' + format(par[3], '1.0f') 
    N5 = format(peaks[4], '1.1f') + ' keV peak:    N = ' + format(par[4], '1.0f') 
    noise = '\u03B7 = ' + format(par[len(peaks)], '1.6f')
    res = '\u03B1 = ' + format(par[len(peaks)+1], '1.2f')

    ax[0].text(40, 2800, 'Normalization Parameters: ', fontsize = 22, fontweight = 'bold', transform=ax[0].transData)
    ax[0].text(41, 2000, N1 + '\n' + N2 + '\n' + N3 + '\n' + N4 + '\n' + N5, fontsize = 18, color = '#000000', transform = ax[0].transData)
    
    ax[0].text(40, 1750, 'Noise Parameter: ', fontsize = 22, fontweight = 'bold', transform=ax[0].transData)
    ax[0].text(41, 1550, noise, fontsize = 18, color = '#000000', transform = ax[0].transData)
    
    ax[0].text(40, 1300, 'Intrinsic Resolution Parameter: ', fontsize = 22, fontweight = 'bold', transform=ax[0].transData)
    ax[0].text(41, 1100, res, fontsize = 18, color = '#000000', transform = ax[0].transData)


    fig.tight_layout()
    # fig.savefig('../Plots/multifit.png', dpi = 300, facecolor = 'white')
    # plt.show()



if __name__ == "__main__":
   main()


