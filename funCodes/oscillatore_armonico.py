import numpy as np                          #numeracci
from matplotlib import pyplot as plt        #grafici
from scipy.optimize import curve_fit        #fit

#condizioni iniziali
k = 100
m = 10
v0 = 0
x0 = 20

omega = np.sqrt(k/m)

#x^ (t) = - omega A sin (omega * t + phi)
#per t = 0
#v0 = - a * omega * np.sin(omega * t) + b * omega * np.cos(omega * t)

b = v0 / omega

#x(t) = A cos(omega t) + b sin(omega t)
#per t = 0

a = x0

def leggeOrariaArmonico(t):
    #x(t) = A cos(omega t) + b sin(omega t)
    return a * np.cos(omega*t) + b * np.sin(omega*t)

def leggeOrariaArmonicoCI(omega, a, b, t):
    return a * np.cos(omega*t) + b * np.sin(omega*t)
#plot
# t = np.arange(0, 3*2*np.pi, 0.01)
# plt.plot(t, leggeOrariaArmonico(t))
# plt.show()
