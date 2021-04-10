import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit


filenameCu = 'data_cu_rate.txt'
filenameAg = 'data_ag_rate.txt'


def expFunc(x, a, b):
    return a * np.exp( -b * x) 

def linFunc(x, m):
    return -m*x

# fit given data and return best fit parameters (with errors)
# and residuals.
# choice==0 -> exponential fit
# choice==1 -> linear fit
def fitFunc(X,Y,errY,choice):

    # fit data according to ~choice~

    if choice==0: # exponential fit

        par, cov = curve_fit(f=expFunc, xdata=X, ydata=Y,
                             sigma=errY, absolute_sigma=True
                             )
        
        residuals = np.array(Y) - expFunc(np.array(X), *par)


    elif choice==1: # lienar fit

        par, cov = curve_fit(f=linFunc, xdata=X, ydata=Y,
                             sigma=errY, absolute_sigma=True
                             )

        residuals = np.array(Y) - linFunc(np.array(X), *par)


    chi2 = np.sum((residuals / np.array(errY))**2) 


    # get parameters error from cov matrix
    par_error = np.zeros(len(par))
    for i in range(len(par)):
        try:
            par_error[i] = cov[i][i]**0.5
        except:
            par_error[i] = 0.00


    return par, par_error, chi2, residuals


                            
