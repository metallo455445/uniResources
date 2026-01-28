import numpy as np
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit

misten = 10

baricentro = 502 #[mm] distanza del baricentro dal lato corto
errorBar = 1 #[mm]
                                                #!v 520 !!!!
distanzeFori = np.array([19, 119, 219, 319, 419, 520, 620, 720, 820, 920]) #[mm] a partirre dal lato corto
errorFori = 1 #[mm]

distanzeFori = distanzeFori + 0.25                  #distanza dal centro del foro
distanzeBaricentro = distanzeFori - baricentro      #lontananza dal baricentro
distanzeBaricentro = np.abs(distanzeBaricentro)     #valori assolute delle distanze
distanzeBaricentro = distanzeBaricentro / 1000      #converte in metri
print(f"distanze bar: {distanzeBaricentro}")

                        #  |Gabri pre caf  | Gabri post caf     |Mat pre caf  | Mat post caf
TenOscillazioni = np.array([[16.18, 15.91, 15.95, 15.99, 15.91, 15.05, 15.92, 16.07, 16.04, 15.99],
                           [15.89, 15.43, 15.53, 15.59, 15.37, 15.28, 15.39, 15.74, 15.17, 15.47],
                           [15.27, 14.89, 14.98, 15.05, 14.93, 14.95, 15.14, 15.27, 15.04, 15.12],
                           [15.84, 16.09, 15.86, 15.77, 15.89, 16.09, 15.87, 16.01, 15.80, 16.16],
                           [21.09, 20.99, 21.17, 21.15, 21.14, 21.38, 21.07, 21.23, 21.16, 21.59],
                           #sbarra rovesciata
                           [38.93, 39.31, 38.86, 38.97, 38.92, 39.35, 39.13, 39.15, 39.27, 39.11],
                           [17.67, 17.63, 17.71, 17.75, 17.60, 16.11, 17.82, 17.60, 17.89, 18.03],
                           [15.31, 15.48, 15.58, 15.25, 15.29, 15.27, 15.27, 15.17, 15.43, 15.29],
                           [15.18, 15.17, 15.03, 15.07, 15.03, 15.07, 15.08, 15.53, 15.06, 15.06],
                           [15.81, 15.55, 15.63, 15.53, 15.46, 15.77, 15.70, 15.72, 15.59, 15.53]])

SingleOscillazioni = TenOscillazioni / 10
print(SingleOscillazioni)

#calcola la media per ogni riga
mediariga = np.empty(10)                                 #<---- 10 !!!
for i in range(mediariga.size):
    mediariga[i] = np.mean(SingleOscillazioni[i, :])
print(mediariga, "\n#####")

#sottraggo alla media
sballo = SingleOscillazioni.copy()
sballo = mediariga[:, None] - SingleOscillazioni
print(sballo)

#calcolo deviazione standard per ogni foro
devStd = np.empty(10)                                   #<--- 10 !!!
for i in range(devStd.size):
    diff = SingleOscillazioni[i, :] - mediariga[i]
    devStd[i] = np.sqrt(np.sum(diff**2) / (len(diff) - 1))
print(f"deviazione standard: {devStd}")

d = distanzeBaricentro                    
sigma_d = np.full(d.shape, 0.001)
T = mediariga          
sigma_T = devStd     #np.full(mediariga.shape, 0.001)             

# Definizione dell’accelerazione di gravita‘.
g = 9.81

def period_model(d, l):
    """Modello per il periodo del pendolo."""
    return 2.0 * np.pi * np.sqrt((l**2.0 / 12.0 + d**2.0) / (g * d))

popt, pcov = curve_fit(period_model, d, T, sigma=sigma_T#, absolute_sigma=True
                       )
l0 = popt[0]
sigma_l = np.sqrt(pcov[0, 0])
sigma_T
# Confrontate i parametri di best fit con la vostra misura diretta!
print(f'l0 = {l0} +/- {sigma_l}')

fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True, height_ratios=[3, 1])

# --- Grafico fit ---
ax1.errorbar(d, T, yerr=None, xerr=sigma_d, fmt='o', label="errore metro[1mm]", color="C0")
ax1.errorbar(d, T, yerr=sigma_T, fmt="o", label="deviazione standard", color="C0")
x = np.linspace(min(d), max(d), 200)
ax1.plot(x, period_model(x, l0), color="orange")
ax1.set_ylabel("Periodo [s]")
ax1.grid(ls='dashed')
ax1.legend()

# --- Grafico residui ---
residui = (T - period_model(d, l0))/ sigma_T
#chi2 = np.sum(np.power((T - period_model(d,l0)/(sigma_T)),2))
chi2 = np.sum(np.power(residui,2))
ax2.axhline(0, color='black', linestyle='dashed')
ax2.errorbar(d, residui, sigma_T, fmt='o')
ax2.set_xlabel("d [m]")
ax2.set_ylabel("Residui [sigma]")
ax2.grid(ls='dashed')
print(f"chi2: {chi2}")
print(f"lung popt {len(popt)}")
plt.tight_layout()
plt.show()
