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

### CONSTANTS

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

### VARIABILI GLOBALI

Qth = 0
sigma_Qth = 0

tau_th = 0
sigma_tau_th = 0

Vmax_th = 0
sigma_Vmax_th = 0

Cf_fit = 0
sigma_Cf_fit = 0

### PARAMETRI FIT

a = 0
b = 0
err_a = 0
err_b = 0

c = 0
d = 0
err_c = 0
err_d = 0

e = 0
f = 0
err_e = 0
err_f = 0

ft_bode = 0
sigma_ft_bode = 0
ft_th = 0
sigma_ft_th = 0



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

    sigma_Cf_fit = np.sqrt( (err_b / b**2)**2 + (0.015 / b)**2 )

    print('Cf_fit = ' + format(Cf_fit, '1.2f') + ' +/- ' + format(sigma_Cf_fit, '1.2f') + '  pF')

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
    XMIN = 0.9
    XMAX = 6.1
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
    ax1.errorbar(df['log10f (dec)'], df['H (dB)'], xerr = 0, yerr = df['sigma H (dB)'], marker = '.', markersize = 13,
                elinewidth=1, color = '#000000', linewidth=0, capsize=2, label = 'Measures')
    
    # PLOT SIMULATIONS
    ax1.plot(sim['f'], sim['H'], color = '#4b00ff', linewidth = 1, linestyle = '-', label = 'Simulation')

    # PLOT FIT FUNCTIONS
    ax1.plot(np.arange(XMIN, XMAX + 1, 1), lin(np.arange(XMIN, XMAX + 1, 1), *par1), color = '#FF4B00', linewidth = 2, linestyle = 'dashed', label = 'y = c + dx')
    ax1.plot(np.arange(XMIN, XMAX + 1, 1), lin(np.arange(XMIN, XMAX + 1, 1), *par2), color = '#00b4ff', linewidth = 2, linestyle = 'dashed', label = 'y = a + bx')

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
    ax2.errorbar(data1['log10f (dec)'], res1, xerr = 0, yerr = data1['sigma Hr (dB)'], marker = '.', markersize = 13,
                elinewidth=1, color = '#FF4B00', linewidth=0, capsize=2, label = 'Measures')

    # BLU 
    ax2.errorbar(data2['log10f (dec)'], res2, xerr = 0, yerr = data2['sigma Hr (dB)'], marker = '.', markersize = 13,
                elinewidth=1, color = '#00b4ff', linewidth=0, capsize=2, label = 'Measures')

    # DRAW DASHED 'ZERO' LINE
    ax2.axhline(color = '#000000', linewidth = 0.5, linestyle = 'dashed')
    
    # PLOT TITLE
    ax1.set_title('PreAmp - Bode Plot', fontsize=32)

    # AXIS LABELS
    # ax1.set_xlabel('log$_{10}$(freq.) (dec)', fontsize = 24, loc = 'right')
    ax1.set_ylabel('H (dB)', fontsize = 24, loc = 'top', labelpad = 0)
    ax2.set_xlabel('log$_{10}$(freq.) (dec)', fontsize = 24, loc = 'right')
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
    

    # SAVE FIGURE
    #fig.savefig('../Plots/PreAmp/bode_plot.png', dpi = 300, facecolor = 'white')
    global k 
    k = 2
    plt.show()

####### READ BODE SIMULATION
def get_bode_sim(filename):

    data = pd.read_csv(filename, sep = '\t', index_col = False)

    data['f'] = np.log10(data['f'])

    return data