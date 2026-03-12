import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Slider

# --- Parametri iniziali ---
m = 1.0          
g = 9.81         
dt = 0.02

k_init = 10.0
mus_init = 0.8
v_belt_init = 0.5
mud_ratio = 0.7  

# --- Configurazione Grafica ---
fig, (ax_anim, ax_graph) = plt.subplots(2, 1, figsize=(10, 9), gridspec_kw={'height_ratios': [1, 1.5]})
plt.subplots_adjust(bottom=0.25, hspace=0.4)

# 1. Setup Animazione
ax_anim.set_xlim(-1, 5)
ax_anim.set_ylim(-0.5, 1)
ax_anim.set_title("Simulazione Stick-Slip con Velocità")

# Elementi nastro (tacche mobili)
num_ticks = 15
ticks_x = np.linspace(-1, 5, num_ticks)
line_belt_ticks, = ax_anim.plot([], [], color='gray', lw=1, zorder=1)
ax_anim.axhline(0, color='black', lw=2, zorder=2) # Linea nastro

line_spring, = ax_anim.plot([], [], 'blue', lw=2, zorder=2)
patch_box = plt.Rectangle((0, 0), 0.4, 0.4, fc='orange', ec='black', zorder=4)
ax_anim.add_patch(patch_box)

# 2. Setup Grafici (Posizione e Velocità)
ax_pos = ax_graph
ax_vel = ax_graph.twinx() # Secondo asse per la velocità

ax_pos.set_xlim(0, 10)
ax_pos.set_ylim(0, 5)
ax_pos.set_xlabel("Tempo (s)")
ax_pos.set_ylabel("Posizione (m)", color='blue')
ax_vel.set_ylabel("Velocità (m/s)", color='green')

line_stick, = ax_pos.plot([], [], color='blue', lw=2, label='Pos (Stick)')
line_slip, = ax_pos.plot([], [], color='red', lw=2, label='Pos (Slip)')
line_v_box, = ax_vel.plot([], [], color='green', lw=1.5, alpha=0.7, label='Vel Cassa')
line_v_belt, = ax_vel.plot([], [], color='black', lw=1, ls='--', label='Vel Nastro')

# Uniamo le legende
lines = [line_stick, line_slip, line_v_box, line_v_belt]
ax_pos.legend(lines, [l.get_label() for l in lines], loc='upper left', fontsize='small')

# --- Slider ---
ax_k = plt.axes([0.2, 0.12, 0.6, 0.02])
ax_mu = plt.axes([0.2, 0.08, 0.6, 0.02])
ax_v = plt.axes([0.2, 0.04, 0.6, 0.02])

s_k = Slider(ax_k, 'Molla (k)', 5.0, 50.0, valinit=k_init)
s_mu = Slider(ax_mu, 'Attrito (mu_s)', 0.1, 1.5, valinit=mus_init)
s_v = Slider(ax_v, 'Vel. Nastro (v)', 0.1, 2.0, valinit=v_belt_init)

# --- Variabili di stato ---
state = {'x': 0.0, 'v': v_belt_init, 'stick': True, 't': 0.0}
history = {'t': [], 'x_stick': [], 'x_slip': [], 'v_box': [], 'v_belt': []}

def update_physics():
    k, mu_s, v_b = s_k.val, s_mu.val, s_v.val
    mu_d = mu_s * mud_ratio
    fs_max, fd = mu_s * m * g, mu_d * m * g
    force_spring = -k * state['x']
    
    if state['stick']:
        state['v'] = v_b
        state['x'] += v_b * dt
        if abs(force_spring) > fs_max: state['stick'] = False
    else:
        v_rel = state['v'] - v_b
        force_friction = -np.sign(v_rel) * fd
        a = (force_spring + force_friction) / m
        state['v'] += a * dt
        state['x'] += state['v'] * dt
        if abs(state['v'] - v_b) < 0.02 and abs(force_spring) < fs_max:
            state['v'] = v_b
            state['stick'] = True

def animate(i):
    global ticks_x
    update_physics()
    state['t'] += dt
    
    # Movimento nastro (tacche)
    ticks_x += s_v.val * dt
    ticks_x[ticks_x > 5] = -1 # Riposiziona le tacche che escono a destra
    
    # Memorizzazione dati
    history['t'].append(state['t'])
    history['v_box'].append(state['v'])
    history['v_belt'].append(s_v.val)
    if state['stick']:
        history['x_stick'].append(state['x'])
        history['x_slip'].append(np.nan)
    else:
        history['x_slip'].append(state['x'])
        history['x_stick'].append(np.nan)
    
    if len(history['t']) > 800:
        for key in history: history[key].pop(0)
    
    # Aggiornamento grafici
    line_spring.set_data([-0.8, state['x']], [0.2, 0.2])
    patch_box.set_xy((state['x'], 0))
    
    # Disegna tacche nastro come segmenti verticali
    t_lines_x = np.repeat(ticks_x, 2)
    t_lines_y = np.tile([0, -0.1], num_ticks)
    line_belt_ticks.set_data(ticks_x, [-0.05]*num_ticks) # Rappresentazione semplificata con punti
    # Per vedere meglio le tacche usiamo uno scatter o plot custom
    line_belt_ticks.set_marker('|')
    line_belt_ticks.set_markersize(10)
    
    line_stick.set_data(history['t'], history['x_stick'])
    line_slip.set_data(history['t'], history['x_slip'])
    line_v_box.set_data(history['t'], history['v_box'])
    line_v_belt.set_data(history['t'], history['v_belt'])
    
    ax_pos.set_xlim(max(0, state['t'] - 10), state['t'] + 1)
    # Autoscale per la velocità
    ax_vel.set_ylim(-2, max(3, s_v.val + 1))
    
    return line_spring, patch_box, line_stick, line_slip, line_v_box, line_v_belt, line_belt_ticks

ani = FuncAnimation(fig, animate, interval=20, blit=True, cache_frame_data=False)
plt.show()
