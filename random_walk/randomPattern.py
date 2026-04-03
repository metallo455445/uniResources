import time
import numpy as np                          #numeracci
from matplotlib import pyplot as plt        #grafici
from scipy.optimize import curve_fit        #fit

def random_walk(num_steps=1000):
    x = np.array(0)
    y = np.array(0)
    phi = np.random.uniform(0., 2. * np.pi, size=num_steps)
    x = np.append(x, np.cumsum(np.cos(phi)))
    y = np.append(y, np.cumsum(np.sin(phi)))
    return x, y

nPassi = 1000

x, y = random_walk(nPassi)
plt.plot(x, y, color="black", label="percorso random walk")
X_extr = [x[0], x[len(x)-1]]
Y_extr = [y[0], y[len(y)-1]]
d = np.sqrt(X_extr[1]**2 + Y_extr[1]**2)
plt.plot(X_extr, Y_extr, "bo", linestyle="--", color="grey", label=rf"spostamento totale: {d:.2f}")
plt.plot(x[0], y[0], "o", color="blue", label="inizio")
plt.plot(x[len(x)-1], y[len(y)-1], "o", color="red", label="fine")
plt.legend()
plt.grid()
plt.xlabel('x')
plt.ylabel('y')
plt.title(rf'numero di passi: {nPassi}')
plt.show()
