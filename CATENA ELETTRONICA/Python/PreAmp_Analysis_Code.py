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

### ------------------------------------ COMPONENTI CIRCUITALI ------------------------------------

# Misure Dirette
Rin = 56564 #Ohm
Rf = 696060 #Ohm
Cf = 0.000000000232 #Farad

# Fondo Scala
FS_Rin = 100000 #Ohm
FS_Rf = 1000000 #Ohm
FS_Cf = 0.000000001 #Farad

# Multimetro Metrix
## FS 100kOhm   -> 0.07% + 8    -> Risoluzione 1Ohm
## FS 1000kOhm  -> 0.07% + 8    -> Risoluzione 10Ohm
## FS 1000pF    -> 2.5%  + 15   -> Risoluzione 1pF
L_Rin = 0.07 / 100
L_Rf = 0.07 / 100
L_Cf = 2.5 / 100
D_Rin = 8
D_Rf = 8
D_Cf = 15
Res_Rin = 1
Res_Rf = 10
Res_Cf = 1e-12

sigma_L_Rin = 0.58 * L_Rin * Rin
sigma_L_Rf = 0.58 * L_Rf * Rf
sigma_L_Cf = 0.58 * L_Cf * Cf
sigma_D_Rin = 0.58 * D_Rin * Res_Rin
sigma_D_Rf = 0.58 * D_Rf * Res_Rf
sigma_D_Cf = 0.58 * D_Cf * Res_Cf

sigma_Rin = np.sqrt(sigma_L_Rin**2 + sigma_D_Rin**2)
sigma_Rf = np.sqrt(sigma_L_Rf**2 + sigma_D_Rf**2)
sigma_Cf = np.sqrt(sigma_L_Cf**2 + sigma_D_Cf**2)

### ------------------------------------ ------------------- --------------------------------------

### ------------------------------------- MISURE SPERIMENTALI -------------------------------------

#Generatore
T_init = 0.000005 #Secondi
Vlow_sper = 0.008 #Volt
Vhigh_sper = -1.01 #Volt
V_amplitude = np.abs(Vlow_sper - Vhigh_sper)
sigma_V_amplitude = 0.018908646170469

#Valori Sperimentali
Vmax_sper = 0.392 #Volt
Vdiv_Vmax_sper = 0.1 #Volt/div
sigma_Vmax_sper = 0.007111568040875373 #Volt

tau_sper = 158 #MicroSecondi us ~circa



### ------------------------------------ ------------------- --------------------------------------

### ---------------------------------------- STIME TEORICHE ---------------------------------------

Qth : float
sigma_Qth : float

tau_th : float
sigma_tau_th : float
ft_th : float
sigma_ft_th : float

Vmax_th : float
sigma_Vmax_th : float

Cf_fit : float
sigma_Cf_fit : float

I = V_amplitude / Rin
sigma_I = np.sqrt( (sigma_V_amplitude / Rin)**2 + (V_amplitude * sigma_Rin / Rin**2)**2 )

### ------------------------------------ ------------------- --------------------------------------

### ---------------------------------------- FIT PARAMETERS ---------------------------------------

a : float
b : float
err_a : float
err_b : float

c : float
d : float
err_c : float
err_d : float

e : float
f : float
err_e : float
err_f : float

### ------------------------------------ ------------------- --------------------------------------

### ------------------------------------------ STIME BODE -----------------------------------------

ft_bode : float
sigma_ft_bode : float
tau_bode : float
sigma_tau_bode : float

### ------------------------------------ ------------------- --------------------------------------

### ------------------------------------- CALIBRAZIONE ARDUINO ------------------------------------

arduino_calib_offset : float
arduino_calib_slope : float
arduino_calib_offset_err : float
arduino_calib_slope_err : float

### ------------------------------------ ------------------- --------------------------------------

### ------------------------------------- EXPFIT ARDUINO ------------------------------------

arduino_exp_a    : float
arduino_exp_b    : float
arduino_exp_tau  : float

arduino_exp_a_err   : float
arduino_exp_b_err   : float
arduino_exp_tau_err : float


### ------------------------------------ ------------------- --------------------------------------




### ------------------------------------ ------------------- --------------------------------------
### ------------------------------------ ------------------- --------------------------------------
### ------------------------------------------ FUNCTIONS ------------------------------------------
### ------------------------------------ ------------------- --------------------------------------
### ------------------------------------ ------------------- --------------------------------------


####### MISURE DIRETTE DELLE COMPONENTI CIRCUITALI
def misure_dirette():

    data = {'Valore' : [format(Rin * 1e-3, '1.3f') + ' k\u03A9', format(Rf * 1e-3, '1.2f') + ' k\u03A9', format(Cf * 1e12, '1.0f') + ' pF'], 
            'Errore' : [format(sigma_Rin * 1e-3, '1.3f') + ' k\u03A9', format(sigma_Rf * 1e-3, '1.2f') + ' k\u03A9', format(sigma_Cf * 1e12, '1.0f') + ' pF'],
             'FS' : [format(FS_Rin * 1e-3, '1.0f') + ' k\u03A9', format(FS_Rf * 1e-3, '1.0f') + ' k\u03A9', format(FS_Cf * 1e12, '1.0f') + ' pF']}
    
    df = pd.DataFrame(data = data, index = ['Rin', 'Rf', 'Cf'])

    return df



