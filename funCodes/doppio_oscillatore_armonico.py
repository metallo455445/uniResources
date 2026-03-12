from oscillatore_armonico import *
import numpy as np                          #numeracci
from matplotlib import pyplot as plt        #grafici
from scipy.optimize import curve_fit        #fit

#condizioni iniziali
k1 = 100.
m1 = 100.
vi1 = 0.
xi1 = 100.

k2 = 10.
m2 = 10.
vi2 = 0.
xi2 = 200.

periodi = 3

mu = xi2 - xi1      #distanza relativa in t=0
vrel0 = vi2 - vi1   #velocità elativa in t=0

omega1 = np.sqrt(k1 / m1)
omega2 = omega1 #np.sqrt(k2 / mu)

b1 = vi1 / omega1
b2 = vi2 / omega2

a1 = xi1
a2 = xi2

#x1(t) = A1 cos(wt + phi1)
#x2(t) - x1(t) = A2 cos(wt + phi2)
#  | x1(0) = A1 cos(phi1)
# <
#  | v1(0) = d/dt x1(0) = -w A1 sin(phi1)
# 
# x1^2(0) + v1^2(0) / w^2 = A1^2

A1 = np.sqrt(xi1 ** 2 + ((vi1 ** 2) / omega1 **2))
phi1 = np.arccos(xi1 / A1)

#per 2 lo stesso solo che devo usre la distanza e velocità relativa 

A2 = np.sqrt(mu ** 2 + ((vrel0 ** 2) / omega1 **2))
phi2 = np.arccos(mu / A2)

def motocomposto(A1, A2, omega, phi1, phi2, t):
    return A1 * np.cos((omega * t) + phi1) + A2 * np.cos((omega * t) + phi2)

t = np.arange(0, periodi * 2 * np.pi, 0.01)
plt.plot(t, leggeOrariaArmonicoCI(omega1, a1, b1, t), label="molla 1")
plt.plot(t, leggeOrariaArmonicoCI(omega2, a2, b2, t), label="molla 2")
plt.plot(t, motocomposto(A1, A2, omega1, phi1, phi2, t), label="unite")
plt.legend()
plt.show()