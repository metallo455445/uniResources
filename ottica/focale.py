import numpy as np                          #numeracci
from matplotlib import pyplot as plt        #grafici
from scipy.optimize import curve_fit        #fit
from scipy.stats import chi2                #per calcolare il p_value
import matplotlib as mpl                    #pgf
import sys

#####################################################################################################################################################

#blocco variabili passate come argomento
if len(sys.argv) > 1:
    img = sys.argv[1]       #bool, se flaso usa ax1.show, se vero usa stmpa pgf

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
        "pgf.preamble": r"\usepackage{amsmath}"
    })

#####################################################################################################################################################
def retta(x, a, b):
    return a*x + b

misure_dirette = np.array([[  7.,   9.,  10.,   8.,   6.],            #pi
                           [26.8, 32.2, 44.1, 25.0, 22.2],            #qi min
                           [34.2, 47.1, 53.8, 51.3, 27.4]] )          #qi max

# aggiungo i centimetri dovuti alle basi delle lenti
misure_dirette[0] += 4.5
misure_dirette[1] += 4.8
misure_dirette[2] += 4.8

print(misure_dirette)

#converto in metri
misure_dirette = misure_dirette / 100

# come da richiesta preso con -
misure_dirette[0] = - misure_dirette[0]                               

# misure sugli assi
asse_y = 1 / ((misure_dirette[1] + misure_dirette[2]) / 2)                 
asse_x = 1 / misure_dirette[0] 

print(f"assex: {asse_x} \n assey: {asse_y}")

# l'errore su y è la dispersione masssima
errori_y = ((misure_dirette[2] - misure_dirette[1]) / 2) / (((misure_dirette[1] + misure_dirette[2]) / 2) ** 2)

#l'errore su x è la risoluzione del metro a anastro: 1 mm propagato
errori_x = 0.001 / (misure_dirette[0] ** 2)

#print incertezze
print(rf'Incertezza x:{errori_x}, incertezza y:{errori_y}')

#fit
popt, pcov = curve_fit(retta, asse_x, asse_y, sigma=errori_y, absolute_sigma=True)
print("Parametri fit:", popt)

# rappresentazione fit
fit = retta(asse_x, popt[0], popt[1])

# residui
residui = asse_y - fit

# normalizza i residui
residui = residui / errori_y

# chi2
chi2_cal = np.sum(residui ** 2)
dof = len(misure_dirette[0]) - len(popt)
chi2_ridotto = chi2_cal / dof
p_val = chi2.sf(chi2_cal, dof)

#stampe debug
print(rf'chi2 calcolato: {chi2_cal:.2f}, dof: {dof}')
print(pcov)

#RICORDATI CHE SE USI LA DISTRIBUZIONE UNIFROME POI IL CHI^2 É DIVERSO... aspettazione = dof, VARIANZA = 4/5 dof

# plot
fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True, height_ratios=[3, 1])

ax1.errorbar(asse_x, asse_y, fmt='o', yerr=errori_y, xerr=errori_x, label='punti misurati')
ax1.plot(asse_x, fit, label='best fit')
ax1.plot([], [], ' ', label=rf'$\chi^2$ridotto: {chi2_ridotto:.2f}')
ax1.plot([], [], ' ', label=rf'p-value: {p_val:.2f}')
ax1.set_ylabel(r'$1/q \quad [\text{m}^{-1}]$')
ax1.grid()
ax1.legend()

ax2.errorbar(asse_x, residui, yerr=1, label='residui ridotti', fmt='o')
ax2.grid()
ax2.axhline(0, ls='dashed', color='black')
ax2.set_xlabel(r'$-1/p \quad [\text{m}^{-1}]$')
ax2.set_ylabel(r'$\sigma$')
#####################################################################################################################################################
#sstampa dei grafici automaticamente differenziata
if img:
    fig.savefig('focale.pgf')
else:
    plt.show()
#####################################################################################################################################################