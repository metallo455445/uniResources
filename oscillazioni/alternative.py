import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.stats import chi2
import os
from scipy.fft import fft, fftfreq

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

# Percorso cartella
cartella_download = r'/home/matteo/Documenti/uni/lab/oscillazioni/runs'

# --- 2. ANALISI E GRAFICI ---

# Incertezza sulle y (modifica questo valore con l'errore reale del tuo strumento!)
sigma_y = 1.0  

# ==========================================
# --- A. PENDOLO SINGOLO ---
# ==========================================
file_singolo = os.path.join(cartella_download, 'singolosmorzato116.txt')
t_s, _, _, x_s = carica_dati(file_singolo)
mask_s = (t_s > 2) & (t_s < 55)
t_s, x_s = t_s[mask_s], x_s[mask_s]

p0_s = [(np.max(x_s)-np.min(x_s))/2, 40, 4.4, 0, np.mean(x_s)]
popt_s, pcov_s = curve_fit(pendolo_smorzato, t_s, x_s, p0=p0_s)

# Calcolo Statistiche Pendolo Singolo
y_fit_s = pendolo_smorzato(t_s, *popt_s)
residui_s = x_s - y_fit_s
residui_norm_s = residui_s / sigma_y
dof_s = len(t_s) - len(popt_s)
chi2_s = np.sum(residui_norm_s**2)
chi2_red_s = chi2_s / dof_s
p_val_s = chi2.sf(chi2_s, dof_s)

# Grafico Pendolo Singolo
fig_s, (ax1_s, ax2_s) = plt.subplots(2, 1, figsize=(10, 6), gridspec_kw={'height_ratios': [3, 1]}, sharex=True)

ax1_s.scatter(t_s, x_s, s=1, color='blue', alpha=0.3, label='Dati Singolo')
ax1_s.plot(t_s, y_fit_s, color='red', label='Fit Smorzato')
testo_stats_s = f"$\\chi^2_{{red}}$ = {chi2_red_s:.2f}\np-value = {p_val_s:.2e}"
ax1_s.plot([], [], ' ', label=testo_stats_s) # Trucco per aggiungere testo in legenda
ax1_s.set_title(f"Pendolo Singolo Smorzato ($\omega_0$ = {popt_s[2]:.3f} rad/s)")
ax1_s.legend()
ax1_s.grid(True, alpha=0.3)
ax1_s.set_ylabel("Ampiezza")

ax2_s.scatter(t_s, residui_norm_s, s=1, color='black', alpha=0.5)
ax2_s.axhline(0, color='red', linestyle='--')
ax2_s.set_ylabel("Residui norm.")
ax2_s.set_xlabel("Tempo (s)")
ax2_s.grid(True, alpha=0.3)


# ==========================================
# --- B. MODO IN FASE ---
# ==========================================
file_fase = os.path.join(cartella_download, 'fase117.txt')
t_f, x_f, _, _ = carica_dati(file_fase)
mask_f = (t_f > 2) & (t_f < 55)
t_f, x_f = t_f[mask_f], x_f[mask_f]

p0_f = [120, 80, 4.4, 0, 420]
popt_f, _ = curve_fit(pendolo_smorzato, t_f, x_f, p0=p0_f)

# Calcolo Statistiche Modo in Fase
y_fit_f = pendolo_smorzato(t_f, *popt_f)
residui_f = x_f - y_fit_f
residui_norm_f = residui_f / sigma_y
dof_f = len(t_f) - len(popt_f)
chi2_f = np.sum(residui_norm_f**2)
chi2_red_f = chi2_f / dof_f
p_val_f = chi2.sf(chi2_f, dof_f)

# Grafico Modo in Fase
fig_f, (ax1_f, ax2_f) = plt.subplots(2, 1, figsize=(10, 6), gridspec_kw={'height_ratios': [3, 1]}, sharex=True)

ax1_f.scatter(t_f, x_f, s=1, color='cyan', alpha=0.3, label='Dati in Fase')
ax1_f.plot(t_f, y_fit_f, color='black', label='Fit Modo Fase')
testo_stats_f = f"$\\chi^2_{{red}}$ = {chi2_red_f:.2f}\np-value = {p_val_f:.2e}"
ax1_f.plot([], [], ' ', label=testo_stats_f)
ax1_f.set_title(f"Modo Normale: In Fase ($\omega_f$ = {popt_f[2]:.3f} rad/s)")
ax1_f.legend()
ax1_f.grid(True, alpha=0.3)
ax1_f.set_ylabel("Ampiezza")

