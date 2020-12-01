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

    ADC_amplitude = ADC_max - ADC_min

    b = 1 / ADC_amplitude
    a = -b * ADC_min

    err_b = b * propagazione_cursori(0.2, 1)
    err_a = ADC_min * err_b

    return a, b, err_a, err_b


def max_values_calib(data):

    a, b, err_a, err_b = arduino_calib()

    data['V (V)'] = a + b * data['max_values']
    data['err V (V)'] = np.sqrt( err_a**2 + err_b**2 )


def linearity_plot(data):
    # FIG SETTINGS AND AXES
    fig = plt.figure(figsize=(16,8))
    ax1 = fig.add_subplot(1, 1, 1)
    
    # PERFORM THE FIT
    par_lin, cov_lin = curve_fit(f = lin, xdata = data['charge'], ydata = data['V (V)'], sigma=data['err V (V)'], absolute_sigma=True)
    func = lin(data['charge'], *par_lin)
    
    # PLOT DATA
    ax1.plot(data['charge'], data['V (V)'], color = '#000000', linewidth = 0, marker = '.', markersize = 15, label = 'Data')
    
    # PLOT FIT FUNCTION
    ax1.plot(np.arange(20, 200, 0.1), lin(np.arange(20, 200, 0.1), *par_lin), color = '#FF4B00', linewidth = 2, linestyle = 'dashed', label = 'Fit')
    
    # PLOT TITLE
    ax1.set_title('Catena Elettronica - Vmax vs Qin', fontsize = 32)
    
    # AXIS LABELS
    ax1.set_xlabel('Qin (pF)', fontsize = 26, loc = 'right')
    ax1.set_ylabel('Vmax (V)', fontsize = 26, loc = 'top')
    
    # AXIS TICKS
    ax1.tick_params(axis = 'both', which = 'major', labelsize = 22, direction = 'in', length = 10)
    ax1.tick_params(axis = 'both', which = 'minor', labelsize = 22, direction = 'in', length = 5)
    ax1.set_xticks(ticks = ax1.get_xticks(), minor = True)
    ax1.set_yticks(ticks = ax1.get_yticks(), minor = True)
    ax1.minorticks_on()
    
    # PLOT RANGE
    ax1.set_xlim(left = 20, right = 200)
    ax1.set_ylim(bottom = 0.25, top = 2.75)
    
    # SAVE FIGURE
    #fig.savefig('../Logbook/catena_linearity.png', dpi = 300, facecolor = 'white')
    
    plt.show()

