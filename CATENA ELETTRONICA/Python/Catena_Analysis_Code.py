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

R1a = 9982  #ohm
R2a = 82393 #ohm

FS = 100000 #ohm
L = 0.07 / 100
D = 8
RES = 1

sigma_L = 0.58 * L
sigma_D = 0.58 * D * RES

sigma_R1a = np.sqrt( (sigma_L* R1a)**2 + sigma_D**2 )
sigma_R2a = np.sqrt( (sigma_L* R2a)**2 + sigma_D**2 )

### ------------------------------------- MISURE SPERIMENTALI -------------------------------------

####### PROPAGAZIONE SUI CURSORI
def propagazione_cursori(Vdiv, measure):

    sigma = np.sqrt( (0.04 * Vdiv)**2 + (0.015 * measure)**2 )

    return sigma

#Generatore
V_gen = 1.02 #volt
sigma_V_gen = propagazione_cursori(0.5, V_gen) #volt

#Shaper
V_shaper = 0.26 #volt
sigma_V_shaper = propagazione_cursori(0.05, V_shaper) #volt

#Catena Completa
V_catena = 2.32 #volt
sigma_V_catena = propagazione_cursori(0.5, V_catena) #volt

### ------------------------------------------ STIME -----------------------------------------------

G_sper = 1 + R2a / R1a
# sigma_G_sper = np.sqrt( (sigma_D / R1a)**2 + (sigma_D / R2a)**2 + 2 * sigma_L**2)
sigma_G_sper = np.sqrt( (sigma_D / R1a)**2 + (sigma_D * R2a / R1a**2)**2 + (R2a / R1a) * sigma_L**2)

V_catena_expected = G_sper * V_shaper
sigma_V_catena_expected = np.sqrt( (V_shaper * sigma_G_sper)**2 + (G_sper * sigma_V_shaper)**2 )


c : float
d : float
err_c : float
err_d : float

e : float
f : float
err_e : float
err_f : float

ft_bode : float
sigma_ft_bode : float


### ------------------------------------ ------------------- --------------------------------------
### ------------------------------------ ------------------- --------------------------------------
### ------------------------------------------ FUNCTIONS ------------------------------------------
### ------------------------------------ ------------------- --------------------------------------
### ------------------------------------ ------------------- --------------------------------------


####### MISURE DIRETTE DELLE COMPONENTI CIRCUITALI
def misure_dirette():

    data = {'Valore' : [format(R1a * 1e-3, '1.3f') + ' k\u03A9', format(R2a * 1e-3, '1.2f') + ' k\u03A9'], 
            'Errore' : [format(sigma_R1a * 1e-3, '1.3f') + ' k\u03A9', format(sigma_R2a * 1e-3, '1.2f') + ' k\u03A9'],
             'FS' : [format(FS * 1e-3, '1.0f') + ' k\u03A9', format(FS * 1e-3, '1.0f') + ' k\u03A9']}
    
    df = pd.DataFrame(data = data, index = ['R1a', 'R2a'])

    return df



####### LINEAR FUCTION
def lin(x, a, b):  
    return a + b * x



##### CALCOLO COMPATIBILITA
def compatib(x, y, errx, erry):

    comp = np.abs( x - y ) / np.sqrt( errx**2 + erry**2 )

    return comp


def get_G_th():
    
    print(
        'Amplificazione teorica   G = ' + format(G_sper, '.3f') + ' +/- ' + format(sigma_G_sper, '.3f')
    )

def get_Vshaper_sper():
    
    print(
        'V_shaper_sper = ' + format(V_shaper, '.3f') + ' +/- ' + format(sigma_V_shaper, '.3f')
    )

def get_Vcatena_th():
    
    print(
        'V_catena_th = ' + format(V_catena_expected, '.2f') + ' +/- ' + format(sigma_V_catena_expected, '.2f')
    )

def get_Vcatena_sper():
    
    print(
        'V_catena_sper = ' + format(V_catena, '.2f') + ' +/- ' + format(sigma_V_catena, '.2f')
    )


def get_Vcatena_comp():

    l = compatib(V_catena, V_catena_expected, sigma_V_catena, sigma_V_catena_expected)
    print(
        'Compatibilità \u03BB = ' + format(l, '.2f')
    )