####### PROPAGAZIONE SUI CURSORI
def propagazione_cursori(Vdiv, measure):

    sigma = np.sqrt( (0.04 * Vdiv)**2 + (0.015 * measure)**2)

    return sigma



####### STIMA TEORICA DELLA CARICA
def carica_teorica():

    global Qth
    global sigma_Qth

    Qth = T_init * V_amplitude / Rin
    sigma_Qth = T_init * np.sqrt( (sigma_V_amplitude / Rin)**2 + (V_amplitude * sigma_Rin / Rin**2)**2 )

    print('Q_th =  ' + format(Qth * 1e12, '1.3f') + ' +/- ' + format(sigma_Qth * 1e12, '1.3f') + '  pC')



####### STIMA TEORICA DEL TEMPO CARATTERISTICO
def tau_teorico():

    global tau_th
    global sigma_tau_th
    global ft_th
    global sigma_ft_th

    tau_th = Rf * Cf
    sigma_tau_th = np.sqrt( (Cf * sigma_Rf)**2 + (Rf * sigma_Cf)**2 )

    ft_th = ( 2 * np.pi )**-1 * tau_th**-1
    sigma_ft_th = ( 2 * np.pi )**-1 * sigma_tau_th * tau_th**-2

    print('\u03C4_th =  ' + format(tau_th * 1e6, '1.3f') + ' +/- ' + format(sigma_tau_th * 1e6, '1.3f') + '  \u03BCs')



####### STIMA TEORICA DI VMAX
def Vmax_teorico():

    global Vmax_th
    global sigma_Vmax_th

    Vmax_th = Qth / Cf
    sigma_Vmax_th = np.sqrt( (sigma_Qth / Cf)**2 + (Qth * sigma_Cf / Cf**2)**2 )

    print('Vmax_th =  ' + format(Vmax_th * 1e3, '1.3f') + ' +/- ' + format(sigma_Vmax_th * 1e3, '1.3f') + '  mV')


####### READ DATA
def get_data(file_name):

    df = pd.read_csv(file_name, index_col = False, header = None, sep = '\t')
    df.index = np.arange(1, len(df)+1)

    return df



####### LINEAR FUCTION
def lin(x, a, b):  
    return a + b * x

####### EXPONENTIAL FUCTION
def esp(x, a, b, c):  
    return a + b * np.exp(- x * c**-1)
    


####### PRE-AMP LINEAR FIT
def preamp_lin_fit(df):

    global a
    global b
    global err_a
    global err_b

    # CONSTANTS
    XMIN = 30
    XMAX = 185
    YMIN = 0.12
    YMAX = 0.82
    RESXMIN = XMIN
    RESXMAX = XMAX
    RESYMIN = -0.03
    RESYMAX = 0.03

    # FIG SETTINGS AND AXES
    fig = plt.figure(figsize=(16,8))
    ax1 = fig.add_subplot(1, 2, 1)
    ax2 = fig.add_subplot(1, 2, 2)

    # PERFORM THE FIT
    par_lin, cov_lin = curve_fit(f = lin, xdata = df['Qin (pC)'], ydata = df['Vmax (V)'], sigma = df['sigma Vmax (V)'], absolute_sigma = True)
    func = lin(df['Qin (pC)'], *par_lin)

    # COMPUTE RESIDUALS
    res = df['Vmax (V)'] - func

    # COMPUTE CHI2
    chi2 = np.sum((res/df['sigma Vmax (V)'])**2)

    # GET FIT PARAMETERS AND PARAMETER ERRORS
    error = []

    for i in range(len(par_lin)):
        try:
            error.append(np.absolute(cov_lin[i][i])**0.5)
        except:
            error.append( 0.00 )

    fit_par = par_lin
    fit_err = np.array(error)

    a = fit_par[0]
    b = fit_par[1]
    err_a = fit_err[0]
    err_b = fit_err[1]

    # COMPUTE SIGMA_POST
    sigma_post = np.sqrt( np.sum( res**2 ) / (len(df['Qin (pC)']) - 2) ) 

    # PLOT DATA
    ax1.errorbar(df['Qin (pC)'], df['Vmax (V)'], xerr = 0, yerr = df['sigma Vmax (V)'], marker = '.', markersize = 13,
                elinewidth=1, color = '#000000', linewidth=0, capsize=2, label = 'Data')

    # PLOT FIT FUNCTION
    ax1.plot(np.arange(XMIN, XMAX + 1, 1), lin(np.arange(XMIN, XMAX + 1, 1), *par_lin), color = '#FF4B00', linewidth = 2, 
            linestyle = '-', label = 'Fit')

    # DRAW DASHED 'ZERO' LINE
    ax2.axhline(color = '#000000', linewidth = 0.5, linestyle = 'dashed')

    # DRAW RESIDUALS
    ax2.errorbar(df['Qin (pC)'], res, xerr=0, yerr=df['sigma Vmax (V)'], marker = '.', markersize = 13, 
                elinewidth=1, color = '#000000', linewidth=0, capsize=2, label = 'Residuals')

    # PRINT FIT RESULTS ON THE PLOT
    q = 'a = ' + format(a, '1.3f') + ' V +/- ' + format(err_a, '1.3f') + ' V'
    m = 'b = ' + format(b * 1e3, '1.2f') + ' +/- ' + format(err_b * 1e3, '1.2f') + ' nF$^{-1}$'
    chisq = '$\chi^{2}$ / ndf = ' + format(chi2, '1.2f') + ' / ' + format(len(df['Qin (pC)']) - len(par_lin), '1.0f') 
    sigmap = '\u03C3$_{post}$ = ' + format(sigma_post, '1.3f') + ' V'

    ax1.text(0.15, 0.85, 'Fit Function', fontsize = 22, fontweight = 'bold', transform=ax1.transAxes)
    ax1.text(0.20, 0.80, 'y = a + bx', fontsize = 18, transform=ax1.transAxes)

    ax1.text(0.45, 0.35, 'Fit Parameters', fontsize = 22, fontweight = 'bold', transform=ax1.transAxes)
    ax1.text(0.45, 0.28, q, fontsize = 18, transform=ax1.transAxes)
    ax1.text(0.45, 0.22, m, fontsize = 18, transform=ax1.transAxes)
    ax1.text(0.45, 0.16, chisq, fontsize = 18, transform=ax1.transAxes)
    ax1.text(0.45, 0.10, sigmap, fontsize = 18, transform=ax1.transAxes)

    # PLOT TITLE
    fig.suptitle('PreAmp - $V_{max}$ vs $Q_{in}$ Plot', fontsize=32)

    # AXIS LABELS
    ax1.set_xlabel('$Q_{in}$ (pC)', fontsize = 24, loc = 'right')
    ax1.set_ylabel('$V_{max}$ (V)', fontsize = 24, loc = 'top', labelpad=0)
    ax2.set_xlabel('$Q_{in}$ (pC)', fontsize = 24, loc = 'right')
    ax2.set_ylabel('$V_{max}$ - fit (V)', fontsize = 24, loc = 'top', labelpad=-15)

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
    ax2.yaxis.set_major_formatter(ScalarFormatter(useMathText=True))
    ax2.yaxis.get_offset_text().set_fontsize(22)
    ax2.ticklabel_format(axis = 'y', style = 'scientific', scilimits = (0, 0))

    # PLOT RANGE
    ax1.set_xlim(left = XMIN, right = XMAX)
    ax1.set_ylim(bottom = YMIN, top = YMAX)
    ax2.set_xlim(left = RESXMIN, right = RESXMAX)
    ax2.set_ylim(bottom = RESYMIN, top = RESYMAX)

    # SAVE FIGURE
    #fig.savefig('../Plots/PreAmp/Vmax_Qin_lin_fit.png', dpi = 300, facecolor='white')

    plt.show()



