#py oscillazioni/singlePendoloSmorzato.py oscillazioni/esperienzaOscillazioni/run\ pendolo\ smorzato/0309_000095/0309_000095_data.txt 60 1 2.0
import numpy as np                          #numeracci
from matplotlib import pyplot as plt        #grafici
from scipy.optimize import curve_fit        #fit
from scipy.signal import find_peaks
from scipy.stats import chi2
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
if len(sys.argv) == 5:
    percorsoData1 = sys.argv[1]
    skippedrows1 = int(sys.argv[2])
    tailRows = int(sys.argv[3])
    prominenza = float(sys.argv[4])
    # percorsoData2 = sys.argv[3]
    # skippedrows2 = int(sys.argv[4])
else:
    # Valori di default di sicurezza se lo script è eseguito senza argomenti
    print("Attenzione: argomenti mancanti, uso i valori di default.")
    percorsoData1 = "data1.csv"   
    skippedrows1 = 0
    # percorsoData2 = "data2.csv"
    # skippedrows2 = 0

#####################################################################################################################################################

def exp(t, lamda, b, offset):
    return offset + np.exp(-lamda*t) * b 

errorBalda = 1

data = np.loadtxt(percorsoData1, delimiter=',', skiprows=skippedrows1)

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

indici_massimi, _ = find_peaks(dataA, prominence=prominenza) 
tempi_massimi = tempiA[indici_massimi]
posizioni_massimi = dataA[indici_massimi]

plt.figure(1)
plt.plot(tempiA, dataA, label="Dati Sensore A")
plt.plot(tempi_massimi, posizioni_massimi, "x", color="red", label="Massimi") 


#gli ultimi valori selezionati da find_peaks non sono solo piscchi, elimina gli ultimi n valori
max_selected_data = posizioni_massimi[:-tailRows]
max_selected_times = tempi_massimi[:-tailRows]

#imposto a 0 il tempo iniziale
tempi_fit = max_selected_times - max_selected_times[0]

#sistemo i valor iniziali
offset_iniziale = max_selected_data[-1]     #valore più piccolo che dovrei trovare
amplificazione_iniziale = max_selected_data[0] - offset_iniziale
lamdaStimato = 0.01

popt, pcov = curve_fit(exp, tempi_fit, max_selected_data, 
                       p0=[lamdaStimato, amplificazione_iniziale, offset_iniziale],
                       bounds=(0, np.inf))
lamda0 = popt[0]
bi = popt[1]
offset0 = popt[2]

perr = np.sqrt(np.diag(pcov))
print(f"{perr}")

#calcolo residui, chi2 e p-value
residui = (max_selected_data - exp(tempi_fit, lamda0, bi, offset0)) / errorBalda 
chi2Calc = np.sum(np.power(residui,2))
p_value = chi2.sf(chi2Calc, (len(tempi_fit)-len(popt)))

#plot del fit 
fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True, height_ratios=[3, 1])
ax1.errorbar(tempi_fit, max_selected_data,errorBalda, xerr=None, fmt="o", label="Massimi selezionati")
ax1.plot(tempi_fit, exp(tempi_fit, lamda0, bi, offset0), label=rf"$\chi^2/dof = {chi2Calc:.2f}/{len(tempi_fit)-len(popt)}$" "\n" rf"$p-value = {p_value:.3f}$")
ax1.legend()

#plot residui
ax2.axhline(0, color='black', linestyle='dashed')
ax2.errorbar(tempi_fit, residui, errorBalda, fmt='o')
ax2.set_xlabel("tempo [s]")
ax2.set_ylabel("Residui [sigma]")
ax2.grid(ls='dashed')
print(f"chi2: {chi2Calc}")

# plt.figure(2)
# plt.plot(tempiB, dataB)
#####################################################################################################################################################
plt.show()
#se si vuole usare plt.show commentare la prossima riga
#plt.savefig('nome.pgf')
#####################################################################################################################################################