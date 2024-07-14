import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Solución analítica para el modelo de Lotka-Volterra (simplificada)
def lotka_volterra_analytical(t, N0, P0, r1, r2, C1, C2):
    N = (N0 * r1) / (C1 * P0 + r1 * (1 - np.exp(-C1 * P0 * t)))
    P = (C2 * N0 * P0 * np.exp(-r2 * t)) / (C1 * P0 + r1 * (1 - np.exp(-C1 * P0 * t)))
    return N, P

# Implementación del método de Runge-Kutta de orden 4 (RK4)
def lotka_rk4(t0, tf, h, N0, P0, r1, r2, C1, C2):
    t_valores = np.arange(t0, tf + h, h)
    N_valores = np.zeros_like(t_valores)
    P_valores = np.zeros_like(t_valores)
    N_valores[0], P_valores[0] = N0, P0

    for i in range(1, len(t_valores)):
        t = t_valores[i-1]
        N = N_valores[i-1]
        P = P_valores[i-1]

        k1_N = r1 * N - C1 * N * P
        k1_P = -r2 * P + C2 * N * P

        k2_N = r1 * (N + 0.5 * h * k1_N) - C1 * (N + 0.5 * h * k1_N) * (P + 0.5 * h * k1_P)
        k2_P = -r2 * (P + 0.5 * h * k1_P) + C2 * (N + 0.5 * h * k1_N) * (P + 0.5 * h * k1_P)

        k3_N = r1 * (N + 0.5 * h * k2_N) - C1 * (N + 0.5 * h * k2_N) * (P + 0.5 * h * k2_P)
        k3_P = -r2 * (P + 0.5 * h * k2_P) + C2 * (N + 0.5 * h * k2_N) * (P + 0.5 * h * k2_P)

        k4_N = r1 * (N + h * k3_N) - C1 * (N + h * k3_N) * (P + h * k3_P)
        k4_P = -r2 * (P + h * k3_P) + C2 * (N + h * k3_N) * (P + h * k3_P)

        N_valores[i] = N + (h / 6) * (k1_N + 2 * k2_N + 2 * k3_N + k4_N)
        P_valores[i] = P + (h / 6) * (k1_P + 2 * k2_P + 2 * k3_P + k4_P)

    return t_valores, N_valores, P_valores

# Función para ejecutar la simulación
def run_simulation():
    try:
        N0 = int(entry_N0.get())
        P0 = int(entry_P0.get())
        r1 = float(entry_r1.get())
        r2 = float(entry_r2.get())
        C1 = float(entry_C1.get())
        C2 = float(entry_C2.get())
        t0 = 0
        tf = 10
        h = 0.1

        # Limpiar la gráfica anterior
        ax.clear()

        # Solución numérica - RK4
        t_rk4, N_rk4, P_rk4 = lotka_rk4(t0, tf, h, N0, P0, r1, r2, C1, C2)

        # Solución analítica
        t_analytical = np.arange(t0, tf + h, h)
        N_analytical, P_analytical = lotka_volterra_analytical(t_analytical, N0, P0, r1, r2, C1, C2)

        # Actualizar la gráfica
        ax.plot(t_rk4, N_rk4, 's', label='Presas (RK4)', color='cyan')
        ax.plot(t_rk4, P_rk4, 's', label='Depredadores (RK4)', color='magenta')
        ax.plot(t_analytical, N_analytical, '-', label='Presas (Solución Analítica)', color='blue')
        ax.plot(t_analytical, P_analytical, '-', label='Depredadores (Solución Analítica)', color='red')
        ax.set_xlabel('Tiempo')
        ax.set_ylabel('Población')
        ax.set_title('Comparación de Soluciones del Modelo Lotka-Volterra')
        ax.legend()
        ax.grid(True)

        # Mostrar la gráfica actualizada
        canvas.draw()
    except ValueError:
        messagebox.showerror("Error", "Por favor, ingrese valores numéricos válidos.")

# Crear la interfaz gráfica
root = tk.Tk()
root.title("Modelo de Lotka-Volterra")

# Crear un marco para organizar los widgets
frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

# Entradas de parámetros
tk.Label(frame, text="Población inicial de presas (N0):").grid(row=0, column=0)
entry_N0 = tk.Entry(frame)
entry_N0.grid(row=0, column=1)

tk.Label(frame, text="Población inicial de depredadores (P0):").grid(row=1, column=0)
entry_P0 = tk.Entry(frame)
entry_P0.grid(row=1, column=1)

tk.Label(frame, text="Tasa de crecimiento de presas (r1):").grid(row=2, column=0)
entry_r1 = tk.Entry(frame)
entry_r1.grid(row=2, column=1)

tk.Label(frame, text="Tasa de mortalidad de depredadores (r2):").grid(row=3, column=0)
entry_r2 = tk.Entry(frame)
entry_r2.grid(row=3, column=1)

tk.Label(frame, text="Tasa de depredación (C1):").grid(row=4, column=0)
entry_C1 = tk.Entry(frame)
entry_C1.grid(row=4, column=1)

tk.Label(frame, text="Tasa de crecimiento de depredadores (C2):").grid(row=5, column=0)
entry_C2 = tk.Entry(frame)
entry_C2.grid(row=5, column=1)

# Botón para ejecutar la simulación
button_run = tk.Button(frame, text="Ejecutar Simulación", command=run_simulation)
button_run.grid(row=6, columnspan=2, pady=10)

# Crear la figura y el canvas para la gráfica
fig, ax = plt.subplots(figsize=(8, 6))
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack()

# Iniciar la interfaz
root.mainloop()