ax2_f.scatter(t_f, residui_norm_f, s=1, color='black', alpha=0.5)
ax2_f.axhline(0, color='red', linestyle='--')
ax2_f.set_ylabel("Residui norm.")
ax2_f.set_xlabel("Tempo (s)")
ax2_f.grid(True, alpha=0.3)


# ==========================================
# --- C. MODO IN CONTROFASE ---
# ==========================================
file_controfase = os.path.join(cartella_download, 'controfase118.txt')
t_c, x_c, _, _ = carica_dati(file_controfase)
mask_c = (t_c > 2) & (t_c < 55)
t_c, x_c = t_c[mask_c], x_c[mask_c]

p0_c = [120, 80, 4.9, 0, 420]
popt_c, _ = curve_fit(pendolo_smorzato, t_c, x_c, p0=p0_c)

# Calcolo Statistiche Modo in Controfase
y_fit_c = pendolo_smorzato(t_c, *popt_c)
residui_c = x_c - y_fit_c
residui_norm_c = residui_c / sigma_y
dof_c = len(t_c) - len(popt_c)
chi2_c = np.sum(residui_norm_c**2)
chi2_red_c = chi2_c / dof_c
p_val_c = chi2.sf(chi2_c, dof_c)

# Grafico Modo in Controfase
fig_c, (ax1_c, ax2_c) = plt.subplots(2, 1, figsize=(10, 6), gridspec_kw={'height_ratios': [3, 1]}, sharex=True)

ax1_c.scatter(t_c, x_c, s=1, color='orange', alpha=0.3, label='Dati Controfase')
ax1_c.plot(t_c, y_fit_c, color='purple', label='Fit Modo Controfase')
testo_stats_c = f"$\\chi^2_{{red}}$ = {chi2_red_c:.2f}\np-value = {p_val_c:.2e}"
ax1_c.plot([], [], ' ', label=testo_stats_c)
ax1_c.set_title(f"Modo Normale: Controfase ($\omega_c$ = {popt_c[2]:.3f} rad/s)")
ax1_c.legend()
ax1_c.grid(True, alpha=0.3)
ax1_c.set_ylabel("Ampiezza")

ax2_c.scatter(t_c, residui_norm_c, s=1, color='black', alpha=0.5)
ax2_c.axhline(0, color='red', linestyle='--')
ax2_c.set_ylabel("Residui norm.")
ax2_c.set_xlabel("Tempo (s)")
ax2_c.grid(True, alpha=0.3)


# ==========================================
# --- D. BATTIMENTI ---
# ==========================================
file_battimenti = os.path.join(cartella_download, 'battimenti119.txt')
t_b, x_b, _, _ = carica_dati(file_battimenti)
mask_b = (t_b > 2) & (t_b < 55)
t_b, x_b = t_b[mask_b], x_b[mask_b]

wp_guess = (popt_f[2] + popt_c[2]) / 2
wb_guess = abs(popt_f[2] - popt_c[2]) / 2

p0_b = [115, 70, wp_guess, wb_guess, 0, 0, 428]
popt_b, pcov_b = curve_fit(battimenti, t_b, x_b, p0=p0_b)

# Calcolo Statistiche Battimenti
y_fit_b = battimenti(t_b, *popt_b)
residui_b = x_b - y_fit_b
residui_norm_b = residui_b / sigma_y
dof_b = len(t_b) - len(popt_b)
chi2_b = np.sum(residui_norm_b**2)
chi2_red_b = chi2_b / dof_b
p_val_b = chi2.sf(chi2_b, dof_b)

# Grafico Battimenti
fig_b, (ax1_b, ax2_b) = plt.subplots(2, 1, figsize=(12, 7), gridspec_kw={'height_ratios': [3, 1]}, sharex=True)

ax1_b.scatter(t_b, x_b, s=1, color='gray', alpha=0.5, label='Dati Battimenti')
ax1_b.plot(t_b, y_fit_b, color='green', label='Fit Battimenti')
inv = popt_b[0] * np.exp(-t_b / popt_b[1]) * np.cos(popt_b[3] * t_b + popt_b[5]) + popt_b[6]
ax1_b.plot(t_b, inv, '--r', label='Inviluppo modulante')
ax1_b.plot(t_b, -inv + 2*popt_b[6], '--r')

