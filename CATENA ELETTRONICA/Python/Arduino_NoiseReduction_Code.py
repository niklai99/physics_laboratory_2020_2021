# CODE BY NICOLO LAI

# IMPORT MODULES

import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter
import seaborn as sns
import numpy as np
from scipy import stats
from scipy.optimize import curve_fit
from scipy.misc import derivative



####### LINEAR FUCTION
def lin(x, a, b):  
    return a + b * x

####### EXPONENTIAL FUCTION
def esp(x, a, b, c):  
    return a + b * np.exp(- x * c**-1)




####### ARDUINO READ LOW TENSION DATA
def arduino_calib_read_low():
    # READ DATA
    file_in =  '../Data/PreAmp/calib_in_18.txt'
    file_vdiv =  '../Data/PreAmp/calib_in_vdiv_18.txt'
    file1 = '../Data/PreAmp/calib_02_18_ROOT.dat'
    file2 = '../Data/PreAmp/calib_05_18_ROOT.dat'
    file3 = '../Data/PreAmp/calib_08_18_ROOT.dat'
    file4 = '../Data/PreAmp/calib_10_18_ROOT.dat'
    file5 = '../Data/PreAmp/calib_12_18_ROOT.dat'
    file6 = '../Data/PreAmp/calib_15_18_ROOT.dat'
    file7 = '../Data/PreAmp/calib_18_18_ROOT.dat'
    file8 = '../Data/PreAmp/calib_20_18_ROOT.dat'
    file9 = '../Data/PreAmp/calib_21_18_ROOT.dat'
    file10 = '../Data/PreAmp/calib_22_18_ROOT.dat'
    file11 = '../Data/PreAmp/calib_23_18_ROOT.dat'
    file12 = '../Data/PreAmp/calib_24_18_ROOT.dat'
    file13 = '../Data/PreAmp/calib_25_18_ROOT.dat'

    data1 = pd.read_csv(file1, sep = ' ', index_col = False, header = None)
    data1.index = np.arange(1, len(data1)+1)
    data1.columns = ['time', 'ADC']

    data2 = pd.read_csv(file2, sep = ' ', index_col = False, header = None)
    data2.index = np.arange(1, len(data2)+1)
    data2.columns = ['time', 'ADC']

    data3 = pd.read_csv(file3, sep = ' ', index_col = False, header = None)
    data3.index = np.arange(1, len(data3)+1)
    data3.columns = ['time', 'ADC']

    data4 = pd.read_csv(file4, sep = ' ', index_col = False, header = None)
    data4.index = np.arange(1, len(data4)+1)
    data4.columns = ['time', 'ADC']

    data5 = pd.read_csv(file5, sep = ' ', index_col = False, header = None)
    data5.index = np.arange(1, len(data5)+1)
    data5.columns = ['time', 'ADC']

    data6 = pd.read_csv(file6, sep = ' ', index_col = False, header = None)
    data6.index = np.arange(1, len(data6)+1)
    data6.columns = ['time', 'ADC']

    data7 = pd.read_csv(file7, sep = ' ', index_col = False, header = None)
    data7.index = np.arange(1, len(data7)+1)
    data7.columns = ['time', 'ADC']

    data8 = pd.read_csv(file8, sep = ' ', index_col = False, header = None)
    data8.index = np.arange(1, len(data8)+1)
    data8.columns = ['time', 'ADC']

    data9 = pd.read_csv(file9, sep = ' ', index_col = False, header = None)
    data9.index = np.arange(1, len(data9)+1)
    data9.columns = ['time', 'ADC']

    data10 = pd.read_csv(file10, sep = ' ', index_col = False, header = None)
    data10.index = np.arange(1, len(data10)+1)
    data10.columns = ['time', 'ADC']

    data11 = pd.read_csv(file11, sep = ' ', index_col = False, header = None)
    data11.index = np.arange(1, len(data11)+1)
    data11.columns = ['time', 'ADC']

    data12 = pd.read_csv(file12, sep = ' ', index_col = False, header = None)
    data12.index = np.arange(1, len(data12)+1)
    data12.columns = ['time', 'ADC']

    data13 = pd.read_csv(file13, sep = ' ', index_col = False, header = None)
    data13.index = np.arange(1, len(data13)+1)
    data13.columns = ['time', 'ADC']

    # GET MAX VALUES
    max1 = data1['ADC'].max()
    max2 = data2['ADC'].max()
    max3 = data3['ADC'].max()
    max4 = data4['ADC'].max()
    max5 = data5['ADC'].max()
    max6 = data6['ADC'].max()
    max7 = data7['ADC'].max()
    max8 = data8['ADC'].max()
    max9 = data9['ADC'].max()
    max10 = data10['ADC'].max()
    max11 = data11['ADC'].max()
    max12 = data12['ADC'].max()
    max13 = data13['ADC'].max()

    max_values = np.array([max1, max2, max3, max4, max5, max6, max7, max8, max9, max10, max11, max12, max13])

    Vin = np.loadtxt(file_in)
    Vdiv = np.loadtxt(file_vdiv)

    data = pd.DataFrame({'max_values': list(max_values), 'Vin': list(Vin), 'Vdiv': list(Vdiv)}, columns = ['max_values', 'Vin', 'Vdiv'])
    
    data = data.iloc[:3,:]

    return data



