import numpy as np                          #numeracci
from matplotlib import pyplot as plt        #grafici
from scipy.optimize import curve_fit        #fit
import matplotlib as mpl                    #pgf

#####################################################################################################################################################
#decommentare fino alla riga 19 per scaricare i file in .pgf Inoltre è necessario il comando plt.savefig("pendolo.pgf") a fine documento
mpl.use("pgf")

plt.rcParams.update({
    "font.family": "serif",     
    "text.usetex": True,
    "pgf.rcfonts": False,
})
#####################################################################################################################################################

#metti il tuo codice qui

#####################################################################################################################################################
#se si vuole usare plt.show commentare la prossima riga
plt.savefig('nome.pgf')
#####################################################################################################################################################