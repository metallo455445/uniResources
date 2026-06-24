import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.colors import LogNorm
from scipy import constants

class Particella:
    def __init__(self, nome, massa, posizione=(0.0, 0.0, 0.0), velocita=(0.0, 0.0, 0.0)):
        self.nome = nome 
        self.massa = massa
        
        self.pos = np.array(posizione, dtype=float)
        self.vel = np.array(velocita, dtype=float)
        self.acc = np.zeros(3, dtype=float)
        self.forzaTOT = np.zeros(3, dtype=float)
        self.EPOT = 0
        
        #Array per salvare la "storia" delle posizioni (per tracciare la scia)
        self.storia_pos = [self.pos.copy()]

    def printinfo(self):
        pos_str = f"({self.pos[0]:.2f}, {self.pos[1]:.2f}, {self.pos[2]:.2f})"
        vel_str = f"({self.vel[0]:.2f}, {self.vel[1]:.2f}, {self.vel[2]:.2f})"
        print(f"[{self.nome}] Posizione: {pos_str} | Velocità: {vel_str}")

    def set_force(self, force):
        self.forzaTOT += force
    
    def set_Epo(self,pot):
        self.EPOT += pot

    def update(self, dt):
        # Seconda legge della dinamica
        self.acc = self.forzaTOT / self.massa 
        
        #aggiornamento velocità accelerazione
        self.vel += self.acc * dt
        self.pos += self.vel * dt
        
        #salva la posizione corrente per la scia
        self.storia_pos.append(self.pos.copy())
        
        #Azzera forza e potenziale per il frame successivo!
        self.forzaTOT = np.zeros(3, dtype=float)
        self.EPOT = 0


# --- IMPOSTAZIONE DELLA SIMULAZIONE ---
particelle = [
    Particella("P1", massa=2.0 * 10**12, posizione=(0,0,0), velocita=(0,0,0)), 
    Particella("P2", massa=10.0**7, posizione=(5.0,0,0), velocita=(0, np.sqrt((constants.G * 2.0 * 10**12) / 5.0), 0)),
    #Particella("P3", massa=11.0**9, posizione=(0,2.5,0), velocita=(0,1,5)),
    # Particella("P1", 10**12, (2.5,0,0),(0,2,0)),
    # Particella("P2", 10**9, (-2.5,0,0),(0,-2,0))
]

def gravitazione(parti):
    for i in range(len(parti)):
        for j in range(i + 1, len(parti)):
            p1 = parti[i]
            p2 = parti[j]

            r_vec = p2.pos - p1.pos
            distanza = np.linalg.norm(r_vec)

            if distanza < 1e-5:
                continue
            
            F_mag = (constants.G * p1.massa * p2.massa) / (distanza**2)
            F_vec = F_mag * (r_vec / distanza)

            pot = -(constants.G * p1.massa * p2.massa) / (distanza)

            p1.set_Epo(pot/2)
            p2.set_Epo(pot/2)

            p1.set_force(F_vec)
            p2.set_force(-F_vec)

def calcola_cm(parti):
    massa_tot = sum(p.massa for p in parti)
    pos_cm_numeratore = sum(p.massa * p.pos for p in parti)
    return pos_cm_numeratore / massa_tot

def momento_angolare(parti, rCM):
    l0tot = 0
    for p in parti:
        r_vec = p.pos - rCM
        
        r_vec = r_vec*p.massa

        L0 = np.cross(r_vec, p.vel)
        l0tot += L0
        print(f"L0[{p.nome}]: {L0}")
    print(f"L0 TOTALE: {l0tot}")

def gradiente(X,Y):
    U = np.zeros_like(X, dtype=float)
    V = np.zeros_like(X, dtype=float)

    for p in particelle:
        massa = p.massa
        x0 = p.pos[0]
        y0 = p.pos[1]

        #distande del punto dalla massa
        dx = X - x0
        dy = Y - y0

        dist_quadro = dx**2 + dy**2

        dist_cubo = (dist_quadro + 1e-5)**(1.5)

        #somma componenti vettoriali
        U -= (constants.G * massa * dx) / dist_cubo 
        V -= (constants.G * massa * dy) / dist_cubo

        limite_massimo = 50.0 # Regola questo numero provando
        U = np.clip(U, -limite_massimo, limite_massimo)
        V = np.clip(V, -limite_massimo, limite_massimo)

    return U, V