####### READ DATA
def get_linearity_data():

    # READ DATA
    file1 = '../Data/Catena/catena_2us_ROOT.dat'
    file2 = '../Data/Catena/catena_3us_ROOT.dat'
    file3 = '../Data/Catena/catena_4us_ROOT.dat'
    file4 = '../Data/Catena/catena_5us_ROOT.dat'
    file5 = '../Data/Catena/catena_6us_ROOT.dat'
    file6 = '../Data/Catena/catena_7us_ROOT.dat'
    file7 = '../Data/Catena/catena_8us_ROOT.dat'
    file8 = '../Data/Catena/catena_9us_ROOT.dat'
    file9 = '../Data/Catena/catena_10us_ROOT.dat'

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

    return data1, data2, data3, data4, data5, data6, data7, data8, data9


def get_max_values():

    data1, data2, data3, data4, data5, data6, data7, data8, data9 = get_linearity_data()

    max1 = data1['ADC'].max()
    max2 = data2['ADC'].max()
    max3 = data3['ADC'].max()
    max4 = data4['ADC'].max()
    max5 = data5['ADC'].max()
    max6 = data6['ADC'].max()
    max7 = data7['ADC'].max()
    max8 = data8['ADC'].max()
    max9 = data9['ADC'].max()

    max_values = np.array([max1, max2, max3, max4, max5, max6, max7, max8, max9])

    return max_values

def compute_charge():

    Rin = 56564
    FS_Rin = 100000
    L_Rin = 0.07 / 100
    D_Rin = 8
    Res_Rin = 1
    sigma_L_Rin = 0.58 * L_Rin * Rin
    sigma_D_Rin = 0.58 * D_Rin * Res_Rin
    sigma_Rin = np.sqrt(sigma_L_Rin**2 + sigma_D_Rin**2)

    Vin = 1.018
    sigma_Vin = propagazione_cursori(0.5, Vin)

    I = Vin / Rin
    sigma_I = np.sqrt( ( sigma_Vin / Rin )**2 + ( sigma_Rin * Vin / Rin**2 )**2 )

    T1 = 1e-6 * 2  #s
    T2 = 1e-6 * 3  #s
    T3 = 1e-6 * 4  #s
    T4 = 1e-6 * 5  #s
    T5 = 1e-6 * 6  #s
    T6 = 1e-6 * 7  #s
    T7 = 1e-6 * 8  #s
    T8 = 1e-6 * 9  #s
    T9 = 1e-6 * 10 #s

    Q1 = T1 * I * 1e12 #pF
    Q2 = T2 * I * 1e12 #pF
    Q3 = T3 * I * 1e12 #pF
    Q4 = T4 * I * 1e12 #pF
    Q5 = T5 * I * 1e12 #pF
    Q6 = T6 * I * 1e12 #pF
    Q7 = T7 * I * 1e12 #pF
    Q8 = T8 * I * 1e12 #pF
    Q9 = T9 * I * 1e12 #pF

    sigma_Q1 = T1 * sigma_I * 1e12 #pF
    sigma_Q2 = T2 * sigma_I * 1e12 #pF
    sigma_Q3 = T3 * sigma_I * 1e12 #pF
    sigma_Q4 = T4 * sigma_I * 1e12 #pF
    sigma_Q5 = T5 * sigma_I * 1e12 #pF
    sigma_Q6 = T6 * sigma_I * 1e12 #pF
    sigma_Q7 = T7 * sigma_I * 1e12 #pF
    sigma_Q8 = T8 * sigma_I * 1e12 #pF
    sigma_Q9 = T9 * sigma_I * 1e12 #pF

    charge = np.array([Q1, Q2, Q3, Q4, Q5, Q6, Q7, Q8, Q9])
    err_charge = np.array([sigma_Q1, sigma_Q2, sigma_Q3, sigma_Q4, sigma_Q5, sigma_Q6, sigma_Q7, sigma_Q8, sigma_Q9])

    return charge, err_charge

def make_dataframe():

    max_values = get_max_values()
    charge, err_charge = compute_charge()

    data = pd.DataFrame({'max_values': list(max_values), 'charge': list(charge), 'err_charge': list(err_charge)}, columns = ['max_values', 'charge', 'err_charge'])

    return data

