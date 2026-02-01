import numpy as np
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit
import matplotlib as mpl

mpl.use("pgf")

plt.rcParams.update({
    "pgf.texsystem": "xelatex",
    "text.usetex": True,
    "pgf.rcfonts": False,
    # Trasforma la lista in una stringa unica separata da \n
    "pgf.preamble": (
        r"\usepackage{unicode-math}"
        r"\setmainfont{Latin Modern Roman}"
    )
})

nMisurazioni = 1
numeroFissoEsagono = 0.866
sigmaMassa = 0.001

def HelloWorld(print):
    print("HelloWorld!")

class oggetto():
    materiale   = ""
    massa       = 0
    tipo        = ""
    volume      = 0
    sigmaVolume = 0
    oggetti = []
    densita = 0
    sigmaDensita = 0

    def __init__(self, mat, massa, tip):
          self.materiale    = mat
          self.massa        = massa
          self.tipo         = tip
          oggetto.oggetti.append(self)

    def clacoloVolume(self):
        if self.tipo == "cilindro":
            r_medio = np.mean(self.diametro) / 2
            h_medio = np.mean(self.altezza)
            
            self.volume = np.pi * (r_medio ** 2) * h_medio
            
            E_r_D = np.mean(self.sigmaDiametro) / np.mean(self.diametro)
            E_r_h = np.mean(self.sigmaAltezza) / np.mean(self.altezza)
            
            E_r_V = 2 * E_r_D + E_r_h
            self.sigmaVolume = self.volume * E_r_V
            
        elif self.tipo == "parallelepipedo":
            A_medio = np.mean(self.latoA)
            B_medio = np.mean(self.latoB)
            C_medio = np.mean(self.latoC)
            
            self.volume = A_medio * B_medio * C_medio
            
            E_r_A = np.mean(self.sigmaLatoA) / A_medio
            E_r_B = np.mean(self.sigmalatoB) / B_medio
            E_r_C = np.mean(self.sigmalatoC) / C_medio
            
            E_r_V = E_r_A + E_r_B + E_r_C
            self.sigmaVolume = self.volume * E_r_V

        elif self.tipo == "sfera":
            D_medio = np.mean(self.diametro)
            r_medio = D_medio / 2
            
            self.volume = (4/3) * np.pi * (r_medio ** 3)
            
            E_r_D = np.mean(self.sigmaDiametro) / D_medio
            
            E_r_V = 3 * E_r_D
            self.sigmaVolume = self.volume * E_r_V

        elif self.tipo == "prismaEx":
            D_misurato = np.mean(self.apotema)
            h_medio = np.mean(self.altezza)
            
            fattore_costante = 3 / (4 * numeroFissoEsagono)
            self.volume = fattore_costante * (D_misurato ** 2) * h_medio
            
            E_r_D = np.mean(self.sigmaApotema) / D_misurato
            E_r_h = np.mean(self.sigmaAltezza) / h_medio
            
            E_r_V = 2 * E_r_D + E_r_h
            self.sigmaVolume = self.volume * E_r_V
            
        #print(f"volume = {self.volume} +- {self.sigmaVolume}")

        self.densita = self.massa / self.volume
        self.sigmaDensita = self.densita * ((sigmaMassa / self.massa) + (self.sigmaVolume / self.volume))

    def infosub(self):
        pass

    def info(self):
        print(f"INFO: materiale:{self.materiale} massa:{self.massa} tipo:{self.tipo} volume:{self.volume} sigmaVol:{self.sigmaVolume}")
        self.infosub()

    @classmethod
    def volumePerMateriale(cls, materiale):
        vol = []
        mas = []
        errorVol = []
        for ogg in cls.oggetti:
            ogg.clacoloVolume()
            if ogg.materiale == materiale:
                vol.append(ogg.volume)
                mas.append(ogg.massa)
                errorVol.append(ogg.sigmaVolume)
        return vol, mas, errorVol
    
    @classmethod
    def densitaMateriale(cls, materiale):
        dens = []
        sigmaDens = []
        for ogg in cls.oggetti:
            if ogg.materiale == materiale:
                dens.append(ogg.densita)
                sigmaDens.append(ogg.sigmaDensita)
        return dens, sigmaDens
    
    @classmethod
    def massaPerSottoclasse(cls, tipologia):
        mass = []
        for ogg in cls.oggetti:
            if ogg.tipo == tipologia:
                mass.append(ogg.massa)
        return mass
    
    @classmethod
    def raggisfere(cls):
        ragg = []
        for ogg in cls.oggetti:
            if ogg.tipo == "sfera":
                raggio_medio = np.mean(ogg.diametro) / 2
                ragg.append(raggio_medio)
        return ragg
    
