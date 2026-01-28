# import numpy as np
# from matplotlib import pyplot as plt
# from scipy.optimize import curve_fit

# centrTemps = np.array([27.69, 28.54, 29.18, 29.72, 30.15, 30.37, 30.59, 31.03, 31.90, 32.24, 32.90, 33.69, 34.14, 34.70, 35.39, 36.08, 36.66, 37.24, 38.07, 38.78])
# maxTemps =   np.array([27.79, 28.86, 29.29, 29.94, 30.15, 30.48, 30.59, 31.03, 31.90, 32.34, 33.01, 33.69, 34.25, 34.82, 35.50, 36.19, 36.77, 37.36, 38.19, 38.90])
# minTempsCU =   np.array([27.60, 28.44, 29.07, 29.61, 30.05, 30.30, 30.53, 30.92, 31.79, 32.24, 32.80, 33.57, 34.03, 34.48, 35.28, 35.96, 36.54, 37.24, 37.97, 38.54])

# deltaCentrTemps = np.empty(centrTemps.size)
# deltaErrorTemps = np.empty(centrTemps.size)

# lamdaAspettato = 400    #rame

# def calcoloDeltaandErrori():
#     for i in range(centrTemps.size):
#         if i != 0:
#             deltaCentrTemps[i] = centrTemps[i] - centrTemps[i-1]
#             deltaErrorTemps[i] = (maxTemps[i] - minTempsCU[i])/2 + (maxTemps[i-1] - minTempsCU[i-1])/2 
            
#     return deltaCentrTemps, deltaErrorTemps

# def stampaRisDelta(deltaCentrTemps, deltaErrorTemps):
#     for i in range(1, deltaCentrTemps.size):
#         print(f"ΔT{i} {np.round(deltaCentrTemps[i], 4)} ± {np.round(deltaErrorTemps[i], 4)}")

# centr, errori = calcoloDeltaandErrori()
# stampaRisDelta(centr, errori)

# def fit_model(x, m, q):
#     return m * x + q

# count = np.array([1., 2., 3., 4., 5., 6., 7., 8., 9., 10., 11., 12, 13., 14., 15., 16., 17., 18., 19., 20.])
# popt, pcov = curve_fit(fit_model, count, centr, sigma=errori)

# plt.errorbar(count, centr, errori, fmt='o')
# plt.plot(count, fit_model(count, *popt))
# plt.xlabel('N')
# plt.ylabel('ΔT')

# plt.show()
# x = np.linspace(0,5,10)
# y = lamdaAspettato + 0*x
# plt.plot(x, y, '-r', label='coefficente termico aspettato')
# plt.title('Paragone coeff. aspettato e reale')
# plt.xlabel('x', color='#1C2833')
# plt.ylabel('y', color='#1C2833')
# plt.legend(loc='upper left')
# plt.grid()
# plt.show()


import numpy as np
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit

# Dati sperimentali
centrTempsCU = np.array([27.69, 28.54, 29.18, 29.72, 30.15, 30.37, 30.59, 31.03, 31.90, 32.24, 32.90, 33.69, 34.14, 34.70, 35.39, 36.08, 36.66, 37.24, 38.07, 38.78])
maxTempsCU   = np.array([27.79, 28.86, 29.29, 29.94, 30.15, 30.48, 30.59, 31.03, 31.90, 32.34, 33.01, 33.69, 34.25, 34.82, 35.50, 36.19, 36.77, 37.36, 38.19, 38.90])
minTempsCU   = np.array([27.60, 28.44, 29.07, 29.61, 30.05, 30.30, 30.53, 30.92, 31.79, 32.24, 32.80, 33.57, 34.03, 34.48, 35.28, 35.96, 36.54, 37.24, 37.97, 38.54])

centrTempsAC = np.array([44.12, 41.95, 40.59, 39.26, 38.07, 36.77, 35.16, 34.02, 32.68, 31.46, 30.15, 28.86, 27.47, 26.10, 24.95])
maxTempsAC   = np.array([44.24, 42.20, 40.60, 39.38, 38.18, 36.77, 35.27, 34.02, 32.79, 31.46, 30.26, 29.06, 27.90, 26.63, 25.37])
minTempsAC   = np.array([44.12, 41.86, 40.48, 39.14, 37.99, 36.66, 34.95, 33.91, 32.57, 31.35, 30.07, 28.76, 27.47, 26.10, 24.85])