##### CALCOLO CF DAL FIT
def compute_Cf_fit():

    global Cf_fit
    global sigma_Cf_fit
    global b
    global err_b

    Cf_fit = b**-1


    sigma_Cf_fit = np.sqrt( ( err_b / b**2 )**2 + 2 * ( sigma_I / ( b * I ) )**2 )
    #sigma_Cf_fit = np.sqrt( ( I * err_b / b**2 )**2 + ( sigma_I / b )**2 )

    #sigma_Cf_fit = np.sqrt( (err_b / b**2)**2 + (0.015 / b)**2 )

    print('Cf_fit = ' + format(Cf_fit, '1.5f') + ' +/- ' + format(sigma_Cf_fit, '1.5f') + '  pF')



##### CALCOLO COMPATIBILITA
def compatib(x, y, errx, erry):

    comp = np.abs( x - y ) / np.sqrt( errx**2 + erry**2 )

    return comp



##### PROPAGAZIONE FUNZIONE DI TRASFERIMENTO
def propagazione_T(T, Vin, Vout, Vdivin, Vdivout):

    sigmaL = 0.040
    sigmaK = 0.015

    sigma = T * np.sqrt( (sigmaL * Vdivin / Vin)**2 + (sigmaL * Vdivout / Vout)**2 + 2 * (sigmaK)**2)

    return sigma



##### PROPAGAZIONE FUNZIONE DI TRASFERIMENTO SENZA CONTRIBUTO DI SCALA
def propagazione_Tr(T, Vin, Vout, Vdivin, Vdivout):

    sigmaL = 0.040

    sigma = T * np.sqrt( (sigmaL * Vdivin / Vin)**2 + (sigmaL * Vdivout / Vout)**2)

    return sigma



