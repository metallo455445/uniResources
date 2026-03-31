import random
import numpy as np
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit
from scipy.stats import chi2
import time

# def random_walk(num_steps=1000):
#     x = np.array(0)
#     y = np.array(0)
#     phi = np.random.uniform(0., 2. * np.pi, size=num_steps)
#     x = np.append(x, np.cumsum(np.cos(phi)))
#     y = np.append(y, np.cumsum(np.sin(phi)))
#     return x, y

# x, y = random_walk(1000)
# plt.plot(x, y, color="black", label="percorso random walk")
# X_extr = [x[0], x[len(x)-1]]
# Y_extr = [y[0], y[len(y)-1]]
# plt.plot(X_extr, Y_extr, "bo", linestyle="--", color="grey", label="spostamento totale")
# plt.plot(x[0], y[0], "o", color="blue", label="inizio")
# plt.plot(x[len(x)-1], y[len(y)-1], "o", color="red", label="fine")
# plt.legend()
# plt.grid()
# plt.show()

def random_walk(num_steps=1000):
    phi = np.random.uniform(0., 2. * np.pi, size=num_steps)
    x = np.sum(np.cos(phi))
    y = np.sum(np.sin(phi))
    return x, y

# def random_walk(num_steps=1000):
#     x = np.zeros(num_steps + 1)
#     y = np.zeros(num_steps + 1)
#     phi = np.random.uniform(0., 2. * np.pi, size=num_steps)
#     np.cumsum(np.cos(phi), out=x[1:])
#     np.cumsum(np.sin(phi), out=y[1:])
    
#     return x, y

# for _ in range(10):
#     x, y = random_walk(1000)
#     print(f"Final position: ({x:.2f}, {y:.2f})")

def gauss(x, A, mu, sigma):
   return A / sigma / np.sqrt(2. * np.pi) * np.exp(-(x - mu) ** 2 / (2. * sigma ** 2))

N = 100000
n = 1000
bin_width = 2.
d_bin_width = 10.

x = []
y = []
for i in range(N):
    x_i, y_i = random_walk(n)
    x.append(x_i)
    y.append(y_i)

plt.figure(1)
o_i, bins, _ = plt.hist(x, bins=np.arange(-80., 80., bin_width), label="Observed")
bin_centers = (bins[:-1] + bins[1:]) / 2.

e_i = gauss(bin_centers, N * bin_width, 0., np.sqrt(n / 2.))

ndof = len(o_i)
chi2_1 = np.sum((o_i - e_i) ** 2. / e_i)

mediaX = np.mean(x)
print(f"Media x: {mediaX}")

print(f"Deviazione std: {np.std(x)} aspettata = {np.sqrt(n / 2)}")

print(f"Chi-squared: {chi2_1:.2f} / {ndof} dof")

plt.plot(bin_centers, e_i, 'r-', label='Expected')
plt.legend()

fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True, height_ratios=[3, 1])
d_quadro = np.empty(len(x))
for i in range(len(x)):
    d_quadro[i] = x[i]**2 + y[i]**2

def distribuzione_esponenziale(d, larg_bin):
    return (np.exp(-d/n) / n) * len(x) * larg_bin

d_oss, d_bins, _ = ax1.hist(d_quadro, bins=np.arange(0., 4000., d_bin_width))
d_bin_centers = (d_bins[:-1] + d_bins[1:]) / 2.
d_aspettati = distribuzione_esponenziale(d_bin_centers, d_bin_width)
residui = d_oss - d_aspettati
sigma_residui = np.std(residui)
residui = residui/sigma_residui
ax1.plot(d_bin_centers, d_aspettati,"r-", color="red")
ax2.axhline(0, color='black', linestyle='dashed')
ax2.errorbar(d_bin_centers, residui, sigma_residui, fmt='.')
ax2.grid()
#plt.plot(d_quadro, p_d_dquadro, ".")
plt.show()