####### PROPAGAZIONE SUI CURSORI
def propagazione_cursori(Vdiv, measure):

    sigma = np.sqrt( (0.04 * Vdiv)**2 + (0.015 * measure)**2)

    return sigma



####### ARDUINO PLOT
def arduino_waveform(data):
    # FIG SETTINGS AND AXES
    fig = plt.figure(figsize=(16,8))
    ax1 = fig.add_subplot(1, 1, 1)

    # PLOT DATA
    ax1.plot(data['time (ms)'], data['V (V)'], color = '#227FF7', linewidth = 2, label = 'Data')

    # PLOT TITLE
    ax1.set_title('PreAmp - Arduino Waveform', fontsize = 32)

    # AXIS LABELS
    ax1.set_xlabel('time (ms)', fontsize = 26, loc = 'right')
    ax1.set_ylabel('V (V)', fontsize = 26, loc = 'top')

    # AXIS TICKS
    ax1.tick_params(axis = 'both', which = 'major', labelsize = 22, direction = 'in', length = 10)
    ax1.tick_params(axis = 'both', which = 'minor', labelsize = 22, direction = 'in', length = 5)
    ax1.set_xticks(ticks = ax1.get_xticks(), minor = True)
    ax1.set_yticks(ticks = ax1.get_yticks(), minor = True)
    ax1.minorticks_on()

    # PLOT RANGE
    ax1.set_xlim(left = 0, right = 2.15)
    ax1.set_ylim(bottom = 0, top = 0.42)

    # SAVE FIGURE
    fig.savefig('../Plots/Arduino_NR/preamp_waveform.png', dpi = 300, facecolor = 'white')

    plt.show()



def arduino_waveform_IIR_filter(data):
    # FIG SETTINGS AND AXES
    fig = plt.figure(figsize=(16,8))
    ax1 = fig.add_subplot(1, 1, 1)

    # PLOT DATA
    ax1.plot(data['time (ms)'], data['V (V)'], color = '#227FF7', linewidth = 2, label = 'Unfiltered Data')
    ax1.plot(data['time (ms)'], data['V filter'], color = '#FF4000', linewidth = 2, label = 'Filtered Data')

    # PLOT TITLE
    ax1.set_title('PreAmp - IIR Filtered Arduino Waveform', fontsize = 32)

    # AXIS LABELS
    ax1.set_xlabel('time (ms)', fontsize = 26, loc = 'right')
    ax1.set_ylabel('V (V)', fontsize = 26, loc = 'top')

    # AXIS TICKS
    ax1.tick_params(axis = 'both', which = 'major', labelsize = 22, direction = 'in', length = 10)
    ax1.tick_params(axis = 'both', which = 'minor', labelsize = 22, direction = 'in', length = 5)
    ax1.set_xticks(ticks = ax1.get_xticks(), minor = True)
    ax1.set_yticks(ticks = ax1.get_yticks(), minor = True)
    ax1.minorticks_on()

    # PLOT RANGE
    ax1.set_xlim(left = 0, right = 2.15)
    ax1.set_ylim(bottom = 0, top = 0.42)

    ax1.legend(loc = 'upper right', prop = {'size': 22}, ncol = 1, frameon = True, fancybox = False, framealpha = 1)

    # SAVE FIGURE
    fig.savefig('../Plots/Arduino_NR/preamp_waveform_IIR_filter.png', dpi = 300, facecolor = 'white')

    plt.show()



