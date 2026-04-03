import random
import numpy as np
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit
from scipy.stats import chi2

#definizione funzione calcolo sep finale random walk
def random_walk(num_steps=1000):
    phi = np.random.uniform(0., 2. * np.pi, size=num_steps)
    x = np.sum(np.cos(phi))
    y = np.sum(np.sin(phi))
    return x, y

#definizione funzioni per le distribuzioni
def gauss(x, A, mu, sigma):
   return A / sigma / np.sqrt(2. * np.pi) * np.exp(-(x - mu) ** 2 / (2. * sigma ** 2))

def distribuzione_esponenziale(d, larg_bin):
    return (np.exp(-d/n) / n) * len(x) * larg_bin

def distribuzione_rayleigh(d, larg_bin, n_passi, N_tot):
    return ((2 * d / n_passi) * np.exp(-(d**2) / n_passi)) * N_tot * larg_bin

#dichiarazione costanti
N = 100000
n = 1000
bin_width = 2.
d2_bin_width = 10.
range_x_dist = 80.
max_cicles = 1000

#richiamo il random walk N volte 
x = []
y = []
for i in range(N):
    x_i, y_i = random_walk(n)
    x.append(x_i)
    y.append(y_i)


###############Sudio della distribuzione della x###############
plt.figure(1)
#crea l'istogramma per graficare le x osservate
x_osservate, x_bins, _ = plt.hist(x, bins=np.arange(-range_x_dist, range_x_dist, bin_width), label="osservati")
#array con la coordinata x dei centri di tutti i bin
x_bin_centers = (x_bins[:-1] + x_bins[1:]) / 2.
#trova i valori di aspettazione della x dalla formula di una distribuzione gaussiana
x_aspettate = gauss(x_bin_centers, N * bin_width, 0., np.sqrt(n / 2.))


ndof = len(x_osservate)
chi2_1 = np.sum((x_osservate - x_aspettate) ** 2. / x_aspettate)
p_value_1 = chi2.sf(chi2_1, ndof)
mediaX = np.mean(x)
print(f"Media x: {mediaX}")
print(f"Deviazione std: {np.std(x)} aspettata = {np.sqrt(n / 2)}")
print(f"Chi-squared: {chi2_1:.2f} / {ndof} dof")

plt.plot(x_bin_centers, x_aspettate, 'r-', label=rf'aspettati ' '\n' rf'$\chi^2$ / dof: {chi2_1:.2f} / {ndof}' '\n' rf'p-value: {p_value_1:.2f}' '\n' rf'Media x: {mediaX:.2f}' '\n' rf'Dev std: {np.std(x):.2f} exp: {np.sqrt(n / 2):.2f}')
plt.legend()
plt.xlabel('Coord x')
plt.ylabel('Frequenza')

########################studio del d^2#########################

fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True, height_ratios=[3, 1])
d2 = np.empty(len(x))
for i in range(len(x)):
    d2[i] = x[i]**2 + y[i]**2

d2_oss, d2_x_bins, _ = ax1.hist(d2, bins=np.arange(0., 4000., d2_bin_width), label=rf'$d^2$ osservata')
d2_x_bin_centers = (d2_x_bins[:-1] + d2_x_bins[1:]) / 2.
d2_aspettati = distribuzione_esponenziale(d2_x_bin_centers, d2_bin_width)

d2_residui = d2_oss - d2_aspettati
d2_sigma_residui = np.sqrt(np.maximum(d2_oss, 1))
#normalizzazione dei residui
#d2_residui = d2_residui / d2_sigma_residui

ax1.plot(d2_x_bin_centers, d2_aspettati,"r-", color="red", label=rf'$d^2$ aspettati (distribuzione esponenziale)')
ax1.legend()
ax1.set_ylabel('Frequenza')
ax2.axhline(0, color='black', linestyle='dashed')
ax2.errorbar(d2_x_bin_centers, d2_residui, yerr=d2_sigma_residui, fmt='.')
ax2.grid()
ax2.set_xlabel(rf'$d^2$')
ax2.set_ylabel('Residui (osservati - attesi)')

plt.figure(2)

########################studio della d#########################


fig2, (ax3, ax4) = plt.subplots(2, 1, sharex=True, height_ratios=[3, 1])
d = np.sqrt(d2)

d_oss, d_x_bins, _ = ax3.hist(d, bins=np.arange(0., 80., bin_width), label=rf'$d$ osservati')
d_x_bin_centers = (d_x_bins[:-1] + d_x_bins[1:]) / 2.
d_aspettati = distribuzione_rayleigh(d_x_bin_centers, bin_width, n, len(x))

d_residui = d_oss - d_aspettati
d_sigma_residui = np.sqrt(np.maximum(d_oss, 1))

ax3.plot(d_x_bin_centers, d_aspettati, "r-", color="red", label=rf'$d$ aspettati')
ax3.legend()
ax3.set_ylabel('Frequenza')
ax4.axhline(0, color='black', linestyle='dashed')
ax4.errorbar(d_x_bin_centers, d_residui, yerr=d_sigma_residui, fmt='.')
ax4.grid()
ax4.set_ylabel('Residui (osservati - attesi)')
ax4.set_xlabel(rf'$d$')

plt.figure(3)

#######################studio della d(n)#######################
# dist = []
# for i in range(max_cicles):
#     x_i, y_i = random_walk(i)
#     dist.append(np.sqrt(x_i**2 + y_i**2))
# assex = np.arange(0, max_cicles)

val_n = np.arange(10, max_cicles, 20)
run_per_n = 200

dist_medie = []
error_medie = []
for i in val_n:
    attuale_d = np.empty(run_per_n)
    for j in range(run_per_n):
        x_i, y_i = random_walk(i)
        attuale_d[j] = (np.sqrt(x_i**2 + y_i**2))
    
    media_d = np.mean(attuale_d)
    dist_medie.append(media_d)

    std_d = np.std(attuale_d, ddof=1)
    err_media = std_d / np.sqrt(run_per_n)
    error_medie.append(err_media)

dist_medie = np.array(dist_medie)
error_medie = np.array(error_medie)

fig3, (ax5, ax6) = plt.subplots(2, 1, sharex=True, height_ratios=[3, 1])
ax5.errorbar(val_n, dist_medie, yerr=error_medie, label=rf'$d(n)$' ,fmt='o')
ax5.plot(val_n, (np.sqrt(np.pi)/2) * np.sqrt(val_n), "r-",color='red', label=r'E[d]=$\frac {\sqrt{\pi}} {2} \sqrt{n}$')
ax5.set_ylabel(rf'$d$')
ax5.legend()
residui = dist_medie - (np.sqrt(np.pi)/2) * np.sqrt(val_n)
#normalizzo i residui
residui = residui/error_medie
ax6.axhline(0, color='black', linestyle='dashed')
ax6.errorbar(val_n, residui, yerr=error_medie, fmt='.')
ax6.grid()
ax6.set_xlabel(rf'$n$')
ax6.set_ylabel(rf'Residui normalizzati [$\sigma$]')

plt.figure(4)
plt.show()