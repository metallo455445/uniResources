import numpy as np
from matplotlib import pyplot as plt
from scipy.signal import find_peaks
import sys

#################################################################################
# FUNZIONE PRINCIPALE DI ELABORAZIONE
#################################################################################
def elabora_canale(data_matrix, pin, temp_min, temp_max, prom):
    """
    Filtra per Pin, isola la run più lunga, ordina gli array di dati, trova i picchi e taglia il dominio.
    Restituisce i dati già pronti per il plot.
    """
    # 1. separa le letture dei due sensore dai file
    mask = data_matrix[:, 0] == pin
    tempi_raw = data_matrix[mask, 1]
    data_raw  = data_matrix[mask, 2]
    
    # 2. Trova e isola la run più luna (sono stato costretto ad aggiungere questa parte perché so erano fuse più run insieme)
    differenze_tempo = np.diff(tempi_raw)
    salti = np.where(differenze_tempo < 0)[0]
    
    # Creiamo gli indici di inizio e fine per ogni porzione di run
    inizi = np.insert(salti + 1, 0, 0)
    fini = np.append(salti + 1, len(tempi_raw))
    
    # Calcoliamo quanto è lunga ogni run e troviamo l'indice di quella con più punti
    lunghezze = fini - inizi
    indice_run_migliore = np.argmax(lunghezze)
    
    # Selezioniamo solo i dati di quella specifica run
    inizio_clean = inizi[indice_run_migliore]
    fine_clean = fini[indice_run_migliore]
    
    tempi_clean = tempi_raw[inizio_clean:fine_clean]
    data_clean = data_raw[inizio_clean:fine_clean]

    # 3. Sorting basati sul tempo
    indici_ordinati = np.argsort(tempi_clean)
    tempi_ord = tempi_clean[indici_ordinati]
    data_ord = data_clean[indici_ordinati]
    
    # 4. Ricerca dei picchi
    indici_massimi, _ = find_peaks(data_ord, prominence=prom)
    tempi_massimi = tempi_ord[indici_massimi]
    pos_massimi = data_ord[indici_massimi]
    
    # 5. Restrizione del dominio (limite inferiore: temp_min, limite superiore: temp_max)
    start_idx = np.searchsorted(tempi_ord, temp_min)
    end_idx = np.searchsorted(tempi_ord, temp_max)
    start_idx_max = np.searchsorted(tempi_massimi, temp_min)
    end_idx_max = np.searchsorted(tempi_massimi, temp_max)
    
    tempi_final = tempi_ord[start_idx:end_idx]
    data_final = data_ord[start_idx:end_idx]
    tempi_massimi_final = tempi_massimi[start_idx_max:end_idx_max]
    pos_massimi_final = pos_massimi[start_idx_max:end_idx_max]
    
    # Restituisce anche i RAW per debuggin
    return tempi_final, data_final, tempi_massimi_final, pos_massimi_final, tempi_raw, data_raw


#################################################################################
# GESTIONE ARGOMENTI
#################################################################################
if len(sys.argv) > 8:
    percorsoData1 = sys.argv[1]
    percorsoData2 = sys.argv[2]
    tempMin1      = float(sys.argv[3])
    tempMax1      = float(sys.argv[4])
    tempMin2      = float(sys.argv[5])
    tempMax2      = float(sys.argv[6])
    prom1         = float(sys.argv[7])
    prom2         = float(sys.argv[8])
else:
    sys.exit("Errore: argomenti da riga di comando insufficienti.")

#################################################################################
# CARICAMENTO ED ELABORAZIONE
#################################################################################
# Prova a caricare data1 con la virgola, se fallisce usa gli spazi
try:
    data1 = np.loadtxt(percorsoData1, delimiter=',', skiprows=4)
except ValueError:
    data1 = np.loadtxt(percorsoData1, skiprows=4)

# Prova a caricare data2 con la virgola, se fallisce usa gli spazi
try:
    data2 = np.loadtxt(percorsoData2, delimiter=',', skiprows=4)
except ValueError:
    data2 = np.loadtxt(percorsoData2, skiprows=4)

# Chiamo la funzione 4 volte (una per ogni traccia!)
t1A, d1A, tm1A, pm1A, t1A_raw, d1A_raw = elabora_canale(data1, 4.0, tempMin1, tempMax1, prom1)
t1B, d1B, tm1B, pm1B, _, _             = elabora_canale(data1, 5.0, tempMin1, tempMax1, prom1)

t2A, d2A, tm2A, pm2A, _, _             = elabora_canale(data2, 4.0, tempMin2, tempMax2, prom2)
t2B, d2B, tm2B, pm2B, _, _             = elabora_canale(data2, 5.0, tempMin2, tempMax2, prom2)

#################################################################################
# PLOT
#################################################################################
fig, axs = plt.subplots(2, 2)
axs[0,0].plot(t1A, d1A, label="Set 1 - Pin 4")
axs[0,0].plot(tm1A, pm1A, "x", color="red", label="Picchi")
axs[0,0].set_title('Run 1 sensore A')

#plt.figure(2)
axs[0,1].plot(t1B, d1B, color="orange", label="Set 1 - Pin 5")
axs[0,1].plot(tm1B, pm1B, "x", color="red")
axs[0,1].set_title('Run 1 sensore B')

#plt.figure(3)
axs[1,0].plot(t2A, d2A, label="Set 2 - Pin 4")
axs[1,0].plot(tm2A, pm2A, "x", color="red")
axs[1,0].set_title('Run 2 sensore A')

#plt.figure(4)
axs[1,1].plot(t2B, d2B, color="orange", label="Set 2 - Pin 5")
axs[1,1].plot(tm2B, pm2B, "x", color="red")
axs[1,1].set_title('Run 2 sensore B')

# Grafico di debug per la run 1A
plt.figure(1)
plt.figure(2)
plt.plot(t1A_raw, d1A_raw, marker='.', linestyle='', markersize=2)
plt.title("Dati Grezzi (Senza Ordine e Senza Linee)")

#################################################################################
# Calcolo pulsazioni angolari
#################################################################################
deltaTempiA = np.concatenate((np.diff(t1A), np.diff(t2A)))
omega_media = (2 * np.pi) / np.mean(deltaTempiA)
print(f"omega media A:{omega_media}")

plt.show()