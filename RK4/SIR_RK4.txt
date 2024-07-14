import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Definición del modelo SIR
def sir_model(y, t, beta, gamma, N):
    S, I, R = y
    dS_dt = -beta * S * I / N
    dI_dt = beta * S * I / N - gamma * I
    dR_dt = gamma * I
    return [dS_dt, dI_dt, dR_dt]

# Implementación del método de Runge-Kutta de orden 4 (RK4)
def rk4(t0, tf, h, S0, I0, R0, beta, gamma, N):
    t_valores = np.arange(t0, tf + h, h)
    S_valores = np.zeros_like(t_valores)
    I_valores = np.zeros_like(t_valores)
    R_valores = np.zeros_like(t_valores)
    S_valores[0], I_valores[0], R_valores[0] = S0, I0, R0

    for i in range(1, len(t_valores)):
        t = t_valores[i-1]
        S = S_valores[i-1]
        I = I_valores[i-1]
        R = R_valores[i-1]

        k1 = sir_model([S, I, R], t, beta, gamma, N)
        k2 = sir_model([S + 0.5 * h * k1[0], I + 0.5 * h * k1[1], R + 0.5 * h * k1[2]], t + 0.5 * h, beta, gamma, N)
        k3 = sir_model([S + 0.5 * h * k2[0], I + 0.5 * h * k2[1], R + 0.5 * h * k2[2]], t + 0.5 * h, beta, gamma, N)
        k4 = sir_model([S + h * k3[0], I + h * k3[1], R + h * k3[2]], t + h, beta, gamma, N)

        S_valores[i] = S + (h / 6) * (k1[0] + 2 * k2[0] + 2 * k3[0] + k4[0])
        I_valores[i] = I + (h / 6) * (k1[1] + 2 * k2[1] + 2 * k3[1] + k4[1])
        R_valores[i] = R + (h / 6) * (k1[2] + 2 * k2[2] + 2 * k3[2] + k4[2])

    return t_valores, S_valores, I_valores, R_valores

# Solución analítica para el modelo SIR (simplificada)
def sir_analytical(S0, I0, R0, beta, gamma, t, N):
    # Suponemos que la solución analítica es válida y se deriva de las ecuaciones SIR.
    # Esto puede requerir más complejidad dependiendo del modelo y sus suposiciones.
    # Esta es solo una aproximación para propósitos ilustrativos.
    S = S0 * np.exp(-beta * I0 * t / N)
    I = I0 * np.exp((beta * S0 / N - gamma) * t)
    R = R0 + (I0 - I)  # R = R0 + (I0 - I)
    return S, I, R

# Función para ejecutar la simulación
def run_simulation():
    try:
        S0 = int(entry_S0.get())
        I0 = int(entry_I0.get())
        R0 = int(entry_R0.get())
        beta = float(entry_beta.get())
        gamma = float(entry_gamma.get())
        N = S0 + I0 + R0  # Población total
        t0 = 0
        tf = 50
        h = 0.1

        # Limpiar la gráfica anterior
        ax.clear()

        # Solución numérica - RK4
        t_rk4, S_rk4, I_rk4, R_rk4 = rk4(t0, tf, h, S0, I0, R0, beta, gamma, N)

        # Solución analítica
        t_analytical = np.arange(t0, tf + h, h)
        S_analytical, I_analytical, R_analytical = sir_analytical(S0, I0, R0, beta, gamma, t_analytical, N)

        # Actualizar la gráfica
        ax.plot(t_rk4, S_rk4, label='Susceptibles (RK4)', color='blue')
        ax.plot(t_rk4, I_rk4, label='Infectados (RK4)', color='red')
        ax.plot(t_rk4, R_rk4, label='Recuperados (RK4)', color='green')
        ax.plot(t_analytical, S_analytical, '--', label='Susceptibles (Analítica)', color='cyan')
        ax.plot(t_analytical, I_analytical, '--', label='Infectados (Analítica)', color='orange')
        ax.plot(t_analytical, R_analytical, '--', label='Recuperados (Analítica)', color='purple')
        ax.set_xlabel('Tiempo')
        ax.set_ylabel('Población')
        ax.set_title('Modelo SIR - Soluciones Numéricas y Analíticas')
        ax.legend()
        ax.grid(True)

        # Mostrar la gráfica actualizada
        canvas.draw()
    except ValueError:
        messagebox.showerror("Error", "Por favor, ingrese valores numéricos válidos.")

# Crear la interfaz gráfica
root = tk.Tk()
root.title("Modelo SIR")

# Crear un marco para organizar los widgets
frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

# Entradas de parámetros
tk.Label(frame, text="Población inicial susceptible (S0):").grid(row=0, column=0)
entry_S0 = tk.Entry(frame)
entry_S0.grid(row=0, column=1)

tk.Label(frame, text="Población inicial infectada (I0):").grid(row=1, column=0)
entry_I0 = tk.Entry(frame)
entry_I0.grid(row=1, column=1)

tk.Label(frame, text="Población inicial recuperada (R0):").grid(row=2, column=0)
entry_R0 = tk.Entry(frame)
entry_R0.grid(row=2, column=1)

tk.Label(frame, text="Tasa de infección (beta):").grid(row=3, column=0)
entry_beta = tk.Entry(frame)
entry_beta.grid(row=3, column=1)

tk.Label(frame, text="Tasa de recuperación (gamma):").grid(row=4, column=0)
entry_gamma = tk.Entry(frame)
entry_gamma.grid(row=4, column=1)

# Botón para ejecutar la simulación
button_run = tk.Button(frame, text="Ejecutar Simulación", command=run_simulation)
button_run.grid(row=5, columnspan=2, pady=10)

# Crear la figura y el canvas para la gráfica
fig, ax = plt.subplots(figsize=(8, 6))
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack()

# Iniciar la interfaz
root.mainloop()
