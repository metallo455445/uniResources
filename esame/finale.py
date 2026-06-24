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

nMisure = 9    #n° di misure da selezionare, si ricorda di modificare di conseguenza distanzeFori e TenOscillazioni
                #nello specifico: eliminare i valori nei blocchi centrali di distanzeFori (520, poi 419, ...) e commentare la riga corrispondente in TenOscillazioni
baricentro = 521 #[mm] distanza del baricentro dal lato corto
errorBar = 1 #[mm]
                                                #497
distanzeFori = np.array([97, 197, 297, 397, 597, 697, 797, 897, 997]) #[mm] a partirre dal lato corto
errorFori = 1 #[mm]

distanzeFori = distanzeFori + 0.25                  #distanza dal centro del foro
distanzeBaricentro = distanzeFori - baricentro      #lontananza dal baricentro
distanzeBaricentro = np.abs(distanzeBaricentro)     #valori assolute delle distanze
distanzeBaricentro = distanzeBaricentro / 1000      #converte in metri
print(f"distanze bar: {distanzeBaricentro}")

TenOscillazioni = np.array([
                            [16.08, 16.10, 16.11, 16.02, 16.08],#1 -0.05
                            [15.70, 15.63, 15.62, 15.74, 15.56],#2
                            [15.80, 15.88, 15.91, 15.97, 15.87],#3
                            [18.65, 18.60, 18.62, 18.63, 18.55],#4 +0.05
                            #[21.09, 20.99, 21.17, 21.15, 21.14],
                            #[38.96, 38.92, 39.05, 38.77, 38.91],#5
                            #ribalta#
                            [22.67, 22.76, 22.70, 22.92, 22.85],#6
                            [16.77, 16.87, 16.91, 16.72, 16.86],#7
                            [15.71, 15.72, 15.69, 15.69, 15.76],#8
                            [15.74, 15.92, 15.94, 15.86, 15.83],#9
                            [16.44, 16.35, 16.36, 16.42, 16.35]#10
                            ])

SingleOscillazioni = TenOscillazioni / 10
#divido per 10 perché questi sono i tempi ti 10 oscillazioni, dividendo per 10 abbiami il periodo di una sola oscillazione
print(SingleOscillazioni)

#calcola la media per ogni riga
#ogni riga si traduce in ogni distanza, trovo la media delle oscillazioni per ogni distanza
mediariga = np.empty(nMisure)                                 #<---- 10 !!!
for i in range(mediariga.size):
    mediariga[i] = np.mean(SingleOscillazioni[i, :])
print(mediariga, "\n#####")

#totalmente opzionale, controllo quanto sballa dalla media osgn misurazione
sballo = SingleOscillazioni.copy()
sballo = mediariga[:, None] - SingleOscillazioni
print(sballo)

#calcolo deviazione standard per ogni foro
devStd = np.empty(nMisure)                                   #<--- 10 !!!
for i in range(devStd.size):
    diff = SingleOscillazioni[i, :] - mediariga[i]
    devStd[i] = np.sqrt(np.sum(diff**2) / (len(diff)*(len(diff) - 1)))      #corretto -> da calcolo della dev.std campionaria a quello della media
print(f"deviazione standard: {devStd}")

# devStd = np.empty(nMisure)
# for i in range(nMisure):
#     devStd[i] = SingleOscillazioni[i, :].std(ddof=1)
#     devStd[i] = devStd[i] / np.sqrt(nMisure)

d = distanzeBaricentro                    
sigma_d = np.full(d.shape, 0.001)   #erore del metro a nastro: 1mm = 0.001 m
T = mediariga          #periodi delle singole oscillazioni per ogni foro
sigma_T = devStd                  

# Definizione dell’accelerazione di gravita‘.
g = 9.81

def period_model(d, l):
    """Modello per il periodo del pendolo."""
    return 2.0 * np.pi * np.sqrt((l**2.0 / 12.0 + d**2.0) / (g * d))

def modello_derivato(d, l):
    return np.pi * np.sqrt((g * d) / (((l**2)/12) + d**2)) * 1/g * (1 - ((l**2) / (12 * d**2)))

popt, pcov = curve_fit(period_model, d, T, sigma=sigma_T, absolute_sigma=True)
l0 = popt[0]
sigma_l = np.sqrt(pcov[0, 0])
# Confrontate i parametri di best fit con la vostra misura diretta!
print(f'l0 = {l0} +/- {sigma_l}')

fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True, height_ratios=[3, 1])

residui = (T - period_model(d, l0))/ sigma_T
#chi2 = np.sum(np.power((T - period_model(d,l0)/(sigma_T)),2))
chi2Stat = np.sum(np.power(residui,2))
p_value = chi2.sf(chi2Stat, (len(d)-len(popt))) #calcolo p-value
chi2_rid = chi2Stat / (len(d)-len(popt))

# --- Grafico fit ---
ax1.errorbar(d, T, yerr=None, xerr=sigma_d, fmt='o', label="errore metro[1mm]", color="C0")
ax1.errorbar(d, T, yerr=sigma_T, fmt="o", label="deviazione standard", color="C0")
x = np.linspace(min(d), max(d), 200)
#ax1.plot(x, period_model(x, l0), color="orange")
ax1.plot(x, period_model(x, l0), color="orange", label=rf"$\chi^2_r = {chi2_rid:.2f}$" "\n" rf"$l_0 = {l0:.3f} \pm {sigma_l:.3f}$ m" "\n"rf"$p-value = {p_value:.3f}$")
ax1.set_ylabel("Periodo [s]")
ax1.grid(ls='dashed')
ax1.legend()

# --- Grafico residui ---
ax2.axhline(0, color='black', linestyle='dashed')
ax2.errorbar(d, residui, sigma_T, fmt='o')
ax2.set_xlabel("d [m]")
ax2.set_ylabel("Residui [sigma]")
ax2.grid(ls='dashed')
print(f"chi2: {chi2Stat}")
print(f"lung popt {len(popt)}")
print(f"p-value: {p_value}")
plt.tight_layout()

print(f'errori y: {sigma_T}')
erroriConf = 0.001
erroriConf = erroriConf * modello_derivato(d, l0)
print(f'errori x: {erroriConf}')
for i in range(len(erroriConf)):
    if sigma_T[i] > np.abs(erroriConf[i] * 10):
        print('ok')
    else:
        print(f'ATTENZIONE indice {i}')


#errore efficace
for i in range(5):
    best_l = popt[0]

    df_dx = modello_derivato(d, best_l)

    errore_efficace = np.sqrt(sigma_T**2 + (df_dx * sigma_d)**2)

    try:
        popt, pcov = curve_fit(period_model, d, T, p0=popt, sigma=errore_efficace, absolute_sigma=True)
    except:
        pass #

l0 = popt[0]

fig, (ax3, ax4) = plt.subplots(2, 1, sharex=True, height_ratios=[3, 1])

residui = (T - period_model(d, l0))/ sigma_T
#chi2 = np.sum(np.power((T - period_model(d,l0)/(sigma_T)),2))
chi2Stat = np.sum(np.power(residui,2))
p_value = chi2.sf(chi2Stat, (len(d)-len(popt))) #calcolo p-value
chi2_rid = chi2Stat / (len(d)-len(popt))

# --- Grafico fit ---
ax3.errorbar(d, T, yerr=None, xerr=sigma_d, fmt='o', label="errore metro[1mm]", color="C0")
ax3.errorbar(d, T, yerr=sigma_T, fmt="o", label="deviazione standard", color="C0")
x = np.linspace(min(d), max(d), 200)
#ax1.plot(x, period_model(x, l0), color="orange")
ax3.plot(x, period_model(x, l0), color="orange", label=rf"$\chi^2_r = {chi2_rid:.2f}$" "\n" rf"$l_0 = {l0:.3f} \pm {sigma_l:.3f}$ m" "\n"rf"$p-value = {p_value:.3f}$")
ax3.set_ylabel("Periodo [s]")
ax3.grid(ls='dashed')
ax3.legend()

# --- Grafico residui ---
ax4.axhline(0, color='black', linestyle='dashed')
ax4.errorbar(d, residui, sigma_T, fmt='o')
ax4.set_xlabel("d [m]")
ax4.set_ylabel("Residui [sigma]")
ax4.grid(ls='dashed')
print(f"chi2: {chi2Stat}")
print(f"lung popt {len(popt)}")
print(f"p-value: {p_value}")
plt.tight_layout()

#####################################################################################################################################################
#sstampa dei grafici automaticamente differenziata
if img:
    plt.savefig('nome.pgf')
else:
    plt.show()
#####################################################################################################################################################