#misure 
deltaXCU = 21.41
sigmaXCU = 0.09

deltaXAC = 25.07
sigmaXAC = 0.03

#potenza erogata dal generatore
W = 16.54

#area della sezione calcoata a partire dal diametro del tubo [corretto per 10 alla -6 perché calcolata a partire dal diamentro in mm]
S = 490.09 * 10**-6

#calcola le distanze tra i fori e l'errore
#restituisce matrice di due righe :
    #prima riga -> valori deltax
    #seconda riga -> valori dell'errore calcolato per ogni delta
def lunghezze(nfori, deltax, sigmax):
    lng = np.zeros((2, nfori))

    for i in range(1, nfori):
        lng[0][i] = lng[0][i-1] + deltax
        lng[1][i] = lng[1][i-1] + sigmax

    print(lng)
    return lng

#calcola il valore centrale di lamda, no errore
def calcoloLamda(X, T):
    lamda = np.empty(len(T)-1)
    for i in range(1, len(T)):
        dX = X[i] - X[0]
        dT = T[i] - T[0]
        lamda[i-1] = (W / S) * (dX*10**-3 )/ dT     #*10 alla -3 perchè la misura dei fori è stata fatta in mm
    return lamda



# Fit lineare
def fit_model(x, m, q):
    return m * x + q


lung1 = lunghezze(centrTempsCU.size, deltaXCU, sigmaXCU)
lung2 = lunghezze(centrTempsAC.size, deltaXAC, sigmaXAC)

# errori su T
tempErrorsCU = (maxTempsCU - minTempsCU) / 2
tempErrorsAC = (maxTempsAC - minTempsAC) / 2

# fit
popt, pcov = curve_fit(fit_model, lung1[0,:], centrTempsCU, sigma=tempErrorsCU, absolute_sigma=True)
lamdaCU_coefAng, q = popt
m_err, q_err = np.sqrt(np.diag(pcov))
plt.figure(1)
plt.errorbar(lung1[0,:], centrTempsCU, yerr=tempErrorsCU, xerr=lung1[1, :],fmt='o', capsize=3)
plt.plot(lung1[0,:], fit_model(lung1[0,:], *popt), color='orange')

popt, pcov = curve_fit(fit_model, lung2[0,:], centrTempsAC, sigma=tempErrorsAC, absolute_sigma=True)
lamdaAC_coefAng, q = popt
m_err, q_err = np.sqrt(np.diag(pcov))

plt.errorbar(lung2[0,:], centrTempsAC, yerr=tempErrorsAC, xerr=lung2[1, :],fmt='o', capsize=3)
plt.plot(lung2[0,:], fit_model(lung2[0,:], *popt), color='gray')

plt.xlabel("Posizione (mm)")
plt.ylabel("Temperatura [°C]")

#####

#ridimensionamento dei lamda dei coefficenti angolari
lamdaCU_coefAng = lamdaCU_coefAng*10**3
lamdaAC_coefAng = lamdaAC_coefAng*10**3

print(f"Lamda CU: {lamdaCU_coefAng} \nLamda AC: {lamdaAC_coefAng}")

lamdaCU = calcoloLamda(lung1[0, :], centrTempsCU)
lamdaAC = calcoloLamda(lung2[0, :], centrTempsAC)


XCU_mid = (lung1[0, :-1] + lung1[0, 1:]) / 2
XAC_mid = (lung2[0, :-1] + lung2[0, 1:]) / 2

plt.figure(2)

plt.plot(XCU_mid, lamdaCU, 'o-', color='blue', label='Rame')
plt.plot(XAC_mid, lamdaAC, 'o-', color='red', label='Acciaio')

plt.xlabel("Posizione (mm)")
plt.ylabel("λ (W/m·K)")
plt.grid()
plt.legend()
plt.show()