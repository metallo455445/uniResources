import time
import numpy as np                          #numeracci
from matplotlib import pyplot as plt        #grafici
from scipy.optimize import curve_fit        #fit

def gauss(x, A, mu, sigma):
    #return A * np.exp(-(x - mu) ** 2 / (2. * sigma **2))
    return A /sigma / np.sqrt(2. * np.pi) * np.exp(-(x - mu) ** 2 / (2. * sigma **2))    
    #gaussiana normalizzata ad A
    
#con somma cumulativa, mostra la "traiettoria" con la quale è arrivato nel punto finale
def randomWalkCUM(num_steps = 1000):
    phi = np.random.uniform(0., 2. * np.pi, size=num_steps)
    x = np.cumsum(np.cos(phi))
    y = np.cumsum(np.sin(phi))
    return x, y

#con somma classica, ricavo solo l'ultimo elemento della somma cumulativa ovvero le coordinate del punto finale
def randomWalkFIN(num_steps = 1000):
    phi = np.random.uniform(0., 2. * np.pi, size=num_steps)
    x = np.sum(np.cos(phi))
    y = np.sum(np.sin(phi))
    return x, y
#somma dic ose randomiche, teorema centrae del limite -> distribuzione gaussiana
#la media è 0 perchè la somma delle medie di variabili casuali
#la varianza della somma delle varianze SE E SOLO SE sono indipendenti
#x e y non sono indiepndenti

N = 10000
n = 1000

#fw rad(2ln2) = 2.35
xFIN = []
yFIN = []

for i in range(N):
    x, y = randomWalkFIN(n)
    xFIN.append(x)
    yFIN.append(y)

o_i, bins, _ = plt.hist(x, bins=100)
bin_centers = (bins[:-1] + bins[1:]) / 2
#ho motivo di pensare che questa distribuzione non possa essere generata da una gaussiana don media e varianza (trovati prima)
#faccio un test del chi2 per verificare che queta distribuzione è compatibile con un modello ben fissato

e_i = gauss(bin_centers, N, 0., np.sqrt(n/2.))
#quando faccio un istogramma non è normalizzato 

#il contenuto delle colonne dell'istogramma fluttua, si può calcolare la deviazione standard 
# x, y = randomWalkCUM(100000)
# plt.plot(x, y)
# plt.gca().set_aspect('equal')
plt.plot(o_i, N)
plt.show()
#prova