import numpy as np
from matplotlib import pyplot as plt
from scipy.stats import chi2
import matplotlib as mpl
import sys

#sezione totalmente opzionale usata per stampare i grafici in formato pgf
if len(sys.argv) > 1:
    img = sys.argv[1]       #bool, se False usa plt.show, se True usa stmpa pgf
else:
    img = False             #se fallisce l'inserimento

if img:
    mpl.use("pgf")

    plt.rcParams.update({
        "font.family": "serif",     
        "text.usetex": True,
        "pgf.rcfonts": False,
    })


#definizione funzione calcolo step finale random walk
def random_walk(num_steps=1000):
    #genera randomicamente un angolo tra 0 e 2pi-greco
    phi = np.random.uniform(0., 2. * np.pi, size=num_steps)
    #per ogni angolo somma in due array distinti il coseno (array x) ed il seno (array y). 
    # In questo modo ottengo direttamente le coordinate del punto finale alleggerendo l'esecuzione
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
max_n = 1000
min_n = 10
step_width = 20
run_per_n = 200

#richiamo il random walk N volte 
x = []
y = []
for i in range(N):
    x_i, y_i = random_walk(n)
    x.append(x_i)
    y.append(y_i)


###############Sudio della distribuzione della x###############
fig1 = plt.figure(1)

#crea l'istogramma per graficare le x osservate
x_osservate, x_bins, _ = plt.hist(x, bins=np.arange(-range_x_dist, range_x_dist, bin_width), label="osservati")

#array con la coordinata x dei centri di tutti i bin
x_bin_centers = (x_bins[:-1] + x_bins[1:]) / 2.

#trova i valori di aspettazione della x dalla formula di una distribuzione gaussiana
x_aspettate = gauss(x_bin_centers, N * bin_width, 0., np.sqrt(n / 2.))

#test chi2 + p-value per ulteriore verifica 
ndof = len(x_osservate)
chi2_1 = np.sum((x_osservate - x_aspettate) ** 2. / x_aspettate)
p_value_1 = chi2.sf(chi2_1, ndof)

#calcolo e deviazione standard per lo studio della bontà della distribuzione
mediaX = np.mean(x)
devStd = np.std(x)

#plot grafico
plt.plot(x_bin_centers, x_aspettate, 'r-', label=rf'aspettati ' '\n' rf'$\chi^2$ / dof: {chi2_1:.2f} / {ndof}' '\n' rf'p-value: {p_value_1:.2f}' '\n' rf'Media x: {mediaX:.2f}' '\n' rf'Dev std: {devStd:.2f} exp: {np.sqrt(n / 2):.2f}')
plt.legend()
plt.xlabel('Coord x')
plt.ylabel('Frequenza')

########################studio del d^2#########################
fig2, (ax1, ax2) = plt.subplots(2, 1, sharex=True, height_ratios=[3, 1])

#calcolo array delle distranze al quadrato [d^2 = x^2 + y^2]
d2 = np.empty(len(x))
for i in range(len(x)):
    d2[i] = x[i]**2 + y[i]**2

#crea l'istogramma per la distribuzione delle distanze al quadrato
d2_oss, d2_x_bins, _ = ax1.hist(d2, bins=np.arange(0., 4000., d2_bin_width), label=rf'$d^2$ osservata')

#coordinate x sei centri di ogni bin dell'istogramma
d2_x_bin_centers = (d2_x_bins[:-1] + d2_x_bins[1:]) / 2.

#calcola i valori di aspettazione dal modello esponenziale
d2_aspettati = distribuzione_esponenziale(d2_x_bin_centers, d2_bin_width)

#calcolo dei residui
d2_residui = d2_oss - d2_aspettati
d2_sigma_residui = np.sqrt(np.maximum(d2_oss, 1))

#plot del secondo grafico + residui
ax1.plot(d2_x_bin_centers, d2_aspettati,"r-", color="red", label=rf'$d^2$ aspettati (distribuzione esponenziale)')
ax1.legend()
ax1.set_ylabel('Frequenza')
ax2.axhline(0, color='black', linestyle='dashed')
ax2.errorbar(d2_x_bin_centers, d2_residui, yerr=d2_sigma_residui, fmt='.')
ax2.grid()
ax2.set_xlabel(rf'$d^2$')
ax2.set_ylabel('Residui (osservati - attesi)')

