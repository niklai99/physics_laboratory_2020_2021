import sys 
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit



def main(arg):

    filename=arg # contains data

    # read data
    data = pd.read_csv(filename, sep = '\t', header = None,
                         names = ['X', 'Y','errY'])

    plt.errorbar(data.X,data.Y,yerr=data.errY,fmt='.')


    plt.show()

    return




if __name__ == "__main__":
   main(sys.argv[1])


