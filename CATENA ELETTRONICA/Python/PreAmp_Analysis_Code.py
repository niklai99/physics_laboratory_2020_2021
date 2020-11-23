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

    print('Qth =  ' + format(Qth * 1e12, '1.3f') + ' +/- ' + format(sigma_Qth * 1e12, '1.3f') + '  pC')

####### STIMA TEORICA DEL TEMPO CARATTERISTICO
def tau_teorico():

    global tau_th
    global sigma_tau_th

    tau_th = Rf * Cf
    sigma_tau_th = np.sqrt( (Cf * sigma_Rf)**2 + (Rf * sigma_Cf)**2 )

    print('\u03C4th =  ' + format(tau_th * 1e6, '1.3f') + ' +/- ' + format(sigma_tau_th * 1e6, '1.3f') + '  \u03BCs')

####### STIMA TEORICA DI VMAX
def Vmax_teorico():

    global Vmax_th
    global sigma_Vmax_th

    Vmax_th = Qth / Cf
    sigma_Vmax_th = np.sqrt( (sigma_Qth / Cf)**2 + (Qth * sigma_Cf / Cf**2)**2 )

    print('Vmax,th =  ' + format(Vmax_th * 1e3, '1.3f') + ' +/- ' + format(sigma_Vmax_th * 1e3, '1.3f') + '  mV')