########################studio della d#########################
fig3, (ax3, ax4) = plt.subplots(2, 1, sharex=True, height_ratios=[3, 1])

#array delle distanze
d = np.sqrt(d2)

#crea l'istogramma della distribuzione delle distanze
d_oss, d_x_bins, _ = ax3.hist(d, bins=np.arange(0., 80., bin_width), label=rf'$d$ osservati')

#array delle coordinate x dei centri dei bin 
d_x_bin_centers = (d_x_bins[:-1] + d_x_bins[1:]) / 2.

#calcola i valori di aspettazione dalla distribuzione di rayleigh
d_aspettati = distribuzione_rayleigh(d_x_bin_centers, bin_width, n, len(x))

#calcolo dei residui
d_residui = d_oss - d_aspettati
d_sigma_residui = np.sqrt(np.maximum(d_oss, 1))

#plot del terzo grafico + residui
ax3.plot(d_x_bin_centers, d_aspettati, "r-", color="red", label=rf'$d$ aspettati')
ax3.legend()
ax3.set_ylabel('Frequenza')
ax4.axhline(0, color='black', linestyle='dashed')
ax4.errorbar(d_x_bin_centers, d_residui, yerr=d_sigma_residui, fmt='.')
ax4.grid()
ax4.set_ylabel('Residui (osservati - attesi)')
ax4.set_xlabel(rf'$d$')

#######################studio della d(n)#######################
#suddivide l'inervallo da min_n a max_n in steps di grandezza step_width
#es: se min_n = 0, max_n = 50 e step_width = 10 --> val_n = ([0, 10, 20, 30, 40, 50])
val_n = np.arange(min_n, max_n, step_width)

dist_medie = []
error_medie = []
for i in val_n:
    #crea un array momentaneo dove immagazzina le distanze per ogni ciclo di i
    attuale_d = np.empty(run_per_n)

    #esegure il ranom walk con un numero di passi dato dall'inidce i per run_per_n volte e salva la distanza ottenuta ad ogni run
    for j in range(run_per_n):
        x_i, y_i = random_walk(i)
        attuale_d[j] = (np.sqrt(x_i**2 + y_i**2))
    
    #calcola la media di delle distanze ottenute per ogni step e le salva nella lista dist_medie
    media_d = np.mean(attuale_d)
    dist_medie.append(media_d)

    #calcola l'errore standard della media e lo salva nella lista error_medie
    #ddof=1 per lo stimatore corretto della deviazione standard campionaria
    std_d = np.std(attuale_d, ddof=1)
    err_media = std_d / np.sqrt(run_per_n)
    error_medie.append(err_media)

#converte le liste in array di numpy per semplicità
dist_medie = np.array(dist_medie)
error_medie = np.array(error_medie)

fig4, (ax5, ax6) = plt.subplots(2, 1, sharex=True, height_ratios=[3, 1])

#plot del grafico 
ax5.errorbar(val_n, dist_medie, yerr=error_medie, label=rf'$d(n)$' ,fmt='o')
ax5.plot(val_n, (np.sqrt(np.pi)/2) * np.sqrt(val_n), "r-",color='red', label=r'E[d]=$\frac {\sqrt{\pi}} {2} \sqrt{n}$')
ax5.set_ylabel(rf'$d$')
ax5.legend()

#calcolo dei residui
residui = dist_medie - (np.sqrt(np.pi)/2) * np.sqrt(val_n)

#normalizzo i residui per avere l'assey y dei residui in unità dell'errore
residui = residui/error_medie

#plot dei residui
ax6.axhline(0, color='black', linestyle='dashed')
ax6.errorbar(val_n, residui, yerr=error_medie, fmt='.')
ax6.grid()
ax6.set_xlabel(rf'$n$')
ax6.set_ylabel(rf'Residui normalizzati [$\sigma$]')

#blocco di salvataggio dei grafici
if img:
    fig1.savefig('distribuzione_x.pgf')
    fig2.savefig('distribuzione_d2.pgf')
    fig3.savefig('distribuzione_d.pgf')
    fig4.savefig('distribuzione_d_n.pgf')
else:
    plt.show()