def makePlot(
                X_Cu, Y_Cu, errY_Cu,
                X_Ag, Y_Ag, errY_Ag,
                par_Cu_exp, residuals_Cu_exp,
                par_Ag_exp, residuals_Ag_exp,
                par_Cu_lin, residuals_Cu_lin,
                par_Ag_lin, residuals_Ag_lin
            ):

    fig, ax = plt.subplots(ncols=2, nrows=2, figsize=(20,9.5),
                           gridspec_kw={'height_ratios': [3, 1]},
                           sharex=True)


    # plot exponential data
    ax[0][0].errorbar(x=X_Cu, y=Y_Cu, yerr=errY_Cu, marker = '.',
                markersize = 15, linewidth = 0, 
                elinewidth = 1.5, capsize = 1.5, capthick = 1.5,
                color = '#0451FF', label = 'Cu Data')

    ax[0][0].errorbar(x=X_Ag, y=Y_Ag, yerr=errY_Ag, marker = '.',
                markersize = 15, linewidth = 0, 
                elinewidth = 1.5, capsize = 1.5, capthick = 1.5,
                color = '#FF4B00', label = 'Ag Data')


    # plot linearized data
    linY_Cu = np.log(Y_Cu/par_Cu_exp[0])
    errLin_Cu = errY_Cu/Y_Cu

    linY_Ag = np.log(Y_Ag/par_Ag_exp[0])
    errLin_Ag = errY_Ag/Y_Ag

    ax[0][1].errorbar(x=X_Cu, y=linY_Cu, yerr=errLin_Cu, marker = '.',
                markersize = 15, linewidth = 0, 
                elinewidth = 1.5, capsize = 1.5, capthick = 1.5,
                color = '#0451FF', label = 'Linearized Cu Data')

    ax[0][1].errorbar(x=X_Ag, y=linY_Ag, yerr=errLin_Ag, marker = '.',
                markersize = 15, linewidth = 0, 
                elinewidth = 1.5, capsize = 1.5, capthick = 1.5,
                color = '#FF4B00', label = 'Linearized Ag Data')


    # plot parameters
    xmin=np.amin(X_Ag)
    xmax=np.amax(X_Cu)

    deltaX = (xmax-xmin)/10 # edit me to change plot ranges!
    xplot=np.linspace(xmin-deltaX,xmax+deltaX)

    # plot exponential fit
    ax[0][0].plot(xplot, expFunc(xplot, *par_Cu_exp), linestyle = '--', linewidth = 2,
               color = '#2a6bff' , label = 'Cu Exponential Fit')
    ax[0][0].plot(xplot, expFunc(xplot, *par_Ag_exp), linestyle = '--', linewidth = 2,
               color = '#ff6626' , label = 'Ag Exponential Fit')

    # plot linear fit
    ax[0][1].plot(xplot, linFunc(xplot, *par_Cu_lin), linestyle = '--', linewidth = 2,
               color = '#2a6bff' , label = 'Cu Linear Fit')
    ax[0][1].plot(xplot, linFunc(xplot, *par_Ag_lin), linestyle = '--', linewidth = 2,
               color = '#ff6626' , label = 'Ag Linear Fit')



    # plot exponential residuals
    ax[1][0].errorbar(x=X_Cu, y=residuals_Cu_exp, yerr=errY_Cu, marker='.',
                   markersize=15, linewidth=0, 
                   elinewidth=1.5, capsize=1.5, capthick = 1.5,
                   color = '#0451FF', label = 'Cu residuals')

    ax[1][0].errorbar(x=X_Ag, y=residuals_Ag_exp, yerr=errY_Ag, marker='.',
                   markersize=15, linewidth=0, 
                   elinewidth=1.5, capsize=1.5, capthick = 1.5,
                   color = '#FF4B00', label = 'Cu residuals')

    # plot linear residuals
    ax[1][1].errorbar(x=X_Cu, y=residuals_Cu_lin, yerr=errLin_Cu, marker='.',
                   markersize=15, linewidth=0, 
                   elinewidth=1.5, capsize=1.5, capthick = 1.5,
                   color = '#0451FF', label = 'Cu residuals')

    ax[1][1].errorbar(x=X_Ag, y=residuals_Ag_lin, yerr=errLin_Ag, marker='.',
                   markersize=15, linewidth=0, 
                   elinewidth=1.5, capsize=1.5, capthick = 1.5,
                   color = '#FF4B00', label = 'Cu residuals')

    ax[1][0].hlines(0, xmin-deltaX, xmax+deltaX, color = '#000000', linestyle = 'dashed', linewidth = 1)
    ax[1][1].hlines(0, xmin-deltaX, xmax+deltaX, color = '#000000', linestyle = 'dashed', linewidth = 1)

    
    # MAKE LEGEND
    handles, labels = ax[0][0].get_legend_handles_labels()
    order = [3, 1, 2, 0]
    ax[0][0].legend([handles[idx] for idx in order], [labels[idx] for idx in order], loc = 'lower left', prop = {'size': 16}, 
                ncol = 2, frameon = True, fancybox = False, framealpha = 0.5)

    handles, labels = ax[0][1].get_legend_handles_labels()
    order = [3, 1, 2, 0]
    ax[0][1].legend([handles[idx] for idx in order], [labels[idx] for idx in order], loc = 'lower left', prop = {'size': 16}, 
                ncol = 2, frameon = True, fancybox = False, framealpha = 0.5)

    # plot title
    fig.suptitle('Event Rate over Absorber Thickness', fontsize = 24)

    # plot ranges
    ax[0][0].set_xlim(xmin-deltaX, xmax+deltaX)
    ax[0][0].set_ylim(0, 8)
    ax[0][1].set_xlim(xmin-deltaX, xmax+deltaX)
    ax[0][1].set_ylim(-2.0, 0)

    # plot labels
    ax[0][0].set_ylabel('Rate [Hz]', fontsize = 20, loc = 'center')
    ax[0][1].set_ylabel('Normalized log(Rate)', fontsize = 20, loc = 'center')
    ax[1][0].set_xlabel('Thickness [cm]', fontsize = 20)
    ax[1][0].set_ylabel('Residuals [Hz]', fontsize = 20, loc = 'center')
    ax[1][1].set_xlabel('Thickness [cm]', fontsize = 20)
    ax[1][1].set_ylabel('Residuals', fontsize = 20, loc = 'center')

    # plot ticks
    ax[0][0].tick_params(axis = 'both', which = 'major', labelsize = 16, direction = 'out', length = 5)
    ax[0][1].tick_params(axis = 'both', which = 'major', labelsize = 16, direction = 'out', length = 5)
    ax[1][0].tick_params(axis = 'both', which = 'major', labelsize = 16, direction = 'out', length = 5)
    ax[1][1].tick_params(axis = 'both', which = 'major', labelsize = 16, direction = 'out', length = 5)


    return fig, ax


