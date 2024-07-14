import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from scipy.integrate import odeint
import tkinter as tk
from tkinter import ttk

def competencia(NP, t, a, b, m, c, d, n):
    N, P = NP
    dN_dt = N * (a - b * N - m * P)
    dP_dt = P * (c - d * P - n * N)
    return [dN_dt, dP_dt]

def actualizar_plot():
    N0 = float(entry_N0.get())
    P0 = float(entry_P0.get())
    a = float(entry_a.get())
    b = float(entry_b.get())
    m = float(entry_m.get())
    c = float(entry_c.get())
    d = float(entry_d.get())
    n = float(entry_n.get())
    T = float(entry_time.get())
    
    y0 = [N0, P0]
    t = np.linspace(0, T, 500)
    params = (a, b, m, c, d, n)
    sol = odeint(competencia, y0, t, args=params)
    
    N, P = sol.T
    
    ax.clear()
    if plot_type.get() == 'N vs t':
        ax.plot(t, N, label='Especie 1 (N)', color='blue')
        ax.plot(t, P, label='Especie 2 (P)', color='red')
        ax.set_xlabel('Tiempo (t)')
        ax.set_ylabel('Población')
    else:
        ax.plot(N, P, label='Trayectoria', color='blue')
        ax.set_xlabel('Especie 1 (N)')
        ax.set_ylabel('Especie 2 (P)')
        
        # Definir la cuadrícula de puntos para el plano de fase
        N_values = np.linspace(0, max(N), 20)
        P_values = np.linspace(0, max(P), 20)
        N_grid, P_grid = np.meshgrid(N_values, P_values)

        # Calcular los valores de las derivadas en cada punto de la cuadrícula
        dN_dt, dP_dt = competencia([N_grid, P_grid], 0, a, b, m, c, d, n)

        # Graficar el campo de direcciones
        ax.quiver(N_grid, P_grid, dN_dt, dP_dt, color='gray')
        
        # Graficar las isoclinas
        N_isocline = c / d * np.ones_like(P_values)
        P_isocline = a / b * np.ones_like(N_values)
        ax.plot(N_values, N_isocline, 'g--', label='Isoclina N')
        ax.plot(P_isocline, P_values, 'm--', label='Isoclina P')

    ax.set_title('Modelo de Competencia entre Especies')
    ax.legend()
    ax.grid(True)
    canvas.draw()

def increment_entry(entry):
    value = float(entry.get())
    entry.delete(0, tk.END)
    entry.insert(0, str(value + 1))

def decrement_entry(entry):
    value = float(entry.get())
    entry.delete(0, tk.END)
    entry.insert(0, str(value - 1))

root = tk.Tk()
root.title("Modelo de Competencia entre Especies")

frame = ttk.Frame(root, padding="10")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

# Parámetros iniciales
ttk.Label(frame, text="Parámetros iniciales").grid(row=0, column=0, columnspan=2)

ttk.Label(frame, text="N0:").grid(row=1, column=0, sticky=tk.E)
entry_N0 = ttk.Entry(frame)
entry_N0.grid(row=1, column=1)
ttk.Button(frame, text="↑", command=lambda: increment_entry(entry_N0)).grid(row=1, column=2)
ttk.Button(frame, text="↓", command=lambda: decrement_entry(entry_N0)).grid(row=1, column=3)

ttk.Label(frame, text="P0:").grid(row=2, column=0, sticky=tk.E)
entry_P0 = ttk.Entry(frame)
entry_P0.grid(row=2, column=1)
ttk.Button(frame, text="↑", command=lambda: increment_entry(entry_P0)).grid(row=2, column=2)
ttk.Button(frame, text="↓", command=lambda: decrement_entry(entry_P0)).grid(row=2, column=3)

ttk.Label(frame, text="a:").grid(row=3, column=0, sticky=tk.E)
entry_a = ttk.Entry(frame)
entry_a.grid(row=3, column=1)
ttk.Button(frame, text="↑", command=lambda: increment_entry(entry_a)).grid(row=3, column=2)
ttk.Button(frame, text="↓", command=lambda: decrement_entry(entry_a)).grid(row=3, column=3)

ttk.Label(frame, text="b:").grid(row=4, column=0, sticky=tk.E)
entry_b = ttk.Entry(frame)
entry_b.grid(row=4, column=1)
ttk.Button(frame, text="↑", command=lambda: increment_entry(entry_b)).grid(row=4, column=2)
ttk.Button(frame, text="↓", command=lambda: decrement_entry(entry_b)).grid(row=4, column=3)

ttk.Label(frame, text="m:").grid(row=5, column=0, sticky=tk.E)
entry_m = ttk.Entry(frame)
entry_m.grid(row=5, column=1)
ttk.Button(frame, text="↑", command=lambda: increment_entry(entry_m)).grid(row=5, column=2)
ttk.Button(frame, text="↓", command=lambda: decrement_entry(entry_m)).grid(row=5, column=3)

ttk.Label(frame, text="c:").grid(row=6, column=0, sticky=tk.E)
entry_c = ttk.Entry(frame)
entry_c.grid(row=6, column=1)
ttk.Button(frame, text="↑", command=lambda: increment_entry(entry_c)).grid(row=6, column=2)
ttk.Button(frame, text="↓", command=lambda: decrement_entry(entry_c)).grid(row=6, column=3)

ttk.Label(frame, text="d:").grid(row=7, column=0, sticky=tk.E)
entry_d = ttk.Entry(frame)
entry_d.grid(row=7, column=1)
ttk.Button(frame, text="↑", command=lambda: increment_entry(entry_d)).grid(row=7, column=2)
ttk.Button(frame, text="↓", command=lambda: decrement_entry(entry_d)).grid(row=7, column=3)

ttk.Label(frame, text="n:").grid(row=8, column=0, sticky=tk.E)
entry_n = ttk.Entry(frame)
entry_n.grid(row=8, column=1)
ttk.Button(frame, text="↑", command=lambda: increment_entry(entry_n)).grid(row=8, column=2)
ttk.Button(frame, text="↓", command=lambda: decrement_entry(entry_n)).grid(row=8, column=3)

# Tiempo de simulación
ttk.Label(frame, text="Tiempo:").grid(row=9, column=0, sticky=tk.E)
entry_time = ttk.Entry(frame)
entry_time.grid(row=9, column=1)
ttk.Button(frame, text="↑", command=lambda: increment_entry(entry_time)).grid(row=9, column=2)
ttk.Button(frame, text="↓", command=lambda: decrement_entry(entry_time)).grid(row=9, column=3)

# Tipo de gráfica
plot_type = tk.StringVar(value='N vs t')
ttk.Radiobutton(frame, text='N vs t', variable=plot_type, value='N vs t').grid(row=10, column=0, columnspan=2)
ttk.Radiobutton(frame, text='Plano Fase (N vs P)', variable=plot_type, value='Plano Fase').grid(row=10, column=2, columnspan=2)

# Botón para actualizar la gráfica
button = ttk.Button(frame, text="Graficar", command=actualizar_plot)
button.grid(row=11, column=0, columnspan=4)

# Configuración de la gráfica
fig, ax = plt.subplots()
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().grid(row=1, column=0)

root.mainloop()