####### PRE-AMP BODE PLOT
def preamp_bode_plot(df, sim):

    global c 
    global d 
    global err_c 
    global err_d 
    
    global e 
    global f
    global err_e 
    global err_f

    global ft_bode
    global sigma_ft_bode

    # CONSTANTS
    XMIN = 8
    XMAX = 1.2 * 1e6
    YMIN = -42
    YMAX = 30

    RESXMIN = XMIN
    RESXMAX = XMAX
    RESYMIN = -0.3
    RESYMAX = 0.4

    # ARANCIONE
    data1 = df.iloc[:3, :]

    # BLU
    data2 = df.iloc[6:-2, :]

    # FIG SETTINGS AND AXES
    fig = plt.figure(figsize=(16,10))
    ax1 = plt.subplot2grid((10, 1), (0, 0), rowspan=8, colspan=1)
    ax2 = plt.subplot2grid((10, 1), (8, 0), rowspan=2, colspan=1)

    # PERFORM THE FITS

    # ARANCIONE
    par1, cov1 = curve_fit(f = lin, xdata = data1['log10f (dec)'], ydata = data1['H (dB)'], sigma = data1['sigma Hr (dB)'], absolute_sigma = True)
    func1 = lin(df['log10f (dec)'], *par1)

    # BLU
    par2, cov2 = curve_fit(f = lin, xdata = data2['log10f (dec)'], ydata = data2['H (dB)'], sigma = data2['sigma Hr (dB)'], absolute_sigma = True)
    func2 = lin(df['log10f (dec)'], *par2)

    # GET FIT PARAMETERS AND PARAMETER ERRORS
    error1 = []
    error2 = []

    # ARANCIONE
    for i in range(len(par1)):
        try:
            error1.append(np.absolute(cov1[i][i])**0.5)
        except:
            error1.append( 0.00 )

    # BLU
    for i in range(len(par2)):
        try:
            error2.append(np.absolute(cov2[i][i])**0.5)
        except:
            error2.append( 0.00 )

    # ARANCIONE
    fit_par1 = par1
    fit_err1 = np.array(error1)

    # BLU
    fit_par2 = par2
    fit_err2 = np.array(error2)

    # ARANCIONE
    c = fit_par1[0]
    d = fit_par1[1]
    err_c = fit_err1[0]
    err_d = fit_err1[1]

    # BLU
    e = fit_par2[0]
    f = fit_par2[1]
    err_e = fit_err2[0]
    err_f = fit_err2[1]

    # COMPUTE RESIDUALS

    # ARANCIONE
    res1 = data1['H (dB)'] - lin(data1['log10f (dec)'], c, d)

    # BLU
    res2 = data2['H (dB)'] - lin(data2['log10f (dec)'], e, f)

    # COMPUTE CHI2

    # ARANCIONE
    chi21 = np.sum((res1/data1['sigma Hr (dB)'])**2)

    # BLU
    chi22 = np.sum((res2/data2['sigma Hr (dB)'])**2)

    # COMPUTE SIGMA_POST

    # ARANCIONE
    sigma_post1 = np.sqrt( np.sum( res1**2 ) / (len(data1['log10f (dec)']) - 2) )

    # BLU
    sigma_post2 = np.sqrt( np.sum( res2**2 ) / (len(data2['log10f (dec)']) - 2) )

    # COMPUTE DERIVATIVES
    def xc(x):
        return (e - x) / (d - f)
    derc = derivative(xc, c, dx=1e-8)

    def xd(x):
        return (e - c) / (x - f)
    derd = derivative(xd, d, dx=1e-8)

    def xe(x):
        return (x - c) / (d - f)
    dere = derivative(xe, e, dx=1e-8)

    def xf(x):
        return (e - c) / (d - x)
    derf = derivative(xf, f, dx=1e-8)

    #print(format(derc, '1.3f'))
    #print(format(derd, '1.3f'))
    #print(format(dere, '1.3f'))
    #print(format(derf, '1.3f'))

    # COMPUTE X AND Y INTERSECTION
    x_int = (e - c) / (d - f)
    sigma_x_int = np.sqrt( (derc * err_c)**2 +  (derd * err_d)**2 + (dere * err_e)**2 + (derf * err_f)**2 +
                            2 * derc * derd * cov1[0][1] + 2 * dere * derf * cov2[0][1] )

    #print(format(x_int, '1.3f'))
    #print(format(sigma_x_int, '1.3f'))

    ft_bode = 10**x_int
    sigma_ft_bode  = sigma_x_int * 10**x_int * np.log(10)

    y_int = lin(x_int, *par1)

    # PLOT DATA
    ax1.errorbar(df['freq (Hz)'], df['H (dB)'], xerr = 0, yerr = df['sigma Hr (dB)'], marker = '.', markersize = 13,
                elinewidth=1, color = '#000000', linewidth=0, capsize=2, label = 'Measures')
    
    # PLOT SIMULATIONS
    ax1.plot(10**sim['f'], sim['H'], color = '#4b00ff', linewidth = 1, linestyle = '-', label = 'Simulation')

    # PLOT FIT FUNCTIONS
    ax1.plot(np.arange(XMIN, XMAX + 1, 1), lin(np.log10(np.arange(XMIN, XMAX+1, 1)), *par1), color = '#FF4B00', linewidth = 2, linestyle = 'dashed', label = 'y = c + dx')
    ax1.plot(np.arange(XMIN, XMAX + 1, 1), lin(np.log10(np.arange(XMIN, XMAX+1, 1)), *par2), color = '#00b4ff', linewidth = 2, linestyle = 'dashed', label = 'y = a + bx')

    # DRAW INTERSECTION LINE
    # ax1.vlines(x = x_int, ymin = YMIN, ymax = y_int, color = '#000000', linestyle = 'dotted')

    # PRINT FIT RESULTS ON THE PLOT

    # BLU
    q2 = 'a = ' + format(e, '1.1f') + ' +/- ' + format(err_e, '1.1f') + ' dB'
    m2 = 'b = ' + format(f, '1.2f') + ' +/- ' + format(err_f, '1.2f') + ' dB/dec'
    chisq2 = '$\chi^{2}$ / ndf = ' + format(chi22, '1.0f') + ' / ' + format(len(data2['log10f (dec)']) - 2, '1.0f') 
    sigmap2 = '\u03C3$_{post}$ = ' + format(sigma_post2, '1.2f') + ' dB'

    # ARANCIONE
    q1 = 'c = ' + format(c, '1.1f') + ' +/- ' + format(err_c, '1.1f') + ' dB'
    m1 = 'd = ' + format(d, '1.2f') + ' +/- ' + format(err_d, '1.2f') + ' dB/dec'
    chisq1 = '$\chi^{2}$ / ndf = ' + format(chi21, '1.2f') + ' / ' + format(len(data1['log10f (dec)']) - 2, '1.0f') 
    sigmap1 = '\u03C3$_{post}$ = ' + format(sigma_post1, '1.2f') + ' dB'


    ax1.text(0.05, 0.75, 'Fit Parameters', fontsize = 22, fontweight = 'bold', transform=ax1.transAxes)

    # ARANCIONE
    ax1.text(0.05, 0.26, q1 + '\n' + m1 + '\n' + chisq1 + '\n' + sigmap1, fontsize = 18, color = '#000000', transform = ax1.transAxes, 
            bbox = dict( facecolor = '#FF4B00', edgecolor = '#FF4B00', alpha = 0.1, linewidth = 2 ))

    # BLU        
    ax1.text(0.05, 0.50, q2 + '\n' + m2 + '\n' + chisq2 + '\n' + sigmap2, fontsize = 18, color = '#000000', transform = ax1.transAxes, 
            bbox = dict( facecolor = '#00b4ff', edgecolor = '#00b4ff', alpha = 0.1, linewidth = 2 ))

    # DRAW RESIDUALS

    # ARANCIONE
    ax2.errorbar(data1['freq (Hz)'], res1, xerr = 0, yerr = data1['sigma Hr (dB)'], marker = '.', markersize = 13,
                elinewidth=1, color = '#000000', ecolor = '#FF4B00', linewidth=0, capsize=2, label = 'Measures')

    # BLU 
    ax2.errorbar(data2['freq (Hz)'], res2, xerr = 0, yerr = data2['sigma Hr (dB)'], marker = '.', markersize = 13,
                elinewidth=1, color = '#000000', ecolor = '#00b4ff', linewidth=0, capsize=2, label = 'Measures')

    # DRAW DASHED 'ZERO' LINE
    ax2.axhline(color = '#000000', linewidth = 0.5, linestyle = 'dashed')
    
    # PLOT TITLE
    ax1.set_title('PreAmp - Bode Plot', fontsize=32)

    # AXIS LABELS
    # ax1.set_xlabel('log$_{10}$(freq.) (dec)', fontsize = 24, loc = 'right')
    ax1.set_ylabel('H (dB)', fontsize = 24, loc = 'top', labelpad = 0)
    ax2.set_xlabel('frequency (Hz)', fontsize = 24, loc = 'right')
    ax2.set_ylabel('H - fit (dB)', fontsize = 24, loc = 'center', labelpad = 0)

    # AXIS TICKS
    ax1.tick_params(axis = 'x', which = 'major', labelsize = 0, direction = 'in', length = 10)
    ax1.tick_params(axis = 'y', which = 'major', labelsize = 22, direction = 'in', length = 10)
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
    ax1.set_xlim(left = XMIN, right = XMAX)
    ax1.set_ylim(bottom = YMIN, top = YMAX)
    ax2.set_xlim(left = RESXMIN, right = RESXMAX)
    ax2.set_ylim(bottom = RESYMIN, top = RESYMAX)

    # MAKE LEGEND
    handles, labels = ax1.get_legend_handles_labels()
    order = [3, 0, 2, 1]
    ax1.legend([handles[idx] for idx in order], [labels[idx] for idx in order], loc = 'best', prop = {'size': 22}, 
                ncol = 2, frameon = True, fancybox = False, framealpha = 1)

    
    ax1.set_xscale('log')
    ax2.set_xscale('log')
    
    # SAVE FIGURE
    #fig.savefig('../Plots/PreAmp/bode_plot.png', dpi = 300, facecolor = 'white')
    
    plt.show()



