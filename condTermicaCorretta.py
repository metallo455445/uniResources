import numpy as np
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit

# Dati sperimentali
centrTempsCU = np.array([27.69, 28.54, 29.18, 29.72, 30.15, 30.37, 30.59, 31.03, 31.90, 32.24, 32.90, 33.69, 34.14, 34.70, 35.39, 36.08, 36.66, 37.24, 38.07, 38.78])
maxTempsCU   = np.array([27.79, 28.86, 29.29, 29.94, 30.15, 30.48, 30.59, 31.03, 31.90, 32.34, 33.01, 33.69, 34.25, 34.82, 35.50, 36.19, 36.77, 37.36, 38.19, 38.90])
minTempsCU   = np.array([27.60, 28.44, 29.07, 29.61, 30.05, 30.30, 30.53, 30.92, 31.79, 32.24, 32.80, 33.57, 34.03, 34.48, 35.28, 35.96, 36.54, 37.24, 37.97, 38.54])

centrTempsCU = np.flip(centrTempsCU)
maxTempsCU = np.flip(maxTempsCU)
minTempsCU = np.flip(minTempsCU)

centrTempsAL = np.array([44.12, 41.95, 40.59, 39.26, 38.07, 36.77, 35.16, 34.02, 32.68, 31.46, 30.15, 28.86, 27.47, 26.10, 24.95])
maxTempsAL   = np.array([44.24, 42.20, 40.60, 39.38, 38.18, 36.77, 35.27, 34.02, 32.79, 31.46, 30.26, 29.06, 27.90, 26.63, 25.37])
minTempsAL   = np.array([44.12, 41.86, 40.48, 39.14, 37.99, 36.66, 34.95, 33.91, 32.57, 31.35, 30.07, 28.76, 27.47, 26.10, 24.85])

#conversione in Kelvin delle temperature
# centrTempsCU = centrTempsCU + np.full(centrTempsCU.size, 273.15)
# centrTempsAL = centrTempsAL + np.full(centrTempsAL.size, 273.15)

#misure 
deltaXCU = 21.41
sigmaXCU = 1.0 #<----[ex 0.09]

deltaXAL = 25.07
sigmaXAL = 1.0 #<------[ex 0.03]

#potenza erogata dal generatore
W = 8.27 ####!!!! Da dividere per due
sigmaW = 0.10

#area della sezione calcolata a partire dal diametro del tubo
S = 490.09 * 10**-6 
sigmaS = 1.96 * 10**-6

#calcola le distanze tra i fori (nelle barre) e l'errore
def lunghezze(nfori, deltax, sigmax):
    lng = np.zeros((2, nfori))

    for i in range(1, nfori):
        lng[0][i] = lng[0][i-1] + deltax
        lng[1][i] = lng[1][i-1] + sigmax

    print(lng)
    return lng

#Calcolo della conducibilità termica
def calcoloLamda(X, T):
    lamda = np.empty(len(T)-1)
    for i in range(1, len(T)):
        dX = X[i] - X[i-1]  
        dT = T[i] - T[i-1]  
        # λ = (W * Δx) / (S * ΔT)
        lamda[i-1] = (W * (dX * 10**-3)) / (S * dT)
    return lamda

def erroreLamda(centrLamda, sigmaCoefAng):
    return centrLamda * np.sqrt((sigmaW ** 2) + (sigmaCoefAng ** 2) + (sigmaS ** 2))

# Fit lineare
def fit_model(x, m, q):
    return m * x + q

lung1 = lunghezze(centrTempsCU.size, deltaXCU, sigmaXCU)
lung2 = lunghezze(centrTempsAL.size, deltaXAL, sigmaXAL)

#veri errori su T
tempErrorsCU = np.full(maxTempsCU.shape, 0.11)
tempErrorsAL = np.full(maxTempsAL.shape, 0.11)
# errori su T
# tempErrorsCU = (maxTempsCU - minTempsCU) / 2
# tempErrorsAL = (maxTempsAL - minTempsAL) / 2

# --- FIT PER IL RAME (FINESTRA 1) ---
plt.figure("Rame - Distribuzione di temperatura")

popt, pcov = curve_fit(fit_model, lung1[0,:], centrTempsCU, sigma=tempErrorsCU, absolute_sigma=True)
lamdaCU_coefAng, q = popt
print(f"coefCU {lamdaCU_coefAng}, errore {np.sqrt(pcov[0][0])}")
print(f"errore su Lamda di CU {erroreLamda(lamdaCU_coefAng, q)}")

