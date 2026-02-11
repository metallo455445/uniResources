#py ./catenaria/FITcatenaria.py ./catenaria/coord.txt      
#                                                                        ^percorso del txt coord
import numpy as np
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit
import sys

if len(sys.argv) > 1:
    coord_path = sys.argv[1]
else:
    print("AAAAAAAAAAA")

data = np.loadtxt(coord_path, delimiter=" ")

#calcolo deviazione standard
diff = data[:,1] - np.mean(data[:,1])
devStdY = np.sqrt(np.pow(diff, 2)/len(data[:,1]))
print(f"dev stdr Y: {np.mean(devStdY)}")

diff = data[:,0] - np.mean(data[:,0])
devStdX = np.sqrt(np.pow(diff, 2)/len(data[:,0]))
print(f"dev stdr X: {np.mean(devStdX)}")

def parabola(x, a, b, c):
    return a * np.power(x, 2) + b * x + c

# La derivata della parabola è 2ax + b
def derivata_parabola(x, a, b):
    return 2 * a * x + b

# Dati
x_data = data[:, 0]
y_data = data[:, 1]
# Nota: usa i singoli valori di incertezza o gli array se sono puntuali
sx = devStdX  
sy = devStdY

# --- PROCESSO DI FIT ITERATIVO ---

# 1. Fit iniziale (solo errori su Y)
popt, pcov = curve_fit(parabola, x_data, y_data, sigma=sy, absolute_sigma=True)

# 2. Raffinamento con Incertezza Efficace
for i in range(5):  # Di solito converge in 2-3 step
    a, b, c = popt
    
    # Calcolo della derivata nei punti x dei dati
    df_dx = derivata_parabola(x_data, a, b)
    
    # Formula dell'incertezza efficace
    # sigma_eff = sqrt( sigma_y^2 + (df/dx * sigma_x)^2 )
    sigma_eff = np.sqrt(sy**2 + (df_dx * sx)**2)
    
    # Nuovo fit pesato con la sigma efficace
    popt, pcov = curve_fit(parabola, x_data, y_data, sigma=sigma_eff, absolute_sigma=True)

a_fin, b_fin, c_fin = popt
perr = np.sqrt(np.diag(pcov)) # Errori sui parametri

print(f"Parametri ottimizzati: a={a_fin}, b={b_fin}, c={c_fin}")

#fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True, height_ratios=[3, 1])

# #--- Grafico Best Fit---
# #ax1.figure('Grafico catenaria')
# ax1.errorbar(data[:,0], data[:,1], devStdY, devStdX, fmt='+')
# ax1.grid(which='both', ls='dashed', color='gray')
# x = np.linspace(0., 700., 1000)
# ax1.plot(x, parabola(x, a_fin, b_fin, c_fin))
#######################################################################################

# --- Calcolo Residui e Chi2 ---
# Usiamo i dati originali per il calcolo, non i 1000 punti del plot
y_model = parabola(data[:, 0], a_fin, b_fin, c_fin)

# Calcoliamo la sigma_eff finale per pesare correttamente i residui
df_dx_final = derivata_parabola(data[:, 0], a_fin, b_fin)
sigma_eff_final = np.sqrt(devStdY**2 + (df_dx_final * devStdX)**2)

# Residui normalizzati (pull)
residui = (data[:, 1] - y_model) / sigma_eff_final

# Chi2 e gradi di libertà
chi2 = np.sum(residui**2)
ndof = len(data[:, 0]) - len(popt)  # N punti - N parametri
chi2_ridotto = chi2 / ndof

print(f"chi2: {chi2:.2f}")
print(f"Gradi di libertà (ndof): {ndof}")
print(f"chi2 ridotto: {chi2_ridotto:.2f}")

# --- Grafico ---
fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True, height_ratios=[3, 1], figsize=(8, 8))

# Grafico Best Fit
ax1.errorbar(data[:,0], data[:,1], yerr=devStdY, xerr=devStdX, fmt='+', alpha=0.5, label='Dati')
x_plot = np.linspace(min(data[:,0]), max(data[:,0]), 1000)
ax1.plot(x_plot, parabola(x_plot, a_fin, b_fin, c_fin), color='red', label='Fit parabola')
ax1.legend()
ax1.grid(ls='dashed')

# Grafico Residui
ax2.errorbar(data[:,0], residui, yerr=1, fmt='o', markersize=2, alpha=0.5) # yerr=1 perché sono normalizzati-> avendo diviso in unità di sigma mi basta 1 come errore
ax2.axhline(0, color='black', linestyle='dashed')
ax2.set_ylabel("Residui norm. ($\sigma$)")
ax2.grid(ls='dashed')

plt.tight_layout()
plt.show()