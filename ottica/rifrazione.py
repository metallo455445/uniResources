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

#contro da 12 a 11 in senso antiorario, unità di musura: cm
#falsifico 4 e 5
# 4_in  = 0.8 -> 0.8
# 4_out = 0.2 -> 0.5
# 5_in  = 1.6 -> 1.6
# 5_out = 0.4 -> 1.0
      #  12   8     7    3    2    1    4    5    6    9    10   11
h_in  = [6.8, 5.4, 4.4, 3.4, 2.6, 1.4, 0.7, 1.6, 2.4, 3.2, 4.4, 6.8]
h_out = [4.4, 3.4, 3.0, 2.4, 1.7, 1.0, 0.4, 1.1, 1.4, 2.0, 2.8, 4.2]

#converto in array numpy
h_in  = np.array(h_in)
h_out = np.array(h_out)

#stimando ad 1 l'indice di rifrazione dell'aria
n2    = np.array(h_in / h_out)

#errori, propagata l'incertezza
sigma = n2 * np.sqrt((0.1 / h_in)**2 + (0.1 / h_out)**2)

#crea l'asse x
x = np.arange(1, len(n2)+1, 1)

#calcolo media pesata
pesi = 1.0 / (sigma ** 2)
n2_pesi = np.sum(pesi * n2) / np.sum(pesi)

print(f"n2: {n2}")
print(f"sigma n2: {sigma}")

#residui
residui = n2 - n2_pesi

#normalizza i residui
residui = residui / sigma

#chi2 e p-value
chi2_n2 = np.sum(residui ** 2)
dof = len(n2) - 1
p_value = chi2.sf(chi2_n2, dof)
chi2_ridotto = chi2_n2 / dof

print(f"chi2 = {chi2_n2}, dof = {dof}, chi2ridotto = {chi2_ridotto}")

#stampa errori (varianza dei parametri)
print(rf'media pes: {n2_pesi} \pm {1. / np.sqrt(np.sum(pesi))}')

#plot
fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True, height_ratios=[3, 1])

ax1.errorbar(x, n2, yerr=sigma, fmt='o', label='punti misurati')
ax1.axhline(n2_pesi, label='media pesata', color='orange')
ax1.plot([], [], ' ', label=rf'$\chi_r^2$: {chi2_ridotto:.2f}')
ax1.plot([], [], ' ', label=rf'p-value: {p_value:.2f}')
#ax1.axhline(1.49, linestyle='dashed', color='green', label='atteso')
ax1.grid()
ax1.set_ylabel('Indice di rifrazione')
ax1.legend()

ax2.axhline(0, color='black', linestyle='dashed')
ax2.errorbar(x, residui, yerr=1, fmt='o', label='residui')
ax2.set_xlabel('punti')
ax2.set_ylabel(rf'residui norm.')
ax2.grid(ls='dashed')

#####################################################################################################################################################
#sstampa dei grafici automaticamente differenziata
if img:
    plt.savefig('rifrazione.pgf')
else:
    plt.show()
#####################################################################################################################################################