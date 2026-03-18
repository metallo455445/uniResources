import numpy as np                          #numeracci
from matplotlib import pyplot as plt        #grafici
from scipy.optimize import curve_fit        #fit
from scipy.signal import find_peaks
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
    skippedrows = int(sys.argv[2])
else:
    percorsoData = "default value"   #se fallisce l'inserimento

#####################################################################################################################################################

data = np.loadtxt(percorsoData, delimiter=',', skiprows=skippedrows)

tempiA = np.empty(int(len(data)/2))
tempiB = np.empty(int(len(data)/2))
dataA = np.empty(int(len(data)/2))
dataB = np.empty(int(len(data)/2))

mask_A = data[:, 0] == 4.0  # Tutte le righe dove il Pin è 4
mask_B = data[:, 0] == 5.0  # Tutte le righe dove il Pin è 5

tempiA = data[mask_A, 1]
dataA = data[mask_A, 2]

tempiB = data[mask_B, 1]
dataB = data[mask_B, 2]

indici_massimi, _ = find_peaks(dataA) 

tempi_massimi = tempiA[indici_massimi]
posizioni_massimi = dataA[indici_massimi]

print("omega")
print(2 * np.pi / (tempi_massimi[1] - tempi_massimi[0])) 

print(f"Ho trovato {len(indici_massimi)} picchi!")

# --- PLOT ---
plt.plot(tempiA, dataA, label="Dati Sensore A")
plt.plot(tempi_massimi, posizioni_massimi, "x", color="red", label="Massimi") # Segna i picchi con una X rossa

# plt.plot(tempiB, dataB, label="Dati Sensore B")

plt.legend()
#####################################################################################################################################################
plt.show()
# se si vuole usare plt.show commentare la prossima riga
# plt.savefig('nome.pgf')
#####################################################################################################################################################