import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from scipy.integrate import odeint
import numpy as np

def lotka_volterra_competicion(y, t, r1, r2, K1, K2, a, b):
    N1, N2 = y
    dN1dt = r1 * N1 * (1 - (N1 + a * N2) / K1)
    dN2dt = r2 * N2 * (1 - (N2 + b * N1) / K2)
    return [dN1dt, dN2dt]

def actualizar_plot():
    N1_0 = float(entry_N1_0.get())
    N2_0 = float(entry_N2_0.get())
    r1 = float(entry_r1.get())
    r2 = float(entry_r2.get())
    K1 = float(entry_K1.get())
    K2 = float(entry_K2.get())
    a = float(entry_a.get())
    b = float(entry_b.get())
    T = float(entry_time.get())
    
    y0 = [N1_0, N2_0]
    t = np.linspace(0, T, 500)
    params = (r1, r2, K1, K2, a, b)
    sol = odeint(lotka_volterra_competicion, y0, t, args=params)
    
    N1, N2 = sol.T
    
    ax.clear()
    if plot_type.get() == 'N vs t':
        ax.plot(t, N1, label='Especie 1 (N1)', color='blue')
        ax.plot(t, N2, label='Especie 2 (N2)', color='red')
        ax.set_xlabel('Tiempo (t)')
        ax.set_ylabel('Población')
    else:
        # Grafica las trayectorias
        ax.plot(N1, N2, label='Trayectoria', color='blue')
        ax.set_xlabel('Especie 1 (N1)')
        ax.set_ylabel('Especie 2 (N2)')
        
        # Definir la cuadrícula de puntos para el plano de fase
        N1_values = np.linspace(0, max(K1, K2), 20)
        N2_values = np.linspace(0, max(K1, K2), 20)
        N1_grid, N2_grid = np.meshgrid(N1_values, N2_values)

        # Calcular los valores de las derivadas en cada punto de la cuadrícula
        dN1_dt, dN2_dt = lotka_volterra_competicion([N1_grid, N2_grid], 0, r1, r2, K1, K2, a, b)

        # Graficar el campo de direcciones
        ax.quiver(N1_grid, N2_grid, dN1_dt, dN2_dt, color='gray')
        
        # Encuentra y grafica los puntos críticos
        critical_points = [(0, 0), (K1, 0), (0, K2)]
        for point in critical_points:
            ax.plot(point[0], point[1], 'ro')  # Punto de equilibrio en rojo
        
        # Graficar las isoclinas
        N1_isoclina = K1 - a * N2_values
        N2_isoclina = K2 - b * N1_values
        ax.plot(N1_isoclina, N2_values, 'g-', label='Isoclina N1')
        ax.plot(N1_values, N2_isoclina, 'm-', label='Isoclina N2')

    ax.set_title('Modelo Lotka-Volterra de Competición')
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
root.title("Modelo Lotka-Volterra de Competición")

frame = ttk.Frame(root, padding="10")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

# Parámetros de la especie #1
ttk.Label(frame, text="Especie #1").grid(row=0, column=0, columnspan=3)

ttk.Label(frame, text="N1(0):").grid(row=1, column=0, sticky=tk.E)
entry_N1_0 = ttk.Entry(frame)
entry_N1_0.grid(row=1, column=1)
ttk.Button(frame, text="↑", command=lambda: increment_entry(entry_N1_0)).grid(row=1, column=2)
ttk.Button(frame, text="↓", command=lambda: decrement_entry(entry_N1_0)).grid(row=1, column=3)

ttk.Label(frame, text="r1:").grid(row=2, column=0, sticky=tk.E)
entry_r1 = ttk.Entry(frame)
entry_r1.grid(row=2, column=1)
ttk.Button(frame, text="↑", command=lambda: increment_entry(entry_r1)).grid(row=2, column=2)
ttk.Button(frame, text="↓", command=lambda: decrement_entry(entry_r1)).grid(row=2, column=3)

ttk.Label(frame, text="K1:").grid(row=3, column=0, sticky=tk.E)
entry_K1 = ttk.Entry(frame)
entry_K1.grid(row=3, column=1)
ttk.Button(frame, text="↑", command=lambda: increment_entry(entry_K1)).grid(row=3, column=2)
ttk.Button(frame, text="↓", command=lambda: decrement_entry(entry_K1)).grid(row=3, column=3)

ttk.Label(frame, text="a:").grid(row=4, column=0, sticky=tk.E)
entry_a = ttk.Entry(frame)
entry_a.grid(row=4, column=1)
ttk.Button(frame, text="↑", command=lambda: increment_entry(entry_a)).grid(row=4, column=2)
ttk.Button(frame, text="↓", command=lambda: decrement_entry(entry_a)).grid(row=4, column=3)

# Parámetros de la especie #2
ttk.Label(frame, text="Especie #2").grid(row=0, column=4, columnspan=3)

ttk.Label(frame, text="N2(0):").grid(row=1, column=4, sticky=tk.E)
entry_N2_0 = ttk.Entry(frame)
entry_N2_0.grid(row=1, column=5)
ttk.Button(frame, text="↑", command=lambda: increment_entry(entry_N2_0)).grid(row=1, column=6)
ttk.Button(frame, text="↓", command=lambda: decrement_entry(entry_N2_0)).grid(row=1, column=7)

ttk.Label(frame, text="r2:").grid(row=2, column=4, sticky=tk.E)
entry_r2 = ttk.Entry(frame)
entry_r2.grid(row=2, column=5)
ttk.Button(frame, text="↑", command=lambda: increment_entry(entry_r2)).grid(row=2, column=6)
ttk.Button(frame, text="↓", command=lambda: decrement_entry(entry_r2)).grid(row=2, column=7)

ttk.Label(frame, text="K2:").grid(row=3, column=4, sticky=tk.E)
entry_K2 = ttk.Entry(frame)
entry_K2.grid(row=3, column=5)
ttk.Button(frame, text="↑", command=lambda: increment_entry(entry_K2)).grid(row=3, column=6)
ttk.Button(frame, text="↓", command=lambda: decrement_entry(entry_K2)).grid(row=3, column=7)

ttk.Label(frame, text="b:").grid(row=4, column=4, sticky=tk.E)
entry_b = ttk.Entry(frame)
entry_b.grid(row=4, column=5)
ttk.Button(frame, text="↑", command=lambda: increment_entry(entry_b)).grid(row=4, column=6)
ttk.Button(frame, text="↓", command=lambda: decrement_entry(entry_b)).grid(row=4, column=7)

# Tiempo de simulación
ttk.Label(frame, text="Tiempo:").grid(row=5, column=0, sticky=tk.E)
entry_time = ttk.Entry(frame)
entry_time.grid(row=5, column=1)
ttk.Button(frame, text="↑", command=lambda: increment_entry(entry_time)).grid(row=5, column=2)
ttk.Button(frame, text="↓", command=lambda: decrement_entry(entry_time)).grid(row=5, column=3)

# Tipo de gráfica
plot_type = tk.StringVar(value='N vs t')
ttk.Radiobutton(frame, text='N vs t', variable=plot_type, value='N vs t').grid(row=6, column=0, columnspan=2)
ttk.Radiobutton(frame, text='Plano Fase (N1 vs N2)', variable=plot_type, value='Plano Fase').grid(row=6, column=2, columnspan=2)

# Botón para actualizar la gráfica
button = ttk.Button(frame, text="Graficar", command=actualizar_plot)
button.grid(row=7, column=0, columnspan=8)

# Configuración de la gráfica
fig, ax = plt.subplots()
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().grid(row=1, column=0)

root.mainloop()
