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

    sigma = np.sqrt( (0.04 * Vdiv)**2 + (0.015 * measure)**2)

    return sigma


####### LINEAR FUCTION
def lin(x, a, b):  
    return a + b * x



##### CALCOLO COMPATIBILITA
def compatib(x, y, errx, erry):

    comp = np.abs( x - y ) / np.sqrt( errx**2 + erry**2 )

    return comp
