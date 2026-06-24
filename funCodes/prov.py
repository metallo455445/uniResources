import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# 1. Prepariamo i dati di base
x = np.linspace(0, 2 * np.pi, 100)

# 2. Creiamo la PRIMA finestra (Figure 1)
fig1, ax1 = plt.subplots()
fig1.canvas.manager.set_window_title('Finestra 1 - Seno')
line1, = ax1.plot([], [], 'r-', lw=2)
ax1.set_xlim(0, 2 * np.pi)
ax1.set_ylim(-1.5, 1.5)

# 3. Creiamo la SECONDA finestra (Figure 2)
fig2, ax2 = plt.subplots()
fig2.canvas.manager.set_window_title('Finestra 2 - Coseno')
line2, = ax2.plot([], [], 'b-', lw=2)
ax2.set_xlim(0, 2 * np.pi)
ax2.set_ylim(-1.5, 1.5)

# 4. Definiamo le funzioni di aggiornamento (Update) per ogni figura
def update_fig1(frame):
    # Calcola il seno spostato dal frame corrente
    y = np.sin(x + frame)
    line1.set_data(x, y)
    return line1,

def update_fig2(frame):
    # Calcola il coseno spostato dal frame corrente
    y = np.cos(x + frame)
    line2.set_data(x, y)
    return line2,

# Generiamo i frame (i valori che passeremo alle funzioni di update)
frames = np.linspace(0, 2 * np.pi, 128)

# 5. Creiamo le due animazioni
# NOTA CRITICA: È fondamentale assegnare FuncAnimation a una variabile!
ani1 = FuncAnimation(fig1, update_fig1, frames=frames,
                     interval=50, blit=True)

ani2 = FuncAnimation(fig2, update_fig2, frames=frames,
                     interval=50, blit=True)

# 6. Mostriamo entrambe le finestre
plt.show()