def arduino_waveform_IIR_filter_peek(data_peek):
    # FIG SETTINGS AND AXES
    fig = plt.figure(figsize=(16,8))
    ax1 = fig.add_subplot(1, 1, 1)

    # PLOT DATA
    ax1.plot(data_peek['time (ms)'], data_peek['V (V)'], color = '#227FF7', linewidth = 2, label = 'Unfiltered Data')
    ax1.plot(data_peek['time (ms)'], data_peek['V filter'], color = '#FF4000', linewidth = 2, label = 'Filtered Data')

    # PLOT TITLE
    ax1.set_title('PreAmp - IIR Filtered Arduino Data', fontsize = 32)

    # AXIS LABELS
    ax1.set_xlabel('time (ms)', fontsize = 26, loc = 'right')
    ax1.set_ylabel('V (V)', fontsize = 26, loc = 'top')

    # AXIS TICKS
    ax1.tick_params(axis = 'both', which = 'major', labelsize = 22, direction = 'in', length = 10)
    ax1.tick_params(axis = 'both', which = 'minor', labelsize = 22, direction = 'in', length = 5)
    ax1.set_xticks(ticks = ax1.get_xticks(), minor = True)
    ax1.set_yticks(ticks = ax1.get_yticks(), minor = True)
    ax1.minorticks_on()

    # PLOT RANGE
    ax1.set_xlim(left = 0.30, right = 1.25)
    ax1.set_ylim(bottom = 0, top = 0.42)

    ax1.legend(loc = 'upper right', prop = {'size': 22}, ncol = 1, frameon = True, fancybox = False, framealpha = 1)

    # SAVE FIGURE
    fig.savefig('../Plots/Arduino_NR/preamp_waveform_IIR_filter_peek.png', dpi = 300, facecolor = 'white')

    plt.show()



