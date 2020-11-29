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



tau_sh_th : float
tau_sh_th1 : float
tau_sh_th2 : float

sigma_tau_sh_th : float
sigma_tau_sh_th1 : float
sigma_tau_sh_th2 : float





####### PROPAGAZIONE SUI CURSORI
def propagazione_cursori(Vdiv, measure):

    sigma = np.sqrt( (0.04 * Vdiv)**2 + (0.015 * measure)**2)

    return sigma



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
    
