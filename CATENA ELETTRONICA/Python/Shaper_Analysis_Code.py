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

# Misure Pre-Amp

Rin = 56564 #Ohm
Rf = 696060 #Ohm
Cf = 0.000000000232 #Farad

# Fondo Scala
FS_Rin = 100000 #Ohm
FS_Rf = 1000000 #Ohm
FS_Cf = 0.000000001 #Farad

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


# Misure Shaper

#Valore
R1 = 100990 #Ohm
R2 = 99930  #Ohm
C1 = 0.000000000157 #Farad
C2 = 0.000000000159 #Farad

# Fondo Scala
FS_R1 = 1000000 #Ohm
FS_R2 = 1000000 #Ohm
FS_C1 = 0.000000001 #Farad
FS_C2 = 0.000000001 #Farad

L_R1 = 0.07 / 100
L_R2 = 0.07 / 100
L_C1 = 2.5 / 100
L_C2 = 2.5 / 100
D_R1 = 8
D_R2 = 8
D_C1 = 15
D_C2 = 15
Res_R1 = 10
Res_R2 = 10
Res_C1 = 1e-12
Res_C2 = 1e-12

sigma_L_R1 = 0.58 * L_R1 * R1
sigma_L_R2 = 0.58 * L_R2 * R2
sigma_L_C1 = 0.58 * L_C1 * C1
sigma_L_C2 = 0.58 * L_C2 * C2
sigma_D_R1 = 0.58 * D_R1 * Res_R1
sigma_D_R2 = 0.58 * D_R2 * Res_R2
sigma_D_C1 = 0.58 * D_C1 * Res_C1
sigma_D_C2 = 0.58 * D_C2 * Res_C2

sigma_R1 = np.sqrt(sigma_L_R1**2 + sigma_D_R1**2)
sigma_R2 = np.sqrt(sigma_L_R2**2 + sigma_D_R2**2)
sigma_C1 = np.sqrt(sigma_L_C1**2 + sigma_D_C1**2)
sigma_C2 = np.sqrt(sigma_L_C2**2 + sigma_D_C2**2)

### ------------------------------------ ------------------- --------------------------------------

### ------------------------------------- MISURE SPERIMENTALI -------------------------------------

#Generatore
freq = 100 #Hz
Amp = 1.01 #V



#Segnale in uscita
V_out_max = 0.342
Vdiv_out_max = 0.065

#Tempo del massimo
t_max = 16 * 1e-6
tdiv = 85 * 1e-6


### ------------------------------------ ------------------- --------------------------------------



tau_sh_th : float
tau_sh_th1 : float
tau_sh_th2 : float

sigma_tau_sh_th : float
sigma_tau_sh_th1 : float
sigma_tau_sh_th2 : float





####### READ DATA
def get_data(file_name):

    df = pd.read_csv(file_name, index_col = False, header = None, sep = '\t')
    df.index = np.arange(1, len(df)+1)

    return df



####### PROPAGAZIONE SUI CURSORI
def propagazione_cursori(Vdiv, measure):

    sigma = np.sqrt( (0.04 * Vdiv)**2 + (0.015 * measure)**2)

    return sigma



err_Amp = propagazione_cursori(0.2, Amp)
err_V_out_max = propagazione_cursori(Vdiv_out_max, V_out_max)

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



##### CALCOLO COMPATIBILITA
def compatib(x, y, errx, erry):

    comp = np.abs( x - y ) / np.sqrt( errx**2 + erry**2 )

    return comp



####### MISURE DIRETTE COMPONENTI CIRCUITALI
def misure_dirette():

    data = {'Valore' : [format(R1 * 1e-3, '1.2f') + ' k\u03A9', format(R2 * 1e-3, '1.2f') + ' k\u03A9', 
                        format(C1 * 1e12, '1.0f') + ' pF', format(C2 * 1e12, '1.0f') + ' pF'], 
            'Errore' : [format(sigma_R1 * 1e-3, '1.2f') + ' k\u03A9', format(sigma_R2 * 1e-3, '1.2f') + ' k\u03A9', 
                        format(sigma_C1 * 1e12, '1.0f') + ' pF', format(sigma_C2 * 1e12, '1.0f') + ' pF'],
             'FS' : [format(FS_R1 * 1e-3, '1.0f') + ' k\u03A9', format(FS_R2 * 1e-3, '1.0f') + ' k\u03A9', 
                    format(FS_C1 * 1e12, '1.0f') + ' pF', format(FS_C2 * 1e12, '1.0f') + ' pF']}
    
    df = pd.DataFrame(data = data, index = ['R1', 'R2', 'C1', 'C2'])

    return df



