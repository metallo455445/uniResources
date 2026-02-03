# import numpy as np
# import matplotlib.pyplot as plt

# # Parametri
# steps = 10000
# c = 2
# x0 = 0.2

# # Inizializzazione
# x_values = np.zeros(steps)
# x = x0

# # Iterazione
# for step in range(steps*100):
#     x = c * x * (x - 1)
#     if step >= (steps*100)-steps:
#         x_values[step-(steps*100)] = x
#     if step % 100000 == 0:
#         print(f"step {step}, x = {x}")

# # Grafico
# plt.figure(figsize=(10, 5))
# plt.plot(x_values[:1000], lw=1)  # visualizza solo i primi 1000 per leggibilità
# plt.title(f"Evoluzione di x (c={c}, x₀={x0})")
# plt.xlabel("Iterazione")
# plt.ylabel("x")
# plt.grid(True)
# plt.tight_layout()
# plt.show()


import numpy as np
import matplotlib.pyplot as plt
from alive_progress import alive_bar

# Parametri
steps = 10000
x0 = 0.2
c_min = 1
c_max = 4.0
c_steps = 500  # numero di valori di c da testare

# Array per memorizzare i risultati
c_values = np.linspace(c_min, c_max, c_steps)

plt.figure(figsize=(12, 8))

with alive_bar(500) as bar:
    for c in c_values:
    # Inizializzazione
        x = x0
        
        # Iterazione
        for step in range(steps * 100):
            x = c * x * (x - 1)
        
        # Raccolta degli ultimi 10000 valori
        x_values = np.zeros(steps)
        for i in range(steps):
            x = c * x * (x - 1)
            x_values[i] = x
        
        # Plot: per ogni valore di c, plottiamo tutti i punti in x_values
        plt.plot([c] * len(x_values), x_values, 'k,', markersize=0.5, alpha=0.3)
        bar()

plt.title("Diagramma di biforcazione: x(n+1) = c·x·(x-1)")
plt.xlabel("Parametro c")
plt.ylabel("Valori di x (ultimi 10000 step)")
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()