def printResults(
                    par_exp_Cu, par_error_exp_Cu, chi2_exp_Cu,
                    par_exp_Ag, par_error_exp_Ag, chi2_exp_Ag,
                    par_lin_Cu, par_error_lin_Cu, chi2_lin_Cu,
                    par_lin_Ag, par_error_lin_Ag, chi2_lin_Ag  
                ):
    
    print('\n========= Exponential Fit Results\n')

    print('I_0 Cu = ' + format(par_exp_Cu[0], '1.2f') + ' +/- ' + format(par_error_exp_Cu[0], '1.2f') + ' Hz')
    print('\u03BC Cu = ' + format(par_exp_Cu[1], '1.2f') + ' +/- ' + format(par_error_exp_Cu[1], '1.2f') + ' 1/cm')
    print('\u03C7^2 / ndf Cu = ' + format(chi2_exp_Cu, '1.2f') + ' / ' + format(4 - len(par_exp_Cu), '1.0f'))
    print('')
    print('I_0 Ag = ' + format(par_exp_Ag[0], '1.2f') + ' +/- ' + format(par_error_exp_Ag[0], '1.2f') + ' Hz')
    print('\u03BC Ag = ' + format(par_exp_Ag[1], '1.2f') + ' +/- ' + format(par_error_exp_Ag[1], '1.2f') + ' 1/cm')
    print('\u03C7^2 / ndf Ag = ' + format(chi2_exp_Ag, '1.2f') + ' / ' + format(4 - len(par_exp_Ag), '1.0f'))


    print('\n========= Linearized Fit Results\n')

    print('\u03BC Cu = ' + format(par_lin_Cu[0], '1.2f') + ' +/- ' + format(par_error_lin_Cu[0], '1.2f') + ' 1/cm')
    print('\u03C7^2 / ndf Cu = ' + format(chi2_lin_Cu, '1.2f') + ' / ' + format(4 - len(par_lin_Cu), '1.0f'))
    print('')
    print('\u03BC Ag = ' + format(par_lin_Ag[0], '1.2f') + ' +/- ' + format(par_error_lin_Ag[0], '1.2f') + ' 1/cm')
    print('\u03C7^2 / ndf Ag = ' + format(chi2_lin_Ag, '1.2f') + ' / ' + format(4 - len(par_lin_Ag), '1.0f'))

    return



def main():

    # read data
    dataCu = pd.read_csv(filenameCu, sep = '\t', header = None,
                         names = ['X','X1', 'Y', 'errY'])
    dataCu['X'] = dataCu['X'] * 1e-4 # um -> cm 

    dataAg = pd.read_csv(filenameAg, sep = '\t', header = None,
                         names = ['X','X1', 'Y', 'errY'])
    dataAg['X'] = dataAg['X'] * 1e-4 # um -> cm 


    # exponential fit data 
    par_exp_Cu, par_error_exp_Cu, chi2_exp_Cu, residuals_exp_Cu = fitFunc(dataCu.X, dataCu.Y, dataCu.errY, 0)
    par_exp_Ag, par_error_exp_Ag, chi2_exp_Ag, residuals_exp_Ag = fitFunc(dataAg.X, dataAg.Y, dataAg.errY, 0)
    
    # linearized fit data
    par_lin_Cu, par_error_lin_Cu, chi2_lin_Cu, residuals_lin_Cu = fitFunc(dataCu.X, np.log(dataCu.Y/par_exp_Cu[0]), dataCu.errY/dataCu.Y, 1)
    par_lin_Ag, par_error_lin_Ag, chi2_lin_Ag, residuals_lin_Ag = fitFunc(dataAg.X, np.log(dataAg.Y/par_exp_Ag[0]), dataAg.errY/dataAg.Y, 1)

    # plot fit
    fig, ax = makePlot(
                        dataCu.X, dataCu.Y, dataCu.errY, 
                        dataAg.X, dataAg.Y, dataAg.errY,
                        par_exp_Cu, residuals_exp_Cu,
                        par_exp_Ag, residuals_exp_Ag,
                        par_lin_Cu, residuals_lin_Cu,
                        par_lin_Ag, residuals_lin_Ag
                    )



    printResults(
                    par_exp_Cu, par_error_exp_Cu, chi2_exp_Cu,
                    par_exp_Ag, par_error_exp_Ag, chi2_exp_Ag,
                    par_lin_Cu, par_error_lin_Cu, chi2_lin_Cu,
                    par_lin_Ag, par_error_lin_Ag, chi2_lin_Ag  
                )

  

    fig.tight_layout()
    # fig.savefig('../Plots/attenuation_coeff.png', dpi = 300, facecolor = 'white')
    plt.show()

    return




if __name__ == "__main__":
   main()