plt.errorbar(lung1[0,:], centrTempsCU, yerr=tempErrorsCU, xerr=lung1[1, :], fmt='o', capsize=3, label='Dati sperimentali')
plt.plot(lung1[0,:], fit_model(lung1[0,:], *popt), label=f'Fit: m = {lamdaCU_coefAng:.4f} °C/mm')
plt.xlabel("Posizione (mm)")
plt.ylabel("Temperatura [°C]")
plt.title("Rame - Distribuzione di temperatura")
plt.legend()
plt.grid(True)



# --- FIT PER L'ALLUMINIO (FINESTRA 2) ---
plt.figure("Alluminio - Distribuzione di temperatura")

popt, pcov = curve_fit(fit_model, lung2[0,:], centrTempsAL, sigma=tempErrorsAL, absolute_sigma=True)
lamdaAL_coefAng, q = popt
print(f"coefAL {lamdaAL_coefAng}, errore {np.sqrt(pcov[0][0])}")
print(f"errore su Lamda di AL {erroreLamda(lamdaAL_coefAng, q)}")

plt.errorbar(lung2[0,:], centrTempsAL, yerr=tempErrorsAL, xerr=lung2[1, :], fmt='o', capsize=3, label='Dati sperimentali')
plt.plot(lung2[0,:], fit_model(lung2[0,:], *popt), label=f'Fit: m = {lamdaAL_coefAng:.4f} °C/mm', color='blue')
plt.xlabel("Posizione (mm)")
plt.ylabel("Temperatura [°C]")
plt.title("Alluminio - Distribuzione di temperatura")
plt.legend()
plt.grid(True)

plt.show()

# Il segno negativo è perché il flusso di calore va da temperature alte a basse
lamda_CU_from_slope = - (W / S) * (1 / (lamdaCU_coefAng * 1000))  # conversione da °C/mm a °C/m
lamda_AL_from_slope = - (W / S) * (1 / (lamdaAL_coefAng * 1000))  # conversione da °C/mm a °C/m

print(f"Conducibilità termica dal coefficiente angolare:")
print(f"Rame: {lamda_CU_from_slope:.2f} W/m·K")
print(f"Acciaio: {lamda_AL_from_slope:.2f} W/m·K")

###roba extra non importante

# # Calcolo del lamda punto per punto
# lamdaCU = calcoloLamda(lung1[0, :], centrTempsCU)
# lamdaAL = calcoloLamda(lung2[0, :], centrTempsAL)

# # Per l'acciaio prendiamo il valore assoluto poiché il gradiente è negativo
# lamdaAL = np.abs(lamdaAL)

# XCU_mid = (lung1[0, :-1] + lung1[0, 1:]) / 2
# XAL_mid = (lung2[0, :-1] + lung2[0, 1:]) / 2

# plt.figure(2)
# plt.subplot(1, 2, 1)
# plt.plot(XCU_mid, lamdaCU, 'o-', color='blue', label='Rame (punto per punto)')
# plt.axhline(y=400, color='red', linestyle='--', label='Valore atteso rame (~400 W/m·K)')
# plt.xlabel("Posizione (mm)")
# plt.ylabel("λ (W/m·K)")
# plt.title("Conducibilità termica - Rame")
# plt.grid()
# plt.legend()

# plt.subplot(1, 2, 2)
# plt.plot(XAL_mid, lamdaAL, 'o-', color='red', label='Acciaio (punto per punto)')
# plt.axhline(y=200, color='green', linestyle='--', label='Valore atteso acciaio (~50 W/m·K)')
# plt.xlabel("Posizione (mm)")
# plt.ylabel("λ (W/m·K)")
# plt.title("Conducibilità termica - Acciaio")
# plt.grid()
# plt.legend()

# plt.tight_layout()

# # Calcolo dei valori medi
# lamdaCU_mean = np.mean(lamdaCU)
# lamdaAL_mean = np.mean(lamdaAL)

# print(f"\nConducibilità termica media punto per punto:")
# print(f"Rame: {lamdaCU_mean:.2f} W/m·K")
# print(f"Acciaio: {lamdaAL_mean:.2f} W/m·K")

# plt.show()