def arduino_calib():
    # READ DATA FROM FILE
    file_name = '../Data/Shaper/calib_arduino7.dat'

    data = pd.read_csv(file_name, index_col = False, header = None, sep = ' ')
    data.index = np.arange(1, len(data)+1)

    data.columns = ['time', 'ADC']

    SAMPLING = 955000

    ADC_max = data['ADC'].max()
    ADC_min = data['ADC'].min()

    ADC_amplitude = ADC_max - ADC_min + 0.385

    b = V_gen / ADC_amplitude
    a = -b * ADC_min

    err_b = propagazione_cursori(0.2, V_gen) / ADC_amplitude
    #err_b = b * propagazione_cursori(0.2, 1)
    err_a = ADC_min * err_b

    return a, b, err_a, err_b


def max_values_calib(data):

    a, b, err_a, err_b = arduino_calib()

    data['V (V)'] = a + b * data['max_values']
    data['err V (V)'] = np.sqrt( err_a**2 + ( data['max_values'] * err_b )**2 )


def linearity_plot(data):
    # FIG SETTINGS AND AXES
    fig = plt.figure(figsize=(16,8))
    ax1 = fig.add_subplot(1, 2, 1)
    ax2 = fig.add_subplot(1, 2, 2)

    data.drop(axis = 0, labels = [0, 8], inplace = True)

    # CONSTANTS
    XMIN = 30
    XMAX = 185
    YMIN = 0.25
    YMAX = 2.75
    RESXMIN = XMIN
    RESXMAX = XMAX
    RESYMIN = -0.05
    RESYMAX = 0.05
    
    # PERFORM THE FIT
    par_lin, cov_lin = curve_fit(f = lin, xdata = data['charge'], ydata = data['V (V)'], sigma=data['err V (V)'], absolute_sigma=True)
    func = lin(data['charge'], *par_lin)

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

    # COMPUTE RESIDUALS
    res = data['V (V)'] - func

    # COMPUTE CHI2
    chi2 = np.sum((res/data['err V (V)'])**2)

    # COMPUTE SIGMA_POST
    sigma_post = np.sqrt( np.sum( res**2 ) / (len(data['charge']) - 2) ) 


    # PLOT DATA
    ax1.errorbar(data['charge'], data['V (V)'], xerr = 0, yerr = data['err V (V)'], color = '#000000', linewidth = 0, marker = '.', markersize = 13, 
                elinewidth=1, capsize = 2,  label = 'Data')
    
    # PLOT FIT FUNCTION
    ax1.plot(np.arange(XMIN, XMAX, 0.1), lin(np.arange(XMIN, XMAX, 0.1), *par_lin), color = '#FF4B00', linewidth = 2, linestyle = 'solid', label = 'Fit')
    
    # DRAW DASHED 'ZERO' LINE
    ax2.axhline(color = '#000000', linewidth = 0.5, linestyle = 'dashed')

    # DRAW RESIDUALS
    ax2.errorbar(data['charge'], res, xerr=0, yerr=data['err V (V)'], marker = '.', markersize = 13, 
                elinewidth=1, color = '#000000', linewidth=0, capsize=2, label = 'Residuals')


    # PRINT FIT RESULTS ON THE PLOT
    q = 'a = ' + format(a, '1.3f') + ' V +/- ' + format(err_a, '1.3f') + ' V'
    m = 'b = ' + format(b * 1e3, '1.2f') + ' +/- ' + format(err_b * 1e3, '1.2f') + ' nF$^{-1}$'
    chisq = '$\chi^{2}$ / ndf = ' + format(chi2, '1.2f') + ' / ' + format(len(data['charge']) - len(par_lin), '1.0f') 
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
    #fig.savefig('../Plots/Catena/catena_linearity.png', dpi = 300, facecolor = 'white')
    
    plt.show()

####### READ DATA
def get_data(file_name):

    df = pd.read_csv(file_name, index_col = False, header = None, sep = '\t')
    df.index = np.arange(1, len(df)+1)

    return df


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