class cilindro(oggetto):
    altezza         = np.empty(nMisurazioni)
    sigmaAltezza    = np.empty(nMisurazioni)
    diametro        = np.empty(nMisurazioni)
    sigmaDiametro   = np.empty(nMisurazioni)
    
    def __init__(self, mat, mas, alt, sigmaAlt, diam, sigmaDiam):  
        super().__init__(mat, mas, "cilindro")
        self.altezza        = alt
        self.sigmaAltezza   = sigmaAlt
        self.diametro       = diam
        self.sigmaDiametro  = sigmaDiam

    def infosub(self):
        print(f"altezza:{self.altezza}, sigma altezza:{self.sigmaAltezza} diametro:{self.diametro} sigma diametro:{self.sigmaDiametro}")

class parallelepipedo(oggetto):
    latoA       = np.empty(nMisurazioni)
    sigmaLatoA  = np.empty(nMisurazioni)
    latoB       = np.empty(nMisurazioni)
    sigmalatoB  = np.empty(nMisurazioni)
    latoC       = np.empty(nMisurazioni)
    sigmalatoC  = np.empty(nMisurazioni)

    def __init__(self, mat, massa, latoA, sigmaA, latoB, sigmaB, latoC, sigmaC):
        super().__init__(mat, massa, "parallelepipedo")
        self.latoA      = latoA
        self.sigmaLatoA = sigmaA
        self.latoB      = latoB
        self.sigmalatoB = sigmaB
        self.latoC      = latoC
        self.sigmalatoC = sigmaC

    def infosub(self):
        print(f"lato A:{self.latoA}, sigma A:{self.sigmaLatoA}, lato B:{self.latoB}, sigma B:{self.sigmalatoB}, lato C:{self.latoC}, sigma C:{self.sigmalatoC}")

class sfera(oggetto):
    diametro        = np.empty(nMisurazioni)
    sigmaDiametro   = np.empty(nMisurazioni)

    def __init__(self, mat, massa, diam, sigmaDiam):
        super().__init__(mat, massa, "sfera")
        self.diametro       = diam
        self.sigmaDiametro  = sigmaDiam

    def infosub(self):
        print(f"diametro:{self.diametro}, sigma diametro:{self.sigmaDiametro}")

class prismaEx(oggetto):
    apotema         = np.empty(nMisurazioni)
    sigmaApotema    = np.empty(nMisurazioni)
    altezza         = np.empty(nMisurazioni)
    sigmaAltezza    = np.empty(nMisurazioni)

    def __init__(self, mat, massa, apotema, sigmaAp, h, sigmah):
        self.apotema        = apotema
        self.sigmaApotema   = sigmaAp
        self.altezza        = h
        self.sigmaAltezza   = sigmah
        super().__init__(mat, massa, "prismaEx")


ParA = parallelepipedo(
    mat = "A",
    massa= 7.874,
    latoA=8.10,
    latoB=18.00,
    latoC=20.40,
    sigmaA=0.02,
    sigmaB=0.02,
    sigmaC=0.02
)

ParB = parallelepipedo(
    mat="A",
    massa=4.833,
    latoA=17.80,
    latoB=10.04,
    latoC=10.04,
    sigmaA=0.02,
    sigmaB=0.02,
    sigmaC=0.02
)

CilA = cilindro(
    mat="A",
    mas=1.427,
    alt=18.92,
    diam=5.88,
    sigmaAlt=0.02,
    sigmaDiam=0.01
)

CilB = cilindro(
    mat="A",
    mas=5.862,
    alt=19.28,
    diam=11.92,
    sigmaAlt=0.02,
    sigmaDiam=0.01
)

CilC = cilindro(
    mat="A",
    mas=15.873,
    alt=19.04,
    diam=19.76,
    sigmaAlt=0.02,
    sigmaDiam=0.01
)

SfeA = sfera(
    mat="B",
    massa=8.359,
    diam=np.array([12.70, 12.70, 12.70]),
    sigmaDiam = np.array([0.01, 0.01, 0.01])
)

SfeB = sfera(
    mat="B",
    massa=11.890,
    diam=np.array([14.28, 14.28, 14.29]),
    sigmaDiam = np.array([0.01, 0.01, 0.01])
)

