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
from scipy.signal import find_peaks
import os

# --- 1. FUNZIONI MODELLO ---

def pendolo_smorzato(t, A, tau, omega, phi, offset):
    return A * np.exp(-t / tau) * np.cos(omega * t + phi) + offset

def inviluppo_esponenziale(t, A0, tau, offset):
    """ Modello per l'inviluppo: A(t) = A0 * exp(-t/tau) + offset """
    return A0 * np.exp(-t / tau) + offset

def battimenti(t, A, tau, omega_p, omega_b, phi_p, phi_b, offset):
    decadimento = np.exp(-t / tau)
    portante = np.cos(omega_p * t + phi_p)
    modulante = np.cos(omega_b * t + phi_b)
    return A * decadimento * portante * modulante + offset

def carica_dati(filename):
    dati = np.loadtxt(filename, skiprows=4)
    return dati[:, 0], dati[:, 1], dati[:, 2], dati[:, 3]

# ATTENZIONE: Inserisci qui l'errore reale delle tue misurazioni sulle y
SIGMA_Y = 1.0  

# --- 2. FUNZIONI PER GRAFICI E STATISTICA ---

def fit_e_grafico_inviluppo(t, x, nome_file, titolo):
    """
    Trova i picchi, fitta l'inviluppo esponenziale e salva il grafico in PGF.
    Dati in blu, fit in rosso tratteggiato.
    """
    # 1. Trova i picchi (massimi)
    # Prominence dinamica per evitare di prendere il rumore di fondo
    prominence = (np.max(x) - np.min(x)) * 0.1 
    peaks, _ = find_peaks(x, prominence=prominence)
    t_peaks = t[peaks]
    x_peaks = x[peaks]
    
    # 2. Fit dell'inviluppo sui picchi
    p0_env = [(np.max(x)-np.min(x))/2, 40, np.mean(x)]
    popt_env, _ = curve_fit(inviluppo_esponenziale, t_peaks, x_peaks, p0=p0_env)
    
    # 3. Calcolo residui e statistica SUI PICCHI
    fit_y_peaks = inviluppo_esponenziale(t_peaks, *popt_env)
    residui = x_peaks - fit_y_peaks
    residui_norm = residui / SIGMA_Y
    
    dof = len(t_peaks) - len(popt_env)
    chi_square = np.sum(residui_norm**2)
    chi_square_red = chi_square / dof if dof > 0 else 0
    err_chi_square_red = np.sqrt(2 / dof) if dof > 0 else 0
    p_value = chi2.sf(chi_square, dof) if dof > 0 else 0
    
    # 4. Creazione Grafico
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 6), 
                                   gridspec_kw={'height_ratios': [3, 1]}, 
                                   sharex=True)
    
    # Dati in blu e picchi
    ax1.plot(t, x, color='blue', alpha=0.4, label='Dati Sperimentali')
    ax1.scatter(t_peaks, x_peaks, color='darkblue', s=15, zorder=5, label='Picchi per il Fit')
    
    # Fit inviluppo in rosso tratteggiato
    t_continuo = np.linspace(min(t), max(t), 1000)
    ax1.plot(t_continuo, inviluppo_esponenziale(t_continuo, *popt_env), 
             '--', color='red', linewidth=2, label='Fit Inviluppo')
    
    # Etichetta statistiche
    stats_label = (f"$\\chi^2_{{red}} = {chi_square_red:.2f} \\pm {err_chi_square_red:.2f}$\n"
                   f"$p$-value = {p_value:.2e}\n"
                #    22
                   )
    ax1.plot([], [], ' ', label=stats_label)
    
    ax1.set_title(titolo)
    ax1.set_ylabel("Ampiezza")
    ax1.legend(loc='upper right')
    ax1.grid(True, alpha=0.3)
    
    # Pannello inferiore: Residui
    ax2.scatter(t_peaks, residui_norm, color='black', s=15)
    ax2.axhline(0, color='red', linestyle='--')
    ax2.set_xlabel("Tempo (s)")
    ax2.set_ylabel("Residui norm.")
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(nome_file, format='pgf')
    plt.close()
    
    return popt_env