####### STIME TEORICHE TAU SHAPER
def get_tau_sh_th():

    global tau_sh_th1
    global tau_sh_th2
    global sigma_tau_sh_th1
    global sigma_tau_sh_th2

    tau_sh_th1 = R1 * C1
    tau_sh_th2 = R2 * C2
    sigma_tau_sh_th1 = np.sqrt( (C1 * sigma_R1)**2 + (R1 * sigma_C1)**2 )
    sigma_tau_sh_th2 = np.sqrt( (C2 * sigma_R2)**2 + (R2 * sigma_C2)**2 )
    print('\u03C4_sh_th1 =  ' + format(tau_sh_th1 * 1e6, '1.2f') + ' +/- ' + format(sigma_tau_sh_th1 * 1e6, '1.2f') + '  \u03BCs')
    print('\u03C4_sh_th2 =  ' + format(tau_sh_th2 * 1e6, '1.2f') + ' +/- ' + format(sigma_tau_sh_th2 * 1e6, '1.2f') + '  \u03BCs')
    


####### MEDIA PESATA TAU SHAPER
def get_tau_sh_mean():

    global tau_sh_th
    global sigma_tau_sh_th

    tau_sh_th = ( (tau_sh_th1 * sigma_tau_sh_th1**-2) + (tau_sh_th2 * sigma_tau_sh_th2**-2) ) / (sigma_tau_sh_th1**-2 + sigma_tau_sh_th2**-2)
    sigma_tau_sh_th = 1 / (sigma_tau_sh_th1**-2 + sigma_tau_sh_th2**-2)**0.5
    
    print('\u03C4_sh_th =  ' + format(tau_sh_th * 1e6, '1.2f') + ' +/- ' + format(sigma_tau_sh_th * 1e6, '1.2f') + '  \u03BCs')
    



def get_V_out_max():
    
    V_out_th = Amp / np.exp(1)
    err_V_out_th = err_Amp / np.exp(1)
    
    l = compatib(V_out_max, V_out_th, err_V_out_max, err_V_out_th)

    print(
        'V_max_th = ' + format(V_out_th, '.3f') + ' +/- ' + format(err_V_out_th, '.3f') + '  V\n' + 
        'V_max_sper = ' + format(V_out_max, '.3f') + ' +/- ' + format(err_V_out_max, '.3f') + '  V\n' + 
        'Compatibilità  \u03BB = ' + format(l, '.2f') + '\n'
        'Variazione percentuale: ' + format( 1e2 * abs( V_out_th - V_out_max) / V_out_th , '.2f') + '%' 
    )



def get_t_sper():

    err_t_max = 0.04 * tdiv
    l = compatib(t_max, tau_sh_th, err_t_max, sigma_tau_sh_th)

    print(
        '\u03C4_sper = ' + format(1e6 * t_max, '.2f') + ' +/- ' + format(1e6 * err_t_max, '.2f') + '  \u03BCs\n' + 
        '\u03C4_sh_th =  ' + format(tau_sh_th * 1e6, '1.2f') + ' +/- ' + format(sigma_tau_sh_th * 1e6, '1.2f') + '  \u03BCs\n'
        'Compatibilità  \u03BB = ' + format(l, '.2f') + '\n'
        'Variazione percentuale: ' + format( 1e2 * abs( tau_sh_th - t_max) / tau_sh_th , '.2f') + '%' 
    )



####### READ BODE SIMULATION
def get_bode_sim(filename):

    data = pd.read_csv(filename, sep = '\t', index_col = False)

    return data