def arduino_IIR_exp_fit(data_peek):
    # FIG SETTINGS AND AXES
    fig = plt.figure(figsize=(16,8))

    ax1 = fig.add_subplot(1, 2, 2)
    ax2 = fig.add_subplot(1, 2, 1)

    par, cov = curve_fit(f = esp, xdata = data_peek['time (ms)'], ydata = data_peek['V filter'], maxfev=1000, 
                        p0 = [0.02, 0.6, 0.151], sigma = data_peek['err V (V)'], absolute_sigma = True)

    func = esp(data_peek['time (ms)'], *par)

    par2, cov2 = curve_fit(f = esp, xdata = data_peek['time (ms)'], ydata = data_peek['V (V)'], maxfev=1000, 
                        p0 = [0.02, 0.6, 0.151], sigma = data_peek['err V (V)'], absolute_sigma = True)

    func2 = esp(data_peek['time (ms)'], *par2)

    # GET FIT PARAMETERS AND PARAMETER ERRORS
    error = []
    for i in range(len(par)):
        try:
            error.append(np.absolute(cov[i][i])**0.5)
        except:
            error.append( 0.00 )

    fit_par = par
    fit_err = np.array(error)

    a = fit_par[0]
    b = fit_par[1]
    tau = fit_par[2]
    a_err = fit_err[0]
    b_err = fit_err[1]
    tau_err = fit_err[2]

    error2 = []
    for i in range(len(par2)):
        try:
            error2.append(np.absolute(cov2[i][i])**0.5)
        except:
            error2.append( 0.00 )

    fit_par2 = par2
    fit_err2 = np.array(error2)

    a2 = fit_par2[0]
    b2 = fit_par2[1]
    tau2 = fit_par2[2]
    err_a2 = fit_err2[0]
    err_b2 = fit_err2[1]
    err_tau2 = fit_err2[2]

    # PLOT DATA
    ax1.plot(data_peek['time (ms)'], data_peek['V filter'], color = '#227FF7', linewidth = 2, label = 'Data')
    ax1.plot(data_peek['time (ms)'], func, color = '#FF4B00', linewidth = 2, linestyle = 'dashed', label = 'Fit')

    ax2.plot(data_peek['time (ms)'], data_peek['V (V)'], color = '#227FF7', linewidth = 2, label = 'Data')
    ax2.plot(data_peek['time (ms)'], func2, color = '#FF4B00', linewidth = 2, linestyle = 'dashed', label = 'Fit')

    aa = 'a = ' + format(a, '1.4f') + ' +/- ' + format(a_err, '1.4f') + '  V'
    bb = 'b = ' + format(b, '1.2f') + ' +/- ' + format(b_err, '1.2f')
    cc = '\u03C4 = ' + format(tau * 1e3, '1.2f') + ' +/- ' + format(tau_err * 1e3, '1.2f') + '  \u03BCs'

    aa2 = 'a = ' + format(a2, '1.4f') + ' +/- ' + format(err_a2, '1.4f') + '  V'
    bb2 = 'b = ' + format(b2, '1.2f') + ' +/- ' + format(err_b2, '1.2f')
    cc2 = '\u03C4 = ' + format(tau2 * 1e3, '1.2f') + ' +/- ' + format(err_tau2 * 1e3, '1.2f') + '  \u03BCs'

    ax1.text(0.15, 0.90, 'Fit Function', fontsize = 28, fontweight = 'bold', transform=ax1.transAxes)
    ax1.text(0.19, 0.83, 'y = a + b * exp(-x / \u03C4)', fontsize = 26, color = '#000000', transform = ax1.transAxes)
    ax1.text(0.28, 0.35, aa + '\n' + bb + '\n' + cc, fontsize = 22, color = '#000000', transform = ax1.transAxes)

    ax2.text(0.15, 0.90, 'Fit Function', fontsize = 28, fontweight = 'bold', transform=ax2.transAxes)
    ax2.text(0.19, 0.83, 'y = a + b * exp(-x / \u03C4)', fontsize = 26, color = '#000000', transform = ax2.transAxes)
    ax2.text(0.28, 0.35, aa2 + '\n' + bb2 + '\n' + cc2, fontsize = 22, color = '#000000', transform = ax2.transAxes)

    # PLOT TITLE
    ax1.set_title('IIR Filtered Data', fontsize = 32)
    ax2.set_title('Unfiltered Data', fontsize = 32)
    #fig.suptitle('PreAmp - Arduino ExpFit', fontsize = 36, y = 1.01)

    # AXIS LABELS
    ax1.set_xlabel('time (ms)', fontsize = 26, loc = 'right')
    ax1.set_ylabel('V (V)', fontsize = 26, loc = 'top', labelpad = -5)
    ax2.set_xlabel('time (ms)', fontsize = 26, loc = 'right')
    ax2.set_ylabel('V (V)', fontsize = 26, loc = 'top', labelpad = -5)

    # AXIS TICKS
    ax1.tick_params(axis = 'both', which = 'major', labelsize = 22, direction = 'in', length = 10)
    ax1.tick_params(axis = 'both', which = 'minor', labelsize = 22, direction = 'in', length = 5)
    ax1.set_xticks(ticks = ax1.get_xticks(), minor = True)
    ax1.set_yticks(ticks = ax1.get_yticks(), minor = True)
    ax1.minorticks_on()
    ax2.tick_params(axis = 'both', which = 'major', labelsize = 22, direction = 'in', length = 10)
    ax2.tick_params(axis = 'both', which = 'minor', labelsize = 22, direction = 'in', length = 5)
    ax2.set_xticks(ticks = ax1.get_xticks(), minor = True)
    ax2.set_yticks(ticks = ax1.get_yticks(), minor = True)
    ax2.minorticks_on()

    # PLOT RANGE
    ax1.set_xlim(left = 0.30, right = 1.25)
    ax1.set_ylim(bottom = 0, top = 0.42)
    ax2.set_xlim(left = 0.30, right = 1.25)
    ax2.set_ylim(bottom = 0, top = 0.42)

    # SAVE FIGURE
    fig.savefig('../Plots/Arduino_NR/preamp_IIR_expfit.png', dpi = 300, facecolor = 'white')

    plt.show()