def energia(parti):
    Etot = 0
    for p in parti:
        E = .5 * p.massa * (np.linalg.norm(p.vel))**2 + p.EPOT
        print(f"E[{p.nome}]: {E}")
        Etot += E
    print(f"E TOTALE: {Etot}")

# Impostazioni tempo 
tempo_totale = 10.0 
fps = 30           
frames = int(tempo_totale * fps)
dt = 1.0 / fps     

#Finestra 1: orbite
fig1 = plt.figure(figsize=(8, 8))
fig1.canvas.manager.set_window_title("Orbite")
ax1 = fig1.add_subplot(111, projection='3d')

# Limiti dello spazio
ax1.set_xlim(-8, 8)
ax1.set_ylim(-8, 8)  
ax1.set_zlim(-8, 8)
ax1.set_xlabel('X')
ax1.set_ylabel('Y')
ax1.set_zlabel('Z')

# Punti e scie
punti_grafici = [ax1.plot([], [], [], 'o', markersize=8, label=p.nome)[0] for p in particelle]
scie_grafiche = [ax1.plot([], [], [], '-', linewidth=1, alpha=0.5)[0] for _ in particelle]
punto_cm = ax1.plot([], [], [], '.', color='red', markersize=10, label="Centro di Massa")[0]
ax1.legend()

#FInestra 2: campo potenziale
fig2 = plt.figure()
fig2.canvas.manager.set_window_title("Campo potenziale")
ax2 = fig2.add_subplot()
x = np.linspace(-8, 8, 20)
y = np.linspace(-8, 8, 20)
X, Y = np.meshgrid(x,y)

#dichiarazioni colore
color_mesh = ax2.pcolormesh(X, Y, np.zeros_like(X), 
                             cmap='inferno', norm=LogNorm(vmin=1e-3, vmax=1e3), 
                             shading='gouraud')

#colorbar laterale come legenda
fig2.colorbar(color_mesh, ax=ax2, label='Intensità Gravitazionale [m/s^2]')

#calcolo campo vettoriale iniziale
U_iniziale, V_iniziale = gradiente(X,Y)
campo = ax2.quiver(X, Y, U_iniziale,V_iniziale)

def cicle1(frame):
    gravitazione(particelle)
    energia(particelle)
    
    for p, punto, scia in zip(particelle, punti_grafici, scie_grafiche):
        p.update(dt)
        p.printinfo()
        
        # Aggiornamento punto
        punto.set_data([p.pos[0]], [p.pos[1]])
        punto.set_3d_properties([p.pos[2]])
        
        # Aggiornamento scia
        storia = np.array(p.storia_pos)
        scia.set_data(storia[:, 0], storia[:, 1])
        scia.set_3d_properties(storia[:, 2])
        
    # Aggiornamento CM
    pos_cm = calcola_cm(particelle)
    momento_angolare(particelle, pos_cm)
    punto_cm.set_data([pos_cm[0]], [pos_cm[1]])
    punto_cm.set_3d_properties([pos_cm[2]])
            
    return punti_grafici + scie_grafiche + [punto_cm]

def cicle2(frame):
    #momemntaneo
    U, V = gradiente(X,Y)
    #aggiorna il campo
    campo.set_UVC(U,V)
    #calcola la magnitudo di ogni vettore
    intensita = np.hypot(U, V)
    
    #evito di avere 0
    intensita[intensita == 0] = 1e-9 
    
    #aggiorna i colori
    color_mesh.set_array(intensita.ravel())
    
    return color_mesh,

try:
    print("Avvio simulazione... l'orbita dovrebbe essere circolare!")
    ani1 = FuncAnimation(fig1, cicle1, frames=frames, interval=1000/fps, blit=False)
    ani2 = FuncAnimation(fig2, cicle2, frames=frames, interval=1000/fps, blit=False)
    plt.show()

except KeyboardInterrupt:
    print("\nSimulazione terminata.")