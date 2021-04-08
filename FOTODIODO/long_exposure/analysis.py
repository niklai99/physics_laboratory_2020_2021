import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from math import pi
from scipy.optimize import curve_fit, fmin

# constants 
p60_xmin= 440 # 60kEv peak starts here
p60_xmax= 540 # 60kEv peak ends here
p60_en = 59.5409 # 60kEv peak precise energy 
p26_en = 26.3446 # 26kEv peak precise energy
p14_en=13.95
p18_en=17.75
p17_en = 16.84
p21_en=20.78
p60esc_en=p60_en-1.8 # escape peak

p14_pr=11.60
p17_pr=2.451
p18_pr=11.83
p21_pr=2.94
p26_pr=2.40
p60_pr=35.78
p60esc_pr=0
peaks=     [p14_en,p17_en,p18_en,p21_en,p26_en,p60_en]
peaks_prob=[p14_pr,p17_pr,p18_pr,p21_pr,p26_pr,p60_pr]


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
def multi_gauss(X,N0,N1,N2,N3,N4,N5,sigmaNoise, sigmaEn):

    N=[N0,N1,N2,N3,N4,N5]
    v=0
    for i in range(len(peaks)):
        mean = peaks[i]
        sigma = np.sqrt(sigmaNoise**2+(sigmaEn*np.sqrt(mean))**2) 
        v += N[i]/ ((2*pi)**0.5 * sigma) * np.exp( -(X-mean)**2/(2*sigma**2) )
        #v += N[i]* np.exp( -(X-mean)**2/(2*sigma**2) )


    mean=p60esc_en
    #v += Nesc / (2*pi)**0.5 / sigmaEsc * np.exp( -(X-mean)**2/(2*sigmaEsc**2) )
    # v1 = N1/((2*pi)**0.5 * sigma1) * np.exp( -(X-mean1)**2/(2*sigma1**2) )
    return v

def multi_gauss1(X,N0,N1,N2,N3,N4,N5,sn,se0,se1,se2,se3,se4,se5):

    N=[N0,N1,N2,N3,N4,N5]
    se=[se0,se1,se2,se3,se4,se5]
    v=0
    for i in range(len(peaks)):
        mean = peaks[i]
        sigma = np.sqrt(sn**2+(se[i]*np.sqrt(mean))**2) 
        v += N[i]* np.exp( -(X-mean)**2/(2*sigma**2) )

    # v1 = N1/((2*pi)**0.5 * sigma1) * np.exp( -(X-mean1)**2/(2*sigma1**2) )
    return v




def compute_sigma(sigma_noise,sigma_alfa,energy):
    return np.sqrt(sigma_noise**2 + sigma_alfa**2*energy)


def peak_fitting(data,p_xmin,p_xmax):

    # find peak
    p_Y=data.Y[data.X>p_xmin] [data.X<p_xmax]
    p_X=data.X[data.X>p_xmin] [data.X<p_xmax]

    # fit peak
    par,cov=curve_fit(lambda X, mean, sigma: gauss(X,np.sum(p_Y),mean,sigma), 
                      p_X, p_Y,
                      sigma=np.sqrt(p_Y), absolute_sigma=True,
                      p0=[np.average(p_X), np.std(p_X)])

    # plot fit
    #xplt=np.linspace(np.amin(p_X), np.amax(p_X))
    #plt.plot(xplt, gauss(xplt,sum(p_Y),*par), color='tomato')
    
    return par,cov,sum(p_Y)



def main():

 
    #TODO: weight fit

    # get histogram data
    Y = np.loadtxt("data")
    X = np.arange(-1,1023) # TODO: change 1023 --> len(data)-1?
    # store data with Pandas
    data=pd.DataFrame(data=X,columns=['X'])
    data['Y']=Y

    # fit 60 keV peak
    par60, cov60, N = peak_fitting(data,p60_xmin,p60_xmax)
    # TODO: prima stima risoluzione energetica


    # ==== x calibration ====

    # get gaussian fit maximum 
    # NB: max = - min
    max_list= fmin(lambda X: -gauss(X,N,*par60), x0=[500]) 

    # get calibration scale factor
    calib=60/max_list

    # calibrate x values
    data.X = data.X*calib 
    #data.Y=data.Y/np.sum(data.Y)

    # plot calibrated histogram
    fig, ax = plt.subplots(ncols=1, nrows=2, figsize=(12,6),
                           gridspec_kw={'height_ratios': [3, 1]},
                           sharex=True)

    ax[0].hist(data.X,weights=data.Y, bins=len(data.X), histtype = 'step', color='royalblue')
    #plt.hist(p_X,weights=p_Y, bins=len(p_X), histtype = 'step', color='royalblue')


    # ==== multi-peak fit ====
    
    # start from x>9
    Xn=np.array(data.X[data.X>10])
    Yn=np.array(data.Y[data.X>10])

    par,cov=curve_fit(multi_gauss,Xn,Yn)
    xgr= np.linspace(np.amin(data.X),np.amax(data.X),1000)
    ygr= multi_gauss(xgr,*par)
    ax[0].plot(xgr,ygr,color='tomato')
    ax[1].plot(Xn, multi_gauss(Xn,*par)-Yn, color='tomato')

    #print(np.average(data.Y[0:100]))


    # ==== plot all gaussians ====
    eff=np.empty(len(peaks))
    for i in range(len(peaks)):
        sigma=compute_sigma(par[len(peaks)],par[len(peaks)+1],peaks[i])
        y=gauss(xgr,par[i],peaks[i], sigma)
        ax[0].plot(xgr,y,":", color='gray')
        #prob = par[i] * np.sqrt(2*pi)*sigma /reference
        eff[i]=par[i]
        print("peak: ", peaks[i], " keV\t", "N: ",  round(par[i],2))


    eff = eff / par[len(peaks)-1]
    fig = plt.figure()
    plt.plot(peaks, eff,color='tomato')

    plt.show()



if __name__ == "__main__":
   main()