####### READ BODE SIMULATION
def get_bode_sim(filename):

    data = pd.read_csv(filename, sep = '\t', index_col = False)

    data['f'] = np.log10(data['f'])

    return data



####### FREQUENZA DI TAGLIO STIMATA CON BODE
def freq_taglio_bode():

    print( 'Frequenza di Taglio teorica ft_th = ' + format(ft_th * 1e-3, '.2f') + ' +/- ' + format(sigma_ft_th * 1e-3, '.2f') + '  kHz')
    print( 'Frequenza di Taglio Bode ft_bode = ' + format(ft_bode * 1e-3, '.2f') + ' +/- ' + format(sigma_ft_bode * 1e-3, '.2f') + '  kHz')
    print( 'Compatibilità frequenza di taglio \u03BB = ' + format(compatib(ft_th, ft_bode, sigma_ft_th, sigma_ft_bode), '1.2f'))



####### TEMPO CARATTERISTICO STIMATO CON BODE
def tau_thebode():

    global tau_bode
    global sigma_tau_bode

    tau_bode = (2 * np.pi * ft_bode)**-1 
    sigma_tau_bode = sigma_ft_bode * (2 * np.pi * ft_bode**2)**-1

    print( 'Tempo caratteristico stimato con Bode \u03C4_bode = ' + format(1e6 * tau_bode, '1.2f') + ' +/- ' + format(1e6 * sigma_tau_bode, '1.2f') + '  \u03BCs')
    print( 'Tempo caratteristico stimato teorico \u03C4_th = ' + format(1e6 * tau_th, '1.2f') + ' +/- ' + format(1e6 * sigma_tau_th, '1.2f') + '  \u03BCs')
    print( 'Compatibilità tempo caratteristico \u03BB = ' + format(compatib(tau_bode, tau_th, sigma_tau_bode, sigma_tau_th), '1.2f'))
    