testo_stats_b = f"$\\chi^2_{{red}}$ = {chi2_red_b:.2f}\np-value = {p_val_b:.2e}"
ax1_b.plot([], [], ' ', label=testo_stats_b)
ax1_b.set_title(f"Fenomeno dei Battimenti ($\omega_p$={popt_b[2]:.3f}, $\omega_b$={popt_b[3]:.3f})")
ax1_b.legend()
ax1_b.grid(True, alpha=0.3)
ax1_b.set_ylabel("Ampiezza")

ax2_b.scatter(t_b, residui_norm_b, s=1, color='black', alpha=0.5)
ax2_b.axhline(0, color='red', linestyle='--')
ax2_b.set_ylabel("Residui norm.")
ax2_b.set_xlabel("Tempo (s)")
ax2_b.grid(True, alpha=0.3)


# ==========================================
# --- E. TRASFORMATA DI FOURIER SUI RESIDUI ---
# ==========================================
print("\n--- ANALISI FFT SUI RESIDUI (MODO IN FASE) ---")

# 1. Calcolo del passo di campionamento medio (dt)
# Assumiamo che i dati temporali siano equispaziati
dt = np.mean(np.diff(t_f))
N = len(t_f)

# 2. Esecuzione della Trasformata di Fourier Veloce (FFT)
yf = fft(residui_f)
# Calcolo delle frequenze associate (in Hz)
xf = fftfreq(N, dt)[:N//2] # Prendiamo solo la metà positiva dello spettro

# 3. Conversione da frequenza (Hz) a pulsazione (rad/s)
omega_fft = 2 * np.pi * xf
ampiezza_fft = 2.0/N * np.abs(yf[0:N//2])

# 4. Ricerca del picco di massimo errore
# Ignoriamo la primissima componente (omega = 0, che è solo l'offset continuo)
indice_picco = np.argmax(ampiezza_fft[1:]) + 1 
omega_anomala = omega_fft[indice_picco]
ampiezza_massima = ampiezza_fft[indice_picco]

print(f"Frequenza angolare dell'errore sistematico: {omega_anomala:.3f} rad/s")

# 5. Creazione del Grafico dello Spettro
plt.figure(figsize=(10, 5))
plt.plot(omega_fft, ampiezza_fft, color='darkred', label='Spettro dei Residui')
plt.axvline(omega_anomala, color='orange', linestyle='--', 
            label=f'Picco anomalo: {omega_anomala:.3f} rad/s')

# Aggiungiamo linee verticali di riferimento per i valori che già conosci
plt.axvline(popt_c[2], color='cyan', linestyle=':', alpha=0.7, label=f'$\omega_p$ fit ({popt_c[2]:.3f})')
plt.axvline(popt_f[2], color='purple', linestyle=':', alpha=0.7, label=f'$\omega_b$ fit ({popt_f[2]:.3f})')

plt.title("Spettro in Frequenza dei Residui (Modo in Fase)")
plt.xlabel("Pulsazione Angolare $\omega$ (rad/s)")
plt.ylabel("Ampiezza FFT")
# Limitiamo l'asse X per concentrarci sulla zona di interesse (da 0 a circa 10 rad/s)
plt.xlim(0, 10) 
plt.grid(True, alpha=0.3)
plt.legend()

# ==========================================
# MOSTRA TUTTI I GRAFICI E STAMPA RISULTATI
# ==========================================
plt.tight_layout() # Ottimizza gli spazi nei grafici
plt.show()

# Stampa riassuntiva in console
print(f"--- RISULTATI FINALI ---")
print(f"Pulsazione Singolo: {popt_s[2]:.3f} rad/s | Chi2_red: {chi2_red_s:.2f} | p-value: {p_val_s:.2e}")
print(f"Pulsazione Fase:    {popt_f[2]:.3f} rad/s | Chi2_red: {chi2_red_f:.2f} | p-value: {p_val_f:.2e}")
print(f"Pulsazione Contro:  {popt_c[2]:.3f} rad/s | Chi2_red: {chi2_red_c:.2f} | p-value: {p_val_c:.2e}")
print(f"Battimento (WP):    {popt_b[2]:.3f} rad/s | Chi2_red: {chi2_red_b:.2f} | p-value: {p_val_b:.2e}")
print(f"Battimento (WB):    {popt_b[3]:.3f} rad/s")