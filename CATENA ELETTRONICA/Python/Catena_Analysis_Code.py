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
sigma_G_sper = np.sqrt( (sigma_D / R1a)**2 + (sigma_D / R2a)**2 + 2 * sigma_L**2)

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


####### PROPAGAZIONE SUI CURSORI
def propagazione_cursori(Vdiv, measure):

    sigma = np.sqrt( (0.04 * Vdiv)**2 + (0.015 * measure)**2 )

    return sigma


####### LINEAR FUCTION
def lin(x, a, b):  
    return a + b * x



##### CALCOLO COMPATIBILITA
def compatib(x, y, errx, erry):

    comp = np.abs( x - y ) / np.sqrt( errx**2 + erry**2 )

    return comp
