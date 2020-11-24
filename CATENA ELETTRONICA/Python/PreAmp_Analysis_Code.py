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

### CONSTANTS

# Misure Dirette
Rin = 56564 #Ohm
Rf = 696060 #Ohm
Cf = 0.000000000222 #Farad

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

    tau_th = Rf * Cf
    sigma_tau_th = np.sqrt( (Cf * sigma_Rf)**2 + (Rf * sigma_Cf)**2 )

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
    sigma_post = np.sqrt(np.sum(res)**2 / (len(df['Qin (pC)']) - len(par_lin))) 

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
    sigmap = '\u03C3$_{post}$ = ' + format(sigma_post, '1.4f') + ' V'

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
    fig.savefig('../Plots/PreAmp/Vmax_Qin_lin_fit.png', dpi = 300, facecolor='white')

    plt.show()