####### LINEAR FUCTION
def lin(x, a, b):  
    return a + b * x




def bode_plot(df, sim):

    XMIN = 40
    XMAX = 1.2 * 1e6
    YMIN = -50
    YMAX = 0

    # ARANCIONE
    data1 = df.iloc[2:6, :]

    # BLU
    data2 = df.iloc[18:21, :]

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
    a = fit_par1[0]
    b = fit_par1[1]
    err_a = fit_err1[0]
    err_b = fit_err1[1]

    # BLU
    c = fit_par2[0]
    d = fit_par2[1]
    err_c = fit_err2[0]
    err_d = fit_err2[1]

    # COMPUTE RESIDUALS

    # ARANCIONE
    res1 = data1['H (dB)'] - lin(data1['log10f (dec)'], *par1)

    # BLU
    res2 = data2['H (dB)'] - lin(data2['log10f (dec)'], *par2)

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


    # FIG SETTINGS AND AXES
    fig = plt.figure(figsize=(16,10))
    ax1 = fig.add_subplot(1, 1, 1)
    #ax1 = plt.subplot2grid((10, 1), (0, 0), rowspan=8, colspan=1)
    #ax2 = plt.subplot2grid((10, 1), (8, 0), rowspan=2, colspan=1)


    # PLOT DATA
    ax1.errorbar(df['freq (Hz)'], df['H (dB)'], xerr = 0, yerr = df['sigma Hr (dB)'], marker = '.', markersize = 13,
                elinewidth=1, color = '#000000', linewidth=0, capsize=2, label = 'Measures')
    
    # PLOT SIMULATIONS
    ax1.plot(sim['Freq.'], sim['V(out)/V(in)'], color = '#4b00ff', linewidth = 1, linestyle = '-', label = 'Simulation')

    # PLOT FIT FUNCTIONS
    ax1.plot(np.arange(XMIN, XMAX + 1, 1), lin(np.log10(np.arange(XMIN, XMAX+1, 1)), *par1), color = '#FF4B00', linewidth = 2, linestyle = 'dashed', label = 'y = a + bx')
    ax1.plot(np.arange(XMIN, XMAX + 1, 1), lin(np.log10(np.arange(XMIN, XMAX+1, 1)), *par2), color = '#00b4ff', linewidth = 2, linestyle = 'dashed', label = 'y = c + dx')


    # PLOT TITLE
    ax1.set_title('Shaper - Bode Plot', fontsize=32)

    # AXIS LABELS
    # ax1.set_xlabel('log$_{10}$(freq.) (dec)', fontsize = 24, loc = 'right')
    ax1.set_ylabel('H (dB)', fontsize = 24, loc = 'top', labelpad = 0)
    ax1.set_xlabel('frequency (Hz)', fontsize = 24, loc = 'right')

    # AXIS TICKS
    ax1.tick_params(axis = 'x', which = 'major', labelsize = 22, direction = 'in', length = 10)
    ax1.tick_params(axis = 'y', which = 'major', labelsize = 22, direction = 'in', length = 10)
    ax1.tick_params(axis = 'both', which = 'minor', labelsize = 22, direction = 'in', length = 5)
    ax1.set_xticks(ticks = ax1.get_xticks(), minor = True)
    ax1.set_yticks(ticks = ax1.get_yticks(), minor = True)
    ax1.minorticks_on()

    # PLOT RANGE
    ax1.set_xlim(left = XMIN, right = XMAX)
    ax1.set_ylim(bottom = YMIN, top = YMAX)
    

    # MAKE LEGEND
    handles, labels = ax1.get_legend_handles_labels()
    order = [3, 0, 1, 2]
    ax1.legend([handles[idx] for idx in order], [labels[idx] for idx in order], loc = 'best', prop = {'size': 22}, 
                ncol = 2, frameon = True, fancybox = False, framealpha = 1)



    
    ax1.set_xscale('log')
    
    # SAVE FIGURE
    #fig.savefig('../Plots/Shaper/bode_plot.png', dpi = 300, facecolor = 'white')
    
    plt.show()