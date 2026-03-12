import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# 1. Parametri Inerzia (I1 < I2 < I3). I2 è l'asse intermedio.
I = np.array([1.0, 2.5, 4.0])

def dynamics(t, y):
    q, w = y[:4], y[4:]
    # Equazioni di Eulero
    dw = np.array([
        (I[1] - I[2]) * w[1] * w[2] / I[0],
        (I[2] - I[0]) * w[2] * w[0] / I[1],
        (I[0] - I[1]) * w[0] * w[1] / I[2]
    ])
    # Evoluzione quaternione (dq/dt = 0.5 * q * omega)
    dq = 0.5 * np.array([
        -q[1]*w[0] - q[2]*w[1] - q[3]*w[2],
         q[0]*w[0] + q[2]*w[2] - q[3]*w[1],
         q[0]*w[1] - q[1]*w[2] + q[3]*w[0],
         q[0]*w[2] + q[1]*w[1] - q[2]*w[0]
    ])
    return np.concatenate([dq, dw])

# 2. Integrazione (15 secondi per vedere i flip multipli)
t_eval = np.linspace(0, 15, 600)
w0 = [0.1, 10.0, 0.0] 
y0 = np.concatenate([[1,0,0,0], w0])
sol = solve_ivp(dynamics, [0, 15], y0, t_eval=t_eval, rtol=1e-10)

# Costanti di conservazione
E = 0.5 * np.sum(I * np.array(w0)**2)
L2 = np.sum((I * np.array(w0))**2)

# 3. Funzioni di rotazione
def rotate_vec(q, v):
    q0, q1, q2, q3 = q
    R = np.array([
        [1-2*(q2**2+q3**2), 2*(q1*q2-q0*q3), 2*(q1*q3+q0*q2)],
        [2*(q1*q2+q0*q3), 1-2*(q1**2+q3**2), 2*(q2*q3-q0*q1)],
        [2*(q1*q3-q0*q2), 2*(q2*q3+q0*q1), 1-2*(q1**2+q2**2)]
    ])
    return R @ v

# 4. Setup Grafico
fig = plt.figure(figsize=(16, 8))
ax1 = fig.add_subplot(121, projection='3d') # Racchetta
ax2 = fig.add_subplot(122, projection='3d') # Poinsot

scia_punta = []
herp_pts = []

def update(n):
    ax1.cla(); ax2.cla()
    q, w_body = sol.y[:4, n], sol.y[4:, n]
    w_world = rotate_vec(q, w_body)
    
    # --- SINISTRA: SPAZIO REALE ---
    punta_w = rotate_vec(q, np.array([0, 0, 3.0]))
    scia_punta.append(punta_w)
    ax1.plot([0, punta_w[0]], [0, punta_w[1]], [0, punta_w[2]], color='black', lw=4)
    ax1.scatter(*punta_w, color='red', s=80)
    if len(scia_punta) > 1:
        traj = np.array(scia_punta)
        ax1.plot(traj[:,0], traj[:,1], traj[:,2], color='blue', alpha=0.3)
    ax1.set_xlim(-4,4); ax1.set_ylim(-4,4); ax1.set_zlim(-4,4)
    ax1.set_title("Evoluzione della Racchetta (15s)")

    # --- DESTRA: SPAZIO DI POINSOT (w) ---
    herp_pts.append(w_world)
    
    # Griglie per le superfici
    u, v = np.mgrid[0:2*np.pi:30j, 0:np.pi:15j]
    
    # Ellissoide Energia (Verde)
    xe = np.sqrt(2*E/I[0])*np.cos(u)*np.sin(v)
    ye = np.sqrt(2*E/I[1])*np.sin(u)*np.sin(v)
    ze = np.sqrt(2*E/I[2])*np.cos(v)
    ax2.plot_wireframe(xe, ye, ze, color='green', alpha=0.07)
    
    # Ellissoide Momento Angolare (Blu) - Nello spazio w: (I1*w1)^2 + ... = L^2
    xl = (np.sqrt(L2)/I[0])*np.cos(u)*np.sin(v)
    yl = (np.sqrt(L2)/I[1])*np.sin(u)*np.sin(v)
    zl = (np.sqrt(L2)/I[2])*np.cos(v)
    ax2.plot_wireframe(xl, yl, zl, color='blue', alpha=0.07)

    # Polhode (Arancione) e punto solidale
    ax2.plot(sol.y[4,:n], sol.y[5,:n], sol.y[6,:n], color='orange', lw=2, label='Polhode')
    ax2.scatter(*w_body, color='red', s=40, label='Punto Polhode')
    
    # Herpolhode (Viola) e punto fisso
    if len(herp_pts) > 1:
        hp = np.array(herp_pts)
        ax2.plot(hp[:,0], hp[:,1], hp[:,2], color='purple', lw=1.5, alpha=0.7, label='Herpolhode')
    ax2.scatter(*w_world, color='purple', s=40, label='Punto Herpolhode')
    
    ax2.set_xlim(-12,12); ax2.set_ylim(-12,12); ax2.set_zlim(-12,12)
    ax2.set_title("Superfici di Conservazione e Traiettorie")
    ax2.legend(loc='upper left', fontsize='small')

ani = FuncAnimation(fig, update, frames=len(t_eval), interval=20)
plt.show()