SfeC = sfera(
    mat="B",
    massa=11.890,
    diam=np.array([14.28, 14.28, 14.28]),
    sigmaDiam = np.array([0.01, 0.01, 0.01])
)

SfeD = sfera(
    mat="B",
    massa=24.822,
    diam=np.array([18.25, 18.25, 18.25]),
    sigmaDiam = np.array([0.01, 0.01, 0.01])
)

SfeE = sfera(
    mat="B",
    massa=44.707,
    diam=np.array([22.22, 22.21, 22.22]),
    sigmaDiam = np.array([0.01, 0.01, 0.01])
)

CilD = cilindro(                                        ###<----!Problemi
    mat="C",
    mas=29.500,
    alt=125.94,                                         ##13.94 valore iniziale: SBAGLIATO   aggiustato per far funzionare il fit
    diam=np.array([6.00, 5.99, 6.00]),
    sigmaAlt=0.02,
    sigmaDiam = np.array([0.01, 0.01, 0.01])
)

CilE = cilindro(
    mat="C",
    mas=24.579,
    alt=37.38,
    diam=np.array([9.95, 9.95, 9.96]),
    sigmaAlt=0.02,
    sigmaDiam = np.array([0.01, 0.01, 0.01])
)

CilF = cilindro(
    mat="C",
    mas=10.669,
    alt=16.18,
    diam=np.array([9.96, 9.96, 9.96]),
    sigmaAlt=0.02,
    sigmaDiam = np.array([0.01, 0.01, 0.01])
)

Pri = prismaEx(
    mat="C",
    massa=28.656,
    apotema=np.array([15.00, 14.92, 15.00]),
    h=17.74,
    sigmaAp = np.array([0.02, 0.02, 0.02]),
    sigmah=0.02
)

ParC = parallelepipedo(
    mat="C",
    massa=34.930,
    latoA=10.00,
    latoB=10.00,
    latoC=41.80,
    sigmaA=0.02,
    sigmaB=0.02,
    sigmaC=0.02
)

def line(x, a, b):
    return a * x + b

#------------------------------------ MATERIALE A ------------------------------------#
volA, massA, erroreVolA = oggetto.volumePerMateriale("A")
volA = np.array(volA)
massA = np.array(massA)
erroreVolA = np.array(erroreVolA)
erroreMasA = np.full(massA.shape, 0.001)

densA, erroreDensA = oggetto.densitaMateriale("A")
densA = np.array(densA)
erroreDensA = np.array(erroreDensA)

print(f"Densita' per A: {densA} +- {erroreDensA}")
print(f"media densita su a: {np.mean(densA)} +- {np.mean(erroreDensA)}")

plt.figure('Grafico massa-volume materiale A')
plt.errorbar(massA, volA, erroreVolA, erroreMasA, fmt='o')
popt, pcov = curve_fit(line, massA, volA)
a0, b0 = popt
sigma_a, sigma_b = np.sqrt(pcov.diagonal())
# Attenzione alle cifre significative quando
# si riportano questi valori sulla relazione:
print(f'a = {a0} +/- {sigma_a}')
print(f'b = {b0} +/- {sigma_b}')
# Grafico del modello di best fit.
x = np.linspace(0., 30., 100)
plt.plot(x, line(x, a0, b0))
plt.ylabel('Volume [mm$^3$]')
plt.xlabel('Massa [g]')
plt.grid(which='both', ls='dashed', color='gray')
plt.savefig('massa_volume_A.pgf')

residuiA = (volA - line(massA, a0, b0))/sigma_b
chi2 = np.sum(np.power(residuiA,2))
print(f"chi2 materiale A: {chi2}")

#------------------------------------ MATERIALE B ------------------------------------#
volB, massB, erroreVolB = oggetto.volumePerMateriale("B")
volB = np.array(volB)
massB= np.array(massB)
erroreVolB = np.array(erroreVolB)
erroreMasB = np.full(massB.shape, 0.001)

densB, erroreDensB = oggetto.densitaMateriale("B")
densB = np.array(densB)
erroreDensB = np.array(erroreDensB)

print(f"Densita' per B: {densB} +- {erroreDensB}")
print(f"media densita su B: {np.mean(densB)} +- {np.mean(erroreDensB)}")