####### ARDUINO PLOT
def preamp_arduino_plot(data):
    # FIG SETTINGS AND AXES
    fig = plt.figure(figsize=(16,8))
    ax1 = fig.add_subplot(1, 1, 1)

    # PLOT DATA
    ax1.plot(data['time (ms)'], data['V (V)'], color = '#227FF7', linewidth = 2, label = 'Data')

    # PLOT TITLE
    ax1.set_title('PreAmp - Preliminary Arduino Waveform', fontsize = 32)

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
    #fig.savefig('../Logbook/shaper_base_arduino_waveform.png', dpi = 300)

    plt.show()


####### ARDUINO LINEAR PLOT
def preamp_arduino_plot_lin(data):
    # FIG SETTINGS AND AXES
    fig = plt.figure(figsize=(16,8))
    ax1 = fig.add_subplot(1, 1, 1)

    # PERFORM THE FIT
    par, cov = curve_fit(f = lin, xdata = data['time (ms)'], ydata = data['lin ADC'])
    func = lin(data['time (ms)'], *par)

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

    err_a = fit_err[0]
    err_b = fit_err[1]


    # PLOT DATA
    ax1.plot(data['time (ms)'], data['lin ADC'], color = '#227FF7', linewidth = 0, marker = '.', markersize = 10, label = 'Data')
    ax1.plot(data['time (ms)'], func, color = '#FF4B00', linewidth = 2, label = 'Fit')

    # aa = 'a = ' + format(a, '1.2f') + ' +/- ' + format(err_a, '1.2f')
    # bb = 'b = ' + format(b, '1.0f') + ' +/- ' + format(err_b, '1.0f')


    # ax1.text(0.4, 0.7, 'Fit Function        y = a + b * exp(-x / \u03C4)', fontsize = 22, color = '#000000', transform = ax1.transAxes)
    # ax1.text(0.5, 0.5, aa + '\n' + bb + '\n' + cc, fontsize = 18, color = '#000000', transform = ax1.transAxes)

    # PLOT TITLE
    ax1.set_title('PreAmp - Preliminary Arduino LinFit', fontsize = 32)

    # AXIS LABELS
    ax1.set_xlabel('time (ms)', fontsize = 26, loc = 'right')
    ax1.set_ylabel('logADC (a.u.)', fontsize = 26, loc = 'top')

    # AXIS TICKS
    ax1.tick_params(axis = 'both', which = 'major', labelsize = 22, direction = 'in', length = 10)
    ax1.tick_params(axis = 'both', which = 'minor', labelsize = 22, direction = 'in', length = 5)
    ax1.set_xticks(ticks = ax1.get_xticks(), minor = True)
    ax1.set_yticks(ticks = ax1.get_yticks(), minor = True)
    ax1.minorticks_on()

    # PLOT RANGE
    ax1.set_xlim(left = 0.30, right = 0.80)
    ax1.set_ylim(top = 6.3)

    # SAVE FIGURE
    fig.savefig('../Plots/PreAmp/arduino_lin_fit.png', dpi = 300, facecolor = 'white')

    plt.show()