def crea_grafico_battimenti_pgf(t, x, func, popt, nome_file, titolo):
    """
    Funzione specifica per i battimenti: mantiene il fit globale 
    ma uniforma i colori (blu per dati, rosso tratteggiato per l'inviluppo modulante).
    """
    fit_y = func(t, *popt)
    residui = x - fit_y
    residui_norm = residui / SIGMA_Y
    
    dof = len(t) - len(popt)
    chi_square = np.sum(residui_norm**2)
    chi_square_red = chi_square / dof
    err_chi_square_red = np.sqrt(2 / dof) 
    p_value = chi2.sf(chi_square, dof)
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 6), 
                                   gridspec_kw={'height_ratios': [3, 1]}, sharex=True)
    
    ax1.plot(t, x, color='blue', alpha=0.4, label='Dati Sperimentali')
    
    # Calcolo inviluppo modulante
    inv = popt[0] * np.exp(-t / popt[1]) * np.cos(popt[3] * t + popt[5]) + popt[6]
    ax1.plot(t, inv, '--', color='red', linewidth=2, label='Inviluppo modulante')
    ax1.plot(t, -inv + 2*popt[6], '--', color='red', linewidth=2)
        
    stats_label = (f"$\\chi^2_{{red}} = {chi_square_red:.2f} \\pm {err_chi_square_red:.2f}$\n"
                   f"$p$-value = {p_value:.2e}")
    ax1.plot([], [], ' ', label=stats_label)
    
    ax1.set_title(titolo)
    ax1.set_ylabel("Ampiezza")
    ax1.legend(loc='upper right')
    ax1.grid(True, alpha=0.3)
    
    ax2.scatter(t, residui_norm, s=1, color='black', alpha=0.5)
    ax2.axhline(0, color='red', linestyle='--')
    ax2.set_xlabel("Tempo (s)")
    ax2.set_ylabel("Residui norm.")
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(nome_file, format='pgf')
    plt.close()

# --- 3. ESECUZIONE ANALISI ---

cartella_download = r'/home/matteo/Documenti/uni/lab/oscillazioni/runs'

# --- A. PENDOLO SINGOLO ---
file_singolo = os.path.join(cartella_download, 'singolosmorzato116.txt')
t_s, _, _, x_s = carica_dati(file_singolo)
mask_s = (t_s > 2) & (t_s < 55)
t_s, x_s = t_s[mask_s], x_s[mask_s]

popt_env_s = fit_e_grafico_inviluppo(t_s, x_s, 'pendolo_singolo_inviluppo.pgf', 
                                     "Pendolo Singolo: Fit dell'Inviluppo Esponenziale")

# --- B. MODO IN FASE ---
file_fase = os.path.join(cartella_download, 'fase117.txt')
t_f, x_f, _, _ = carica_dati(file_fase)
mask_f = (t_f > 2) & (t_f < 55)
t_f, x_f = t_f[mask_f], x_f[mask_f]

popt_env_f = fit_e_grafico_inviluppo(t_f, x_f, 'fase_inviluppo.pgf', 
                                     "Modo Normale (In Fase): Fit dell'Inviluppo Esponenziale")

# --- C. MODO IN CONTROFASE ---
file_controfase = os.path.join(cartella_download, 'controfase118.txt')
t_c, x_c, _, _ = carica_dati(file_controfase)
mask_c = (t_c > 2) & (t_c < 55)
t_c, x_c = t_c[mask_c], x_c[mask_c]

popt_env_c = fit_e_grafico_inviluppo(t_c, x_c, 'controfase_inviluppo.pgf', 
                                     "Modo Normale (Controfase): Fit dell'Inviluppo Esponenziale")

# --- D. BATTIMENTI ---
file_battimenti = os.path.join(cartella_download, 'battimenti119.txt')
t_b, x_b, _, _ = carica_dati(file_battimenti)
mask_b = (t_b > 2) & (t_b < 55)
t_b, x_b = t_b[mask_b], x_b[mask_b]

# Per i battimenti manteniamo il fit completo per estrarre portante e modulante
# (Le pulsazioni servono come stima iniziale)
wp_guess = 4.4 # Stima approssimativa ricavata in precedenza
wb_guess = 0.25 
p0_b = [115, 70, wp_guess, wb_guess, 0, 0, 428]
popt_b, _ = curve_fit(battimenti, t_b, x_b, p0=p0_b)

crea_grafico_battimenti_pgf(t_b, x_b, battimenti, popt_b, 'battimenti.pgf', 
                            f"Fenomeno dei Battimenti ($\\omega_p$={popt_b[2]:.3f}, $\\omega_b$={popt_b[3]:.3f})")

print("--- ANALISI COMPLETATA ---")
print(f"Tau Singolo:    {popt_env_s[1]:.2f} s")
print(f"Tau Fase:       {popt_env_f[1]:.2f} s")
print(f"Tau Controfase: {popt_env_c[1]:.2f} s")
print("I grafici sono stati salvati in formato .pgf con i nuovi stili (dati blu, inviluppo rosso tratteggiato).")