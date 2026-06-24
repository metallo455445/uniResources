import numpy as np
import matplotlib as mpl
# Imposta il backend per esportare in pgf
mpl.use("pgf")
mpl.rcParams.update({
    "pgf.texsystem": "pdflatex",
    'font.family': 'serif',
    'text.usetex': True,
    'pgf.rcfonts': False,
})
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.stats import chi2
import os

# --- 1. FUNZIONI MODELLO ---

def pendolo_smorzato(t, A, tau, omega, phi, offset):
    return A * np.exp(-t / tau) * np.cos(omega * t + phi) + offset

def battimenti(t, A, tau, omega_p, omega_b, phi_p, phi_b, offset):
    decadimento = np.exp(-t / tau)
    portante = np.cos(omega_p * t + phi_p)
    modulante = np.cos(omega_b * t + phi_b)
    return A * decadimento * portante * modulante + offset

def carica_dati(filename):
    dati = np.loadtxt(filename, skiprows=4)
    return dati[:, 0], dati[:, 1], dati[:, 2], dati[:, 3]

# ATTENZIONE: Inserisci qui l'errore reale della tua misurazione sulle y
SIGMA_Y = 1.0  

# Percorso cartella (aggiornato al tuo)
cartella_download = r'/home/matteo/Documenti/uni/lab/oscillazioni/runs'
#file_battimenti = os.path.join(cartella_download, 'battimenti119.txt')

# --- 2. CALCOLO SILENZIOSO DELLE STIME (Come nel tuo script) ---
# Fittiamo rapidamente fase e controfase per ottenere le stime perfette

# Fase
t_f, x_f, _, _ = carica_dati(os.path.join(cartella_download, 'fase117.txt'))
mask_f = (t_f > 2) & (t_f < 55)
popt_f, _ = curve_fit(pendolo_smorzato, t_f[mask_f], x_f[mask_f], p0=[120, 80, 4.4, 0, 420])

# Controfase
t_c, x_c, _, _ = carica_dati(os.path.join(cartella_download, 'controfase118.txt'))
mask_c = (t_c > 2) & (t_c < 55)
popt_c, _ = curve_fit(pendolo_smorzato, t_c[mask_c], x_c[mask_c], p0=[120, 80, 4.9, 0, 420])

# --- 3. ANALISI BATTIMENTI ---
file_battimenti = os.path.join(cartella_download, 'battimenti119.txt')
t_b, x_b, _, _ = carica_dati(file_battimenti)
mask_b = (t_b > 2) & (t_b < 55)
t_b, x_b = t_b[mask_b], x_b[mask_b]

# Le tue stime vincenti
wp_guess = (popt_f[2] + popt_c[2]) / 2
wb_guess = abs(popt_f[2] - popt_c[2]) / 2

p0_b = [115, 70, wp_guess, wb_guess, 0, 0, 428]
popt_b, pcov_b = curve_fit(battimenti, t_b, x_b, p0=p0_b)

# --- 4. STATISTICHE E RESIDUI ---
fit_y = battimenti(t_b, *popt_b)
residui = x_b - fit_y
residui_norm = residui / SIGMA_Y

dof = len(t_b) - len(popt_b)
chi_square = np.sum(residui_norm**2)
chi_square_red = chi_square / dof
err_chi_square_red = np.sqrt(2 / dof) 
p_value = chi2.sf(chi_square, dof)

# --- 5. GRAFICO ---
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 7), 
                               gridspec_kw={'height_ratios': [3, 1]}, 
                               sharex=True)

# Pannello superiore: Dati e Fit (identico al tuo)
ax1.scatter(t_b, x_b, s=1, color='gray', alpha=0.5, label='Dati Battimenti')
ax1.plot(t_b, fit_y, color='green', label='Fit Battimenti')

# Inviluppo per i battimenti
inv = popt_b[0] * np.exp(-t_b / popt_b[1]) * np.cos(popt_b[3] * t_b + popt_b[5]) + popt_b[6]
ax1.plot(t_b, inv, '--r', label='Inviluppo modulante')
ax1.plot(t_b, -inv + 2*popt_b[6], '--r')

# Etichetta stat
stats_label = (f"$\\chi^2_{{red}} = {chi_square_red:.2f} \\pm {err_chi_square_red:.2f}$\n"
               f"$p$-value = {p_value:.2e}")
ax1.plot([], [], ' ', label=stats_label)

ax1.set_title(f"Fenomeno dei Battimenti ($\\omega_p$={popt_b[2]:.3f}, $\\omega_b$={popt_b[3]:.3f})")
ax1.set_ylabel("Ampiezza")
ax1.legend(loc='upper right')
ax1.grid(True, alpha=0.3)

# Pannello inferiore: Residui normalizzati
ax2.scatter(t_b, residui_norm, s=1, color='black', alpha=0.5)
ax2.axhline(0, color='red', linestyle='--')
ax2.set_xlabel("Tempo (s)")
ax2.set_ylabel("Residui norm.")
ax2.grid(True, alpha=0.3)

plt.tight_layout()

# Salvataggio
nome_file_out = 'battimenti_definitivo.pgf'
plt.savefig(nome_file_out, format='pgf')
plt.close()

# Stampa riassuntiva
print(f"--- RISULTATI BATTIMENTI ---")
print(f"Battimento (WP):    {popt_b[2]:.3f} rad/s")
print(f"Battimento (WB):    {popt_b[3]:.3f} rad/s")
print(f"Chi^2 ridotto:      {chi_square_red:.3f} ± {err_chi_square_red:.3f}")
print(f"p-value:            {p_value:.3e}")
print(f"Grafico esportato in {nome_file_out}")