def arduino_waveform_BUTTER_filter_peek(data_peek):
    # FIG SETTINGS AND AXES
    fig = plt.figure(figsize=(16,8))
    ax1 = fig.add_subplot(1, 1, 1)

    # PLOT DATA
    ax1.plot(data_peek['time (ms)'], data_peek['V (V)'], color = '#227FF7', linewidth = 2, label = 'Unfiltered Data')
    ax1.plot(data_peek['time (ms)'], data_peek['V filter2'], color = '#FF4000', linewidth = 2, label = 'Filtered Data')

    # PLOT TITLE
    ax1.set_title('PreAmp - BUTTER Filtered Arduino Data', fontsize = 32)

    # AXIS LABELS
    ax1.set_xlabel('time (ms)', fontsize = 26, loc = 'right')
    ax1.set_ylabel('V (V)', fontsize = 26, loc = 'top')

    # AXIS TICKS
    ax1.tick_params(axis = 'both', which = 'major', labelsize = 22, direction = 'in', length = 10)
    ax1.tick_params(axis = 'both', which = 'minor', labelsize = 22, direction = 'in', length = 5)
    ax1.set_xticks(ticks = ax1.get_xticks(), minor = True)
    ax1.set_yticks(ticks = ax1.get_yticks(), minor = True)
    ax1.minorticks_on()

    # PLOT RANGE
    ax1.set_xlim(left = 0.30, right = 1.25)
    ax1.set_ylim(bottom = 0, top = 0.42)

    ax1.legend(loc = 'upper right', prop = {'size': 22}, ncol = 1, frameon = True, fancybox = False, framealpha = 1)

    # SAVE FIGURE
    fig.savefig('../Plots/Arduino_NR/preamp_waveform_BUTTER_filter_peek.png', dpi = 300, facecolor = 'white')

    plt.show()



