import numpy as np                          #numeracci
from matplotlib import pyplot as plt        #grafici
from scipy.optimize import curve_fit        #fit
import matplotlib as mpl                    #pgf
import sys

#####################################################################################################################################################
#blocco preambolo pgf
#decommentare fino alla riga 16 per scaricare i file in .pgf Inoltre è necessario il comando plt.savefig("pendolo.pgf") a fine documento
# mpl.use("pgf")

# plt.rcParams.update({
#     "font.family": "serif",     
#     "text.usetex": True,
#     "pgf.rcfonts": False,
# })
#####################################################################################################################################################

#blocco variabili passate come argomento
if len(sys.argv) > 1:
    percorsoData = sys.argv[1]
    #skippedrows = sys.argv[2]
else:
    percorsoData = "default value"   #se fallisce l'inserimento

#####################################################################################################################################################

data = np.loadtxt(percorsoData, delimiter=',', skiprows=4)

mask_A = data[:, 0] == 4.0  # Tutte le righe dove il Pin è 4
mask_B = data[:, 0] == 5.0  # Tutte le righe dove il Pin è 5

tempiA_row = data[mask_A, 1]
dataA_row = data[mask_A, 2]

tempiB_row = data[mask_B, 1]
dataB_row = data[mask_B, 2]

#sort dei tempi dato che il progrmma di Baldini a volte non li mette in ordine cronologico
indici_tempiA = np.argsort(tempiA_row)
indici_tempiB = np.argsort(tempiB_row)

tempiA = tempiA_row[indici_tempiA]
dataA = dataA_row[indici_tempiA]
tempiB = tempiB_row[indici_tempiB]
dataB = dataB_row[indici_tempiB]

plt.plot(tempiA, dataA)
plt.plot(tempiB, dataB)
#####################################################################################################################################################
plt.show()
#se si vuole usare plt.show commentare la prossima riga
#plt.savefig('nome.pgf')
#####################################################################################################################################################