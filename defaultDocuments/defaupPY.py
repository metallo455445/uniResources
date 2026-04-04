import numpy as np                          #numeracci
from matplotlib import pyplot as plt        #grafici
from scipy.optimize import curve_fit        #fit
from scipy.stats import chi2                #per calcolare il p_value
import matplotlib as mpl                    #pgf
import sys

#####################################################################################################################################################

#blocco variabili passate come argomento
if len(sys.argv) > 1:
    img = sys.argv[1]       #bool, se flaso usa plt.show, se vero usa stmpa pgf

    #convertitore da stringa a bool
    if img == 'True' or img == 'true':
        img = True
    elif img == 'False' or img == 'false':
        img = False
    else:
        print("Errore nell'inserimento del parametro 1: selezionato in automatico False")
        img = False

else:
    img = False   #se fallisce l'inserimento

#####################################################################################################################################################
#blocco preambolo pgf, automaticamnte selezionato
if img:
    mpl.use("pgf")

    plt.rcParams.update({
        "font.family": "serif",     
        "text.usetex": True,
        "pgf.rcfonts": False,
    })

#####################################################################################################################################################

#metti il tuo codice qui

#####################################################################################################################################################
#sstampa dei grafici automaticamente differenziata
if img:
    plt.savefig('nome.pgf')
else:
    plt.show()
#####################################################################################################################################################