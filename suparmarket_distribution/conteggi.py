import numpy as np                          #numeracci
from matplotlib import pyplot as plt        #grafici
from scipy.optimize import curve_fit        #fit
from scipy.stats import chi2                #per calcolare il p_value
import matplotlib as mpl                    #pgf
from scipy.stats import poisson
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

def analisiCampione(l, nome=None):
    fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True, height_ratios=[3, 1])
    #calcolo media campione
    media_camp = l.mean()

    #calcolo numero campioni
    N = len(l)

    #deviazione std media
    s = l.std(ddof=1)

    print(rf'Media campione osservazioni: {media_camp:.2f}')
    print(rf'Numero conteggi:{N}')
    print(rf'Deviazione standard della media:{s:.2f}')

    bins = np.arange(l.min() - 0.5, l.max() + 1.5)

    #l = array delle occorrenze
    oss, _, _ = ax1.hist(l, bins=bins, rwidth=0.25, label='Osservati')

    #calcolo poissoniana
    k  = np.arange(l.min(), l.max() +1)
    exp_poisson = N * poisson.pmf(k, media_camp)

    #residui
    residui = oss - exp_poisson

    print(f'oss:{np.sum(oss)}, poisson:{np.sum(exp_poisson)}')
    

    #normalizza i residui (divido per la radice dei conteggi attesi) statistica poisson
    residui = residui / np.sqrt(exp_poisson)

    #chi2 e pvalue. dof = gradi_liberta - 1 (perché conoscendo il numero di tutti i bin tranne l'ultimo, si può ricavare) - nparametri stimati
    dof = len(k) - 1 - 1                     #in questo caso ho stimato la media  
    chi2_calc = np.sum(residui ** 2)
    print(rf"chi^2: {chi2_calc} dof:{dof}")
    chi2_norm = chi2_calc / dof
    p_value = chi2.sf(chi2_calc, dof)

    print(rf'$\chi^2$ norm = {chi2_norm:.2f}' '\n' rf'p-value = {p_value:.2f}')

    #plot
    ax1.bar(k - 0.3, exp_poisson, width=0.25, color='#ff7f0e', label='Poisson')
    ax1.plot([], [], ' ', label=rf'$\chi^2$ norm: {chi2_norm:.2f}')
    ax1.plot([], [], ' ', label=rf'p-value: {p_value:.2f}')
    ax1.legend(loc='upper right')
    ax1.set_ylabel('frequenza')
    ax2.errorbar(k, residui, fmt='o', yerr=1)
    ax2.axhline(0, color='black', linestyle='dashed')
    ax2.grid()
    ax2.set_ylabel('Residui std')
    ax2.set_xlabel('Occorrenze')

    if img:
        plt.savefig(nome)
        plt.close(fig)
    else:
        plt.show()

dataset = {
    'set1' : [2, 3, 2, 2, 1, 2, 2, 2, 1, 1, 
              3, 3, 3, 1, 3, 3, 2, 1, 4, 1, 
              2, 3, 2, 2, 0, 1, 4, 2, 3, 2],
    'set2' : [4, 1, 2, 3, 4, 4, 1, 3, 3, 3,
              3, 2, 2, 2, 3, 2, 3, 7, 1, 1,
              5, 6, 5, 1, 5, 1, 2, 1, 4, 3],
}

dataset['set3'] = list(np.array(dataset['set1']) + np.array(dataset['set2']))

for nome, dati in dataset.items():
    arr = np.array(dati)
    
    if img:
        analisiCampione(arr, f"{nome}.pgf")
    else:
        analisiCampione(arr)   