plt.figure('Grafico massa-volume materiale B')
plt.errorbar(massB, volB, erroreVolB, erroreMasB, fmt='o')
popt, pcov = curve_fit(line, massB, volB)
a0, b0 = popt
sigma_a, sigma_b = np.sqrt(pcov.diagonal())
# Attenzione alle cifre significative quando
# si riportano questi valori sulla relazione:
print(f'a = {a0} +/- {sigma_a}')
print(f'b = {b0} +/- {sigma_b}')
# Grafico del modello di best fit.
x = np.linspace(0., 50., 100)
plt.plot(x, line(x, a0, b0))
plt.ylabel('Volume [mm$^3$]')
plt.xlabel('Massa [g]')
plt.grid(which='both', ls='dashed', color='gray')
plt.savefig('massa_volume_B.pgf')

residuiB = (volB - line(massB, a0, b0))/sigma_b
chi2 = np.sum(np.power(residuiB,2))
print(f"chi2 materiale B: {chi2}")

#------------------------------------ MATERIALE C ------------------------------------#
volC, massC, erroreVolC = oggetto.volumePerMateriale("C")
volC = np.array(volC)
massC = np.array(massC)
erroreVolC = np.array(erroreVolC)
erroreMasC = np.full(massC.shape, 0.001)

densC, erroreDensC = oggetto.densitaMateriale("C")
densC = np.array(densC)
erroreDensC = np.array(erroreDensC)

print(f"Densita' per C: {densC} +- {erroreDensC}")
print(f"media densita su C: {np.mean(densC)} +- {np.mean(erroreDensC)}")

plt.figure('Grafico massa-volume materiale C')
plt.errorbar(massC, volC, erroreVolC, erroreMasC, fmt='o')
popt, pcov = curve_fit(line, massC, volC)
a0, b0 = popt
sigma_a, sigma_b = np.sqrt(pcov.diagonal())
# Attenzione alle cifre significative quando
# si riportano questi valori sulla relazione:
print(f'a = {a0} +/- {sigma_a}')
print(f'b = {b0} +/- {sigma_b}')
# Grafico del modello di best fit.
x = np.linspace(0., 40., 100)
plt.plot(x, line(x, a0, b0))
plt.ylabel('Volume [mm$^3$]')
plt.xlabel('Massa [g]')
plt.grid(which='both', ls='dashed', color='gray')
plt.savefig('massa_volume_C.pgf')

residuiC = (volC - line(massC, a0, b0))/sigma_b
chi2 = np.sum(np.power(residuiC,2))
print(f"chi2 materiale C: {chi2}")

#------------------------------------ GRAFICI SFERE ------------------------------------#

raggi = oggetto.raggisfere()
masseSfere = oggetto.massaPerSottoclasse("sfera")
r = np.array(raggi)
m = np.array(masseSfere)
sigma_m = np.full(m.shape, sigmaMassa)
sigma_r = np.full(r.shape, 0.001)           #<<--- risoluzione palmer

print(f"Raggi: {r}, Masse: {m}")

plt.figure('Grafico massa-raggio')
plt.errorbar(r, m, sigma_m, sigma_r, fmt='o')
plt.xscale('log')
plt.yscale('log')
plt.xlabel('Raggio [mm]')
plt.ylabel('Massa [g]')
plt.grid(which='both', ls='dashed', color='gray')

# CORREZIONE DEGLI OFFSET: usare fattori moltiplicativi
for i in range(len(r)):
    testo_punto = f"({r[i]:.2f}, {m[i]:.1f})"
    
    # Offset Moltiplicativo (es. 1.05 = sposta del 5% del valore attuale)
    offset_factor_x = 1.05 
    offset_factor_y = 1.10   
    
    # Le coordinate del testo sono (valore * fattore)
    plt.text(r[i] * offset_factor_x, m[i] * offset_factor_y, 
             testo_punto, 
             fontsize=7, color='red')
             
plt.savefig('massa_raggio.pgf')

#------------------------------------ GRAFICO TOTALE ------------------------------------#

massTOT = np.concatenate((massA, massB, massC))
volTOT = np.concatenate((volA, volB, volC))
erroreVolTOT = np.concatenate((erroreVolA, erroreVolB, erroreVolC))
erroreMasTOT = np.concatenate((erroreMasA, erroreMasB, erroreMasC))

plt.figure('Grafico massa-volume totale')
plt.errorbar(massTOT, volTOT, erroreVolTOT, erroreMasTOT, fmt='o')

x = np.linspace(0., 40., 100)
plt.ylabel('Volume [mm$^3$]')
plt.xlabel('Massa [g]')
plt.grid(which='both', ls='dashed', color='gray')
plt.savefig('massa_volume_tot.pgf')

#plt.show()
#plt.savefig("grafico_densita.pgf") 