def bode_plot(df, sim):

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
    XMIN = 7
    XMAX = 1.3 * 1e5
    YMIN = -27
    YMAX = 27

    RESXMIN = XMIN
    RESXMAX = XMAX
    RESYMIN = -0.4
    RESYMAX = 0.4

    # ARANCIONE
    data1 = df.iloc[:6, :]

    # BLU
    data2 = df.iloc[19:, :]

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

    ## BLU
    for i in range(len(par2)):
        try:
            error2.append(np.absolute(cov2[i][i])**0.5)
        except:
            error2.append( 0.00 )

    ## ARANCIONE
    fit_par1 = par1
    fit_err1 = np.array(error1)

    # BLU
    fit_par2 = par2
    fit_err2 = np.array(error2)

    ## ARANCIONE
    c = fit_par1[0]
    d = fit_par1[1]
    err_c = fit_err1[0]
    err_d = fit_err1[1]

    ## BLU
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
    ax1.plot(sim['f'], sim['H'], color = '#4b00ff', linewidth = 1, linestyle = '-', label = 'Simulation')

    # PLOT FIT FUNCTIONS
    ax1.plot(np.arange(XMIN, XMAX + 1, 1), lin(np.log10(np.arange(XMIN, XMAX+1, 1)), *par1), color = '#FF4B00', linewidth = 2, linestyle = 'dashed', label = 'y = c + dx')
    ax1.plot(np.arange(XMIN, XMAX + 1, 1), lin(np.log10(np.arange(XMIN, XMAX+1, 1)), *par2), color = '#00b4ff', linewidth = 2, linestyle = 'dashed', label = 'y = a + bx')

    # DRAW INTERSECTION LINE
    # ax1.vlines(x = x_int, ymin = YMIN, ymax = y_int, color = '#000000', linestyle = 'dotted')

    # PRINT FIT RESULTS ON THE PLOT

    # BLU
    q2 = 'a = ' + format(e, '1.1f') + ' +/- ' + format(err_e, '1.1f') + ' dB'
    m2 = 'b = ' + format(f, '1.1f') + ' +/- ' + format(err_f, '1.1f') + ' dB/dec'
    chisq2 = '$\chi^{2}$ / ndf = ' + format(chi22, '1.0f') + ' / ' + format(len(data2['log10f (dec)']) - 2, '1.0f') 
    sigmap2 = '\u03C3$_{post}$ = ' + format(sigma_post2, '1.2f') + ' dB'

    # ARANCIONE
    q1 = 'c = ' + format(c, '1.2f') + ' +/- ' + format(err_c, '1.2f') + ' dB'
    m1 = 'd = ' + format(d, '1.2f') + ' +/- ' + format(err_d, '1.2f') + ' dB/dec'
    chisq1 = '$\chi^{2}$ / ndf = ' + format(chi21, '1.2f') + ' / ' + format(len(data1['log10f (dec)']) - 2, '1.0f') 
    sigmap1 = '\u03C3$_{post}$ = ' + format(sigma_post1, '1.2f') + ' dB'


    ax1.text(0.07, 0.72, 'Fit Parameters', fontsize = 22, fontweight = 'bold', transform=ax1.transAxes)

    # ARANCIONE
    ax1.text(0.07, 0.23, q1 + '\n' + m1 + '\n' + chisq1 + '\n' + sigmap1, fontsize = 18, color = '#000000', transform = ax1.transAxes, 
            bbox = dict( facecolor = '#FF4B00', edgecolor = '#FF4B00', alpha = 0.1, linewidth = 2 ))

    # BLU        
    ax1.text(0.07, 0.47, q2 + '\n' + m2 + '\n' + chisq2 + '\n' + sigmap2, fontsize = 18, color = '#000000', transform = ax1.transAxes, 
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
    ax1.set_title('Catena Elettronica - Bode Plot', fontsize=32)

    # AXIS LABELS
    # ax1.set_xlabel('frequency (Hz)', fontsize = 0, loc = 'right')
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
    ax2.tick_params(axis = 'both', which = 'major', labelsize = 22, direction = 'in', length = 10, pad = 5)
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
    #fig.savefig('../Plots/Catena/bode_plot.png', dpi = 300, facecolor = 'white')
    
    plt.show()


####### FREQUENZA DI TAGLIO STIMATA CON BODE
def freq_taglio_bode():

    print( 'Frequenza di Taglio Bode ft_bode = ' + format(ft_bode * 1e-3, '.2f') + ' +/- ' + format(sigma_ft_bode * 1e-3, '.2f') + '  kHz')
    

####### READ BODE SIMULATION
def get_bode_sim(filename):

    data = pd.read_csv(filename, sep = '\t', index_col = False)

    return data