####### ARDUINO EXPONENTIAL FIT
def preamp_arduino_fit(data):

    global arduino_exp_a      
    global arduino_exp_b      
    global arduino_exp_tau    
    global arduino_exp_a_err  
    global arduino_exp_b_err  
    global arduino_exp_tau_err

    # FIG SETTINGS AND AXES
    fig = plt.figure(figsize=(19.2, 9), dpi = 100)
    ax1 = fig.add_subplot(1, 2, 1)
    ax2 = fig.add_subplot(1, 2, 2)

    par, cov = curve_fit(f = esp, xdata = data['time (ms)'], ydata = data['V (V)'], maxfev=1000, 
                        p0 = [0.02, 0.6, 0.151], sigma = data['err V (V)'], absolute_sigma = True)

    func = esp(data['time (ms)'], *par)

    # COMPUTE RESIDUALS
    res = data['V (V)'] - func

    # COMPUTE CHI2
    chi2 = np.sum((res/data['err V (V)'])**2)

    # GET FIT PARAMETERS AND PARAMETER ERRORS
    error = []

    for i in range(len(par)):
        try:
            error.append(np.absolute(cov[i][i])**0.5)
        except:
            error.append( 0.00 )

    fit_par = par
    fit_err = np.array(error)


    arduino_exp_a = fit_par[0]
    arduino_exp_b = fit_par[1]
    arduino_exp_tau = fit_par[2]

    arduino_exp_a_err = fit_err[0]
    arduino_exp_b_err = fit_err[1]
    arduino_exp_tau_err = fit_err[2]

    # COMPUTE SIGMA_POST
    sigma_post = np.sqrt( np.sum( res**2 ) / (len(data['V (V)']) - 2) ) 

    # PLOT DATA
    ax1.plot(data['time (ms)'], data['V (V)'], color = '#227FF7', linewidth = 2, label = 'Data')
    ax1.plot(data['time (ms)'], func, color = '#FF4B00', linewidth = 2, linestyle = 'dashed', label = 'Fit')

    # PLOT RESIDUALS
    ax2.errorbar(data['time (ms)'], res, xerr = 0, yerr = data['err V (V)'], marker = '.', markersize = 13,
                elinewidth=1, color = '#227FF7', linewidth=0, capsize=2, label = 'Residuals')

    # DRAW DASHED 'ZERO' LINE
    ax2.axhline(color = '#000000', linewidth = 0.5, linestyle = 'dashed')

    aa = 'a = ' + format(arduino_exp_a, '1.4f') + ' +/- ' + format(arduino_exp_a_err, '1.4f') + '  V'
    bb = 'b = ' + format(arduino_exp_b, '1.2f') + ' +/- ' + format(arduino_exp_b_err, '1.2f')
    cc = '\u03C4 = ' + format(arduino_exp_tau * 1e3, '1.2f') + ' +/- ' + format(arduino_exp_tau_err * 1e3, '1.2f') + '  \u03BCs'
    chisq = '$\chi^{2}$ / ndf = ' + format(chi2, '1.1f') + ' / ' + format(len(data['time (ms)'] ) - len(par), '1.0f') 
    sigmap = '\u03C3$_{post}$ = ' + format(sigma_post, '1.3f') + '  V'
    
    ax1.text(0.15, 0.90, 'Fit Function', fontsize = 28, fontweight = 'bold', transform=ax1.transAxes)

    ax1.text(0.19, 0.83, 'y = a + b * exp(-x / \u03C4)', fontsize = 26, color = '#000000', transform = ax1.transAxes)

    ax1.text(0.28, 0.35, aa + '\n' + bb + '\n' + cc + '\n' + chisq + '\n' + sigmap, fontsize = 24, color = '#000000', transform = ax1.transAxes)

    # PLOT TITLE
    fig.suptitle('PreAmp - Arduino ExpFit', fontsize = 36)

    # AXIS LABELS
    ax1.set_xlabel('time (ms)', fontsize = 26, loc = 'right')
    ax1.set_ylabel('V (V)', fontsize = 26, loc = 'top')
    ax2.set_xlabel('time (ms)', fontsize = 26, loc = 'right')
    ax2.set_ylabel('V - fit (V)', fontsize = 26, loc = 'top', labelpad = -15)

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
    ax2.set_ylim(bottom = -0.05, top = 0.05)

    # SAVE FIGURE
    #fig.savefig('../Plots/PreAmp/arduino_exp_fit.png', dpi = 300, facecolor = 'white')

    plt.show()


####### TEMPO CARATTERISTICO STIMATO ARDUINO EXPFIT
def tau_arduino_exp():

    print( 'Tempo caratteristico stimato con Arduino \u03C4_exp = ' + format(1e3 * arduino_exp_tau, '1.2f') + ' +/- ' + format(1e3 * arduino_exp_tau_err, '1.2f') + '  \u03BCs')
    print( 'Tempo caratteristico stimato teorico \u03C4_th = ' + format(1e6 * tau_th, '1.2f') + ' +/- ' + format(1e6 * sigma_tau_th, '1.2f') + '  \u03BCs')
    print( 'Compatibilità tempo caratteristico \u03BB = ' + format(compatib(1e-3 * arduino_exp_tau, tau_th, 1e-3 * arduino_exp_tau_err, sigma_tau_th), '1.2f'))



####### ARDUINO CALIRATION READ DATA
def arduino_calib_read():
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

    #data_in =  pd.read_csv(file_in, sep = ' ', index_col = False, header = None)
    #data_in.index = np.arange(1, len(data_in)+1)
    #data_in.columns = ['Vin']
    #Vin = data_in.to_numpy()

    Vin = np.loadtxt(file_in)

    Vdiv = np.loadtxt(file_vdiv)

    data = pd.DataFrame({'max_values': list(max_values), 'Vin': list(Vin), 'Vdiv': list(Vdiv)}, columns = ['max_values', 'Vin', 'Vdiv'])

    return data

####### ARDUINO CALIRATION READ DATA LOW TENSIONS
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

    #data_in =  pd.read_csv(file_in, sep = ' ', index_col = False, header = None)
    #data_in.index = np.arange(1, len(data_in)+1)
    #data_in.columns = ['Vin']
    #Vin = data_in.to_numpy()

    Vin = np.loadtxt(file_in)

    Vdiv = np.loadtxt(file_vdiv)

    data = pd.DataFrame({'max_values': list(max_values), 'Vin': list(Vin), 'Vdiv': list(Vdiv)}, columns = ['max_values', 'Vin', 'Vdiv'])
    
    data = data.iloc[:3,:]

    return data

####### ARDUINO CALIBRATION FIT
def arduino_calib_plot(data):

    global arduino_calib_offset
    global arduino_calib_slope
    global arduino_calib_offset_err
    global arduino_calib_slope_err

    XMIN = 800
    XMAX = 4200
    YMIN = 0
    YMAX = 2.7
    RESXMIN = XMIN
    RESXMAX = XMAX
    RESYMIN = -0.08
    RESYMAX = 0.08

    # FIG SETTINGS AND AXES
    fig = plt.figure(figsize=(16,8))
    ax1 = fig.add_subplot(1, 2, 1)
    ax2 = fig.add_subplot(1, 2, 2)

    # PERFORM THE FIT
    par_lin, cov_lin = curve_fit(f = lin, xdata = data['max_values'], ydata = data['Vin'])
    func = lin(data['max_values'], *par_lin)

    # COMPUTE RESIDUALS
    res = data['Vin'] - func

    # COMPUTE CHI2
    chi2 = np.sum((res/data['err Vin'])**2)

    # GET FIT PARAMETERS AND PARAMETER ERRORS
    error = []
    for i in range(len(par_lin)):
        try:
            error.append(np.absolute(cov_lin[i][i])**0.5)
        except:
            error.append( 0.00 )

    fit_par = par_lin
    fit_err = np.array(error)

    arduino_calib_offset = fit_par[0]
    arduino_calib_slope = fit_par[1]
    arduino_calib_offset_err = fit_err[0]
    arduino_calib_slope_err = fit_err[1]

    # COMPUTE SIGMA_POST
    sigma_post = np.sqrt( np.sum( res**2 ) / (len(data['max_values']) - 2) ) 

    # PLOT DATA
    ax1.errorbar(data['max_values'], data['Vin'], xerr = 0, yerr = data['err Vin'], color = '#000000', linewidth = 0, marker = '.', markersize = 15, elinewidth=1, capsize=2, label = 'Data')

    # PLOT FIT FUNCTION
    ax1.plot(np.arange(XMIN, XMAX + 1, 1), lin(np.arange(XMIN, XMAX + 1, 1), *par_lin), color = '#FF4B00', linewidth = 2, linestyle = 'dashed', label = 'Fit')
    
    # DRAW DASHED 'ZERO' LINE
    ax2.axhline(color = '#000000', linewidth = 0.5, linestyle = 'dashed')

    # DRAW RESIDUALS
    ax2.errorbar(data['max_values'], res, xerr=0, yerr = data['err Vin'], marker = '.', markersize = 13, 
            elinewidth=1, color = '#000000', linewidth=0, capsize=2, label = 'Residuals')

    q = 'a = ' + format(arduino_calib_offset, '1.3f') + ' V +/- ' + format(arduino_calib_offset_err, '1.3f') + ' V'
    m = 'b = ' + format(arduino_calib_slope * 1e3, '1.3f') + ' +/- ' + format(arduino_calib_slope_err * 1e3, '1.3f') + ' mV/adc'
    chisq = '$\chi^{2}$ / ndf = ' + format(chi2, '1.2f') + ' / ' + format(len(data['max_values']) - len(par_lin), '1.0f') 
    sigmap = '\u03C3$_{post}$ = ' + format(sigma_post, '1.3f') + ' V'
    ax1.text(0.15, 0.85, 'Fit Function', fontsize = 22, fontweight = 'bold', transform=ax1.transAxes)
    ax1.text(0.20, 0.80, 'y = a + bx', fontsize = 18, transform=ax1.transAxes)
    ax1.text(0.45, 0.35, 'Fit Parameters', fontsize = 22, fontweight = 'bold', transform=ax1.transAxes)
    ax1.text(0.40, 0.28, q, fontsize = 18, transform=ax1.transAxes)
    ax1.text(0.40, 0.22, m, fontsize = 18, transform=ax1.transAxes)
    ax1.text(0.40, 0.16, chisq, fontsize = 18, transform=ax1.transAxes)
    ax1.text(0.40, 0.10, sigmap, fontsize = 18, transform=ax1.transAxes)

    # PLOT TITLE
    fig.suptitle('Arduino 18 Calibration Fit', fontsize=32)

    # AXIS LABELS
    ax1.set_xlabel('V (adc)', fontsize = 26, loc = 'right')
    ax1.set_ylabel('V (V)', fontsize = 26, loc = 'top')

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
    ax1.set_xlim(left = XMIN, right = XMAX)
    ax1.set_ylim(bottom = YMIN, top = YMAX)
    ax2.set_xlim(left = RESXMIN, right = RESXMAX)
    ax2.set_ylim(bottom = RESYMIN, top = RESYMAX)

    # SAVE FIGURE
    #fig.savefig('../Logbook/catena_linearity.png', dpi = 300, facecolor = 'white')

    plt.show()


####### ARDUINO GET CALIBRATION FUNCTION
def get_calib_function():
    print(
        'VOLT = ' +  ' (' + format(arduino_calib_offset, '.3f') + ' +/- ' + format(arduino_calib_offset_err, '.3f') + ') ' + ' + ' 
        + ' (' + format(arduino_calib_slope, '.6f') + ' +/- ' + format(arduino_calib_slope_err, '.6f') + ') ' + ' ADC'
    )



####### ARDUINO CALIBRATON
def arduino_calib(ADC):
    V = arduino_calib_offset + arduino_calib_slope * ADC
    return V



####### ARDUINO CALIBRATON ERROR
def arduino_calib_err():
    errV = np.sqrt(arduino_calib_offset_err**2 + arduino_calib_slope_err**2)
    return errV