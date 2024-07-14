import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Definición del modelo de sistema
def system_model(y, t, a, b, c, d, m, n):
    x, y = y
    dx_dt = x * (a - b * x - m * y)
    dy_dt = y * (c - d * y - n * x)
    return [dx_dt, dy_dt]

# Implementación del método de Runge-Kutta de orden 4 (RK4)
def rk4(t0, tf, h, x0, y0, a, b, c, d, m, n):
    t_valores = np.arange(t0, tf + h, h)
    x_valores = np.zeros_like(t_valores)
    y_valores = np.zeros_like(t_valores)
    x_valores[0], y_valores[0] = x0, y0

    for i in range(1, len(t_valores)):
        t = t_valores[i-1]
        x = x_valores[i-1]
        y = y_valores[i-1]

        k1 = system_model([x, y], t, a, b, c, d, m, n)
        k2 = system_model([x + 0.5 * h * k1[0], y + 0.5 * h * k1[1]], t + 0.5 * h, a, b, c, d, m, n)
        k3 = system_model([x + 0.5 * h * k2[0], y + 0.5 * h * k2[1]], t + 0.5 * h, a, b, c, d, m, n)
        k4 = system_model([x + h * k3[0], y + h * k3[1]], t + h, a, b, c, d, m, n)

        x_valores[i] = x + (h / 6) * (k1[0] + 2 * k2[0] + 2 * k3[0] + k4[0])
        y_valores[i] = y + (h / 6) * (k1[1] + 2 * k2[1] + 2 * k3[1] + k4[1])

    return t_valores, x_valores, y_valores

# Solución analítica (simplificada) para el modelo
def system_analytical(x0, y0, a, b, c, d, m, n, t):
    # Aproximación simple; en la práctica, esto puede ser más complejo
    x = x0 * np.exp((a - b * x0 - m * y0) * t)
    y = y0 * np.exp((c - d * y0 - n * x0) * t)
    return x, y

# Función para ejecutar la simulación
def run_simulation():
    try:
        x0 = float(entry_x0.get())
        y0 = float(entry_y0.get())
        a = float(entry_a.get())
        b = float(entry_b.get())
        c = float(entry_c.get())
        d = float(entry_d.get())
        m = float(entry_m.get())
        n = float(entry_n.get())
        t0 = 0
        tf = 10
        h = 0.1

        # Limpiar la gráfica anterior
        ax.clear()

        # Solución numérica - RK4
        t_rk4, x_rk4, y_rk4 = rk4(t0, tf, h, x0, y0, a, b, c, d, m, n)

        # Solución analítica
        t_analytical = np.arange(t0, tf + h, h)
        x_analytical, y_analytical = system_analytical(x0, y0, a, b, c, d, m, n, t_analytical)

        # Actualizar la gráfica
        ax.plot(t_rk4, x_rk4, label='x (RK4)', color='blue')
        ax.plot(t_rk4, y_rk4, label='y (RK4)', color='red')
        ax.plot(t_analytical, x_analytical, '--', label='x (Analítica)', color='cyan')
        ax.plot(t_analytical, y_analytical, '--', label='y (Analítica)', color='orange')
        ax.set_xlabel('Tiempo')
        ax.set_ylabel('Población')
        ax.set_title('Modelo de Sistema - Soluciones Numéricas y Analíticas')
        ax.legend()
        ax.grid(True)

        # Mostrar la gráfica actualizada
        canvas.draw()
    except ValueError:
        messagebox.showerror("Error", "Por favor, ingrese valores numéricos válidos.")

# Crear la interfaz gráfica
root = tk.Tk()
root.title("Modelo de Sistema")

# Crear un marco para organizar los widgets
frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

# Entradas de parámetros
tk.Label(frame, text="Población inicial x (x0):").grid(row=0, column=0)
entry_x0 = tk.Entry(frame)
entry_x0.grid(row=0, column=1)

tk.Label(frame, text="Población inicial y (y0):").grid(row=1, column=0)
entry_y0 = tk.Entry(frame)
entry_y0.grid(row=1, column=1)

tk.Label(frame, text="Parámetro a:").grid(row=2, column=0)
entry_a = tk.Entry(frame)
entry_a.grid(row=2, column=1)

tk.Label(frame, text="Parámetro b:").grid(row=3, column=0)
entry_b = tk.Entry(frame)
entry_b.grid(row=3, column=1)

tk.Label(frame, text="Parámetro c:").grid(row=4, column=0)
entry_c = tk.Entry(frame)
entry_c.grid(row=4, column=1)

tk.Label(frame, text="Parámetro d:").grid(row=5, column=0)
entry_d = tk.Entry(frame)
entry_d.grid(row=5, column=1)

tk.Label(frame, text="Parámetro m:").grid(row=6, column=0)
entry_m = tk.Entry(frame)
entry_m.grid(row=6, column=1)

tk.Label(frame, text="Parámetro n:").grid(row=7, column=0)
entry_n = tk.Entry(frame)
entry_n.grid(row=7, column=1)

# Botón para ejecutar la simulación
button_run = tk.Button(frame, text="Ejecutar Simulación", command=run_simulation)
button_run.grid(row=8, columnspan=2, pady=10)

# Crear la figura y el canvas para la gráfica
fig, ax = plt.subplots(figsize=(8, 6))
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack()

# Iniciar la interfaz
root.mainloop()