def arduino_BUTTER_exp_fit(data_peek):
    # FIG SETTINGS AND AXES
    fig = plt.figure(figsize=(16,8))

    ax1 = fig.add_subplot(1, 2, 2)
    ax2 = fig.add_subplot(1, 2, 1)

    par, cov = curve_fit(f = esp, xdata = data_peek['time (ms)'], ydata = data_peek['V filter2'], maxfev=1000, 
                        p0 = [0.02, 0.6, 0.151], sigma = data_peek['err V (V)'], absolute_sigma = True)

    func = esp(data_peek['time (ms)'], *par)

    par2, cov2 = curve_fit(f = esp, xdata = data_peek['time (ms)'], ydata = data_peek['V (V)'], maxfev=1000, 
                        p0 = [0.02, 0.6, 0.151], sigma = data_peek['err V (V)'], absolute_sigma = True)

    func2 = esp(data_peek['time (ms)'], *par2)

    # GET FIT PARAMETERS AND PARAMETER ERRORS
    error = []
    for i in range(len(par)):
        try:
            error.append(np.absolute(cov[i][i])**0.5)
        except:
            error.append( 0.00 )

    fit_par = par
    fit_err = np.array(error)

    a = fit_par[0]
    b = fit_par[1]
    tau = fit_par[2]
    a_err = fit_err[0]
    b_err = fit_err[1]
    tau_err = fit_err[2]

    error2 = []
    for i in range(len(par2)):
        try:
            error2.append(np.absolute(cov2[i][i])**0.5)
        except:
            error2.append( 0.00 )

    fit_par2 = par2
    fit_err2 = np.array(error2)

    a2 = fit_par2[0]
    b2 = fit_par2[1]
    tau2 = fit_par2[2]
    err_a2 = fit_err2[0]
    err_b2 = fit_err2[1]
    err_tau2 = fit_err2[2]

    # PLOT DATA
    ax1.plot(data_peek['time (ms)'], data_peek['V filter2'], color = '#227FF7', linewidth = 2, label = 'Data')
    ax1.plot(data_peek['time (ms)'], func, color = '#FF4B00', linewidth = 2, linestyle = 'dashed', label = 'Fit')

    ax2.plot(data_peek['time (ms)'], data_peek['V (V)'], color = '#227FF7', linewidth = 2, label = 'Data')
    ax2.plot(data_peek['time (ms)'], func2, color = '#FF4B00', linewidth = 2, linestyle = 'dashed', label = 'Fit')

    aa = 'a = ' + format(a, '1.4f') + ' +/- ' + format(a_err, '1.4f') + '  V'
    bb = 'b = ' + format(b, '1.2f') + ' +/- ' + format(b_err, '1.2f')
    cc = '\u03C4 = ' + format(tau * 1e3, '1.2f') + ' +/- ' + format(tau_err * 1e3, '1.2f') + '  \u03BCs'

    aa2 = 'a = ' + format(a2, '1.4f') + ' +/- ' + format(err_a2, '1.4f') + '  V'
    bb2 = 'b = ' + format(b2, '1.2f') + ' +/- ' + format(err_b2, '1.2f')
    cc2 = '\u03C4 = ' + format(tau2 * 1e3, '1.2f') + ' +/- ' + format(err_tau2 * 1e3, '1.2f') + '  \u03BCs'

    ax1.text(0.15, 0.90, 'Fit Function', fontsize = 28, fontweight = 'bold', transform=ax1.transAxes)
    ax1.text(0.19, 0.83, 'y = a + b * exp(-x / \u03C4)', fontsize = 26, color = '#000000', transform = ax1.transAxes)
    ax1.text(0.28, 0.35, aa + '\n' + bb + '\n' + cc, fontsize = 22, color = '#000000', transform = ax1.transAxes)

    ax2.text(0.15, 0.90, 'Fit Function', fontsize = 28, fontweight = 'bold', transform=ax2.transAxes)
    ax2.text(0.19, 0.83, 'y = a + b * exp(-x / \u03C4)', fontsize = 26, color = '#000000', transform = ax2.transAxes)
    ax2.text(0.28, 0.35, aa2 + '\n' + bb2 + '\n' + cc2, fontsize = 22, color = '#000000', transform = ax2.transAxes)

    # PLOT TITLE
    ax1.set_title('BUTTER Filtered Data', fontsize = 32)
    ax2.set_title('Unfiltered Data', fontsize = 32)
    #fig.suptitle('PreAmp - Arduino ExpFit', fontsize = 36, y = 1.01)

    # AXIS LABELS
    ax1.set_xlabel('time (ms)', fontsize = 26, loc = 'right')
    ax1.set_ylabel('V (V)', fontsize = 26, loc = 'top', labelpad = -5)
    ax2.set_xlabel('time (ms)', fontsize = 26, loc = 'right')
    ax2.set_ylabel('V (V)', fontsize = 26, loc = 'top', labelpad = -5)

    # AXIS TICKS
    ax1.tick_params(axis = 'both', which = 'major', labelsize = 22, direction = 'in', length = 10)
    ax1.tick_params(axis = 'both', which = 'minor', labelsize = 22, direction = 'in', length = 5)
    ax1.set_xticks(ticks = ax1.get_xticks(), minor = True)
    ax1.set_yticks(ticks = ax1.get_yticks(), minor = True)
    ax1.minorticks_on()
    ax2.tick_params(axis = 'both', which = 'major', labelsize = 22, direction = 'in', length = 10)
    ax2.tick_params(axis = 'both', which = 'minor', labelsize = 22, direction = 'in', length = 5)
    ax2.set_xticks(ticks = ax1.get_xticks(), minor = True)
    ax2.set_yticks(ticks = ax1.get_yticks(), minor = True)
    ax2.minorticks_on()

    # PLOT RANGE
    ax1.set_xlim(left = 0.30, right = 1.25)
    ax1.set_ylim(bottom = 0, top = 0.42)
    ax2.set_xlim(left = 0.30, right = 1.25)
    ax2.set_ylim(bottom = 0, top = 0.42)

    # SAVE FIGURE
    fig.savefig('../Plots/Arduino_NR/preamp_BUTTER_expfit.png', dpi = 300, facecolor = 'white')

    plt.show()