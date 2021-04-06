import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from math import pi
from scipy.optimize import curve_fit, fmin

# constants TODO: double-check all energies
p60_xmin= 440 # 60kEv peak starts here
p60_xmax= 540 # 60kEv peak ends here
p60_en = 59.5409 # 60kEv peak precise energy 

p26_en = 26.3446 # 26kEv peak precise energy

p14_en = (13.76 + 13.944)/2 
p14_en=14
p17_en = (16.13 +17.79)/2
p17_en=18

p15_en=15.876
p21_en=21


def gauss(X,N,mean,sigma):
    return N/((2*pi)**0.5 * sigma) * np.exp( -(X-mean)**2/(2*sigma**2) )


# There are many ways to do a multi-peak fit that I can think of.
# Here, I compute 4 different gaussian USING ALWAYS EVERY x value and
# return the sum squared of the 4 values (which is the quantity that we want 
# to to minimize).
# Alterantive: compute only ONE FIT at a time based on the x value and return 
# only that gaussian value. However, given the proximity of the two peaks at 
# 14 and 17 keV, I prefer the first approach.
def multi_gauss(X,N1,N2,N3,N4,N5,N6,sigmaNoise, sigmaEn):
    mean1=p60_en
    mean2=p26_en
    mean3=p14_en
    mean4=p17_en

    mean5=p15_en
    mean6=p21_en

    sigma1=np.sqrt(sigmaNoise**2+(sigmaEn*np.sqrt(mean1))**2) # TODO: double-check
    sigma2=np.sqrt(sigmaNoise**2+(sigmaEn*np.sqrt(mean2))**2)
    sigma3=np.sqrt(sigmaNoise**2+(sigmaEn*np.sqrt(mean3))**2)
    sigma4=np.sqrt(sigmaNoise**2+(sigmaEn*np.sqrt(mean4))**2)

    sigma5=np.sqrt(sigmaNoise**2+(sigmaEn*np.sqrt(mean5))**2)
    sigma6=np.sqrt(sigmaNoise**2+(sigmaEn*np.sqrt(mean6))**2)

    v1 = N1/((2*pi)**0.5 * sigma1) * np.exp( -(X-mean1)**2/(2*sigma1**2) )
    v2 = N2/((2*pi)**0.5 * sigma2) * np.exp( -(X-mean2)**2/(2*sigma2**2) )
    v3 = N3/((2*pi)**0.5 * sigma3) * np.exp( -(X-mean3)**2/(2*sigma3**2) )
    v4 = N4/((2*pi)**0.5 * sigma4) * np.exp( -(X-mean4)**2/(2*sigma4**2) )

    v1 = N1* np.exp( -(X-mean1)**2/(2*sigma1**2) )
    v2 = N2* np.exp( -(X-mean2)**2/(2*sigma2**2) )
    v3 = N3* np.exp( -(X-mean3)**2/(2*sigma3**2) )
    v4 = N4* np.exp( -(X-mean4)**2/(2*sigma4**2) )

    v5 = N5* np.exp( -(X-mean5)**2/(2*sigma5**2) )
    v6 = N6* np.exp( -(X-mean6)**2/(2*sigma6**2) )


    #return np.sqrt(v1**2+v2**2+v3**2+v4**2)
    #return np.sqrt(v1**2+v2**2+v3**2+v4**2+v5**2+v6**2)
    return v1+v2+v3+v4+v5+v6
    #return v1+v3+v4
    #return v4
    #return v1

def multi_gauss1(Xt,sigmaNoise, sigmaEn):
    X=Xt[0]
    t=Xt[1]
    N=Xt[2]
    mean1=p60_en
    mean2=p26_en
    mean3=p14_en
    mean4=p17_en
    sigma1=np.sqrt(sigmaNoise**2+(sigmaEn*np.sqrt(mean1))**2) # TODO: double-check
    sigma2=np.sqrt(sigmaNoise**2+(sigmaEn*np.sqrt(mean2))**2)
    sigma3=np.sqrt(sigmaNoise**2+(sigmaEn*np.sqrt(mean3))**2)
    sigma4=np.sqrt(sigmaNoise**2+(sigmaEn*np.sqrt(mean4))**2)

    if t==0:
        v1 = N/((2*pi)**0.5 * sigma1) * np.exp( -(X-mean1)**2/(2*sigma1**2) )
        return v1
    elif t==1:
        v2 = N/((2*pi)**0.5 * sigma2) * np.exp( -(X-mean2)**2/(2*sigma2**2) )
        return v2
    elif t==2:
        v3 = N/((2*pi)**0.5 * sigma3) * np.exp( -(X-mean3)**2/(2*sigma3**2) )
        return v3
    elif t==3:
        v4 = N/((2*pi)**0.5 * sigma4) * np.exp( -(X-mean4)**2/(2*sigma4**2) )
        return v4


def peak_fitting(data,p_xmin,p_xmax):

    # find peak
    p_Y=data.Y[data.X>p_xmin] [data.X<p_xmax]
    p_X=data.X[data.X>p_xmin] [data.X<p_xmax]

    # fit peak
    par,cov=curve_fit(lambda X, mean, sigma: gauss(X,np.sum(p_Y),mean,sigma), 
                      p_X, p_Y,
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
    plt.hist(data.X,weights=data.Y, bins=len(data.X), histtype = 'step', color='royalblue')
    #plt.hist(p_X,weights=p_Y, bins=len(p_X), histtype = 'step', color='royalblue')


    # ==== multi-peak fit ====
    
    # start from x>9
    Xn=np.array(data.X[data.X>10])
    Yn=np.array(data.Y[data.X>10])
#    Xn=np.empty(len(Xt))
#    for i in range(len(Xt)):
#        if Xt[i] > 10 and Xt[i] < 10:
#            Xn[i]=0
    par,cov=curve_fit(multi_gauss,Xn,Yn)
    xgr= np.linspace(np.amin(data.X),np.amax(data.X),1000)
    plt.plot(xgr,multi_gauss(xgr,*par),color='tomato')

    #print(np.average(data.Y[0:100]))
 

    plt.show()



if __name__ == "__main__":
   main()


