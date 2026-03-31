#py oscillazioni/singlePendolo1.py oscillazioni/esperienzaOscillazioni/run\ pendolo\ singolo/0309_000091/0309_000091_data.txt 70 oscillazioni/esperienzaOscillazioni/run\ pendolo\ singolo/0309_000092/0309_000092_data.txt 60
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

# Blocco variabili passate come argomento
if len(sys.argv) == 5:
    percorsoData1 = sys.argv[1]
    skippedrows1 = int(sys.argv[2])
    percorsoData2 = sys.argv[3]
    skippedrows2 = int(sys.argv[4])
else:
    # Valori di default di sicurezza se lo script è eseguito senza argomenti
    print("Attenzione: argomenti mancanti, uso i valori di default.")
    percorsoData1 = "data1.csv"   
    skippedrows1 = 0
    percorsoData2 = "data2.csv"
    skippedrows2 = 0

#####################################################################################################################################################

# --- SET DI DATI 1 ---
data1 = np.loadtxt(percorsoData1, delimiter=',', skiprows=skippedrows1)

mask_A1 = data1[:, 0] == 4.0  # Tutte le righe dove il Pin è 4
mask_B1 = data1[:, 0] == 5.0  # Tutte le righe dove il Pin è 5

tempiA1 = data1[mask_A1, 1]
dataA1 = data1[mask_A1, 2]

tempiB1 = data1[mask_B1, 1]
dataB1 = data1[mask_B1, 2]

indici_massimi1, _ = find_peaks(dataA1) 
tempi_massimi1 = tempiA1[indici_massimi1]
posizioni_massimi1 = dataA1[indici_massimi1]

# --- PLOT 1 ---
plt.figure(1)
plt.plot(tempiA1, dataA1, label="Dati Sensore A (Set 1)")
plt.plot(tempi_massimi1, posizioni_massimi1, "x", color="red", label="Massimi (Set 1)") 

# --- SET DI DATI 2 ---
# CORRETTO: ricaricavi percorsoData1! Ora carica il 2.
data2 = np.loadtxt(percorsoData2, delimiter=',', skiprows=skippedrows2)

mask_A2 = data2[:, 0] == 4.0  
mask_B2 = data2[:, 0] == 5.0  

tempiA2 = data2[mask_A2, 1]
dataA2 = data2[mask_A2, 2]

tempiB2 = data2[mask_B2, 1]
dataB2 = data2[mask_B2, 2]

indici_massimi2, _ = find_peaks(dataA2) 
tempi_massimi2 = tempiA2[indici_massimi2]
posizioni_massimi2 = dataA2[indici_massimi2]

# --- PLOT 2 --- (sulla stessa figura)
plt.figure(2)
plt.plot(tempiA2, dataA2, label="Dati Sensore A (Set 2)", alpha=0.7) # Alpha per renderlo un po' trasparente se si sovrappone
plt.plot(tempi_massimi2, posizioni_massimi2, "o", color="orange", label="Massimi (Set 2)") 
plt.legend()


# --- CALCOLO DELTA TEMPI E OMEGA ---
# Usiamo np.diff per calcolare la differenza tra elementi adiacenti.
# Lo facciamo separatamente per evitare di contare il salto temporale tra la fine del Set 1 e l'inizio del Set 2
deltaTempo1 = np.diff(tempi_massimi1)
deltaTempo2 = np.diff(tempi_massimi2)

# Uniamo i delta tempo in un unico array
deltaTempo_TOT = np.concatenate((deltaTempo1, deltaTempo2))

print("Vettore dei delta tempo (Periodi):")
print(deltaTempo_TOT)

# Calcolo Omega
omega_media = (2 * np.pi) / np.mean(deltaTempo_TOT)
print(f"Omega media = {omega_media:.4f} rad/s")

#####################################################################################################################################################
plt.show()
# se si vuole usare plt.show commentare la prossima riga
# plt.savefig('nome.pgf')
#####################################################################################################################################################