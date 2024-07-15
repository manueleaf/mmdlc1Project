import numpy as np
import matplotlib.pyplot as plt
from tkinter import Tk, Label, Entry, Button

# Función para el modelo de células rojas usando Runge-Kutta de orden 4
def runge_kutta(R0, M0, a, g, days):
    R = [R0]
    M = [M0]
    dt = 1  # Usamos un paso de tiempo de 1 día

    for k in range(days):
        R_k = R[-1]
        M_k = M[-1]

        # Funciones de derivada
        def dR_dt(R, M):
            return (1 - a) * R + M

        def dM_dt(R):
            return g * a * R

        # Runge-Kutta de orden 4 para R
        k1_R = dR_dt(R_k, M_k)
        k1_M = dM_dt(R_k)
        
        k2_R = dR_dt(R_k + 0.5 * dt * k1_R, M_k + 0.5 * dt * k1_M)
        k2_M = dM_dt(R_k + 0.5 * dt * k1_R)
        
        k3_R = dR_dt(R_k + 0.5 * dt * k2_R, M_k + 0.5 * dt * k2_M)
        k3_M = dM_dt(R_k + 0.5 * dt * k2_R)
        
        k4_R = dR_dt(R_k + dt * k3_R, M_k + dt * k3_M)
        k4_M = dM_dt(R_k + dt * k3_R)
        
        R_k1 = R_k + (dt / 6) * (k1_R + 2 * k2_R + 2 * k3_R + k4_R)
        M_k1 = M_k + (dt / 6) * (k1_M + 2 * k2_M + 2 * k3_M + k4_M)

        R.append(R_k1)
        M.append(M_k1)

    return np.array(R), np.array(M)

# Función para graficar los resultados
def plot_results(days, R, M):
    t = np.arange(0, days + 1, 1)
    plt.figure(figsize=(12, 6))
    plt.plot(t, R, label='Número de Células Rojas (R)')
    plt.plot(t, M, label='Número de Células Producidas (M)')
    plt.xlabel('Días')
    plt.ylabel('Número de Células')
    plt.title('Producción de Células Rojas')
    plt.legend()
    plt.grid(True)
    plt.show()

# Función para manejar el botón de "Calcular"
def calculate():
    R0 = float(entry_R0.get())
    M0 = float(entry_M0.get())
    a = float(entry_a.get())
    g = float(entry_g.get())
    days = int(entry_days.get())

    R, M = runge_kutta(R0, M0, a, g, days)
    plot_results(days, R, M)

# Crear la interfaz gráfica
root = Tk()
root.title("Modelo de Producción de Células Rojas")

Label(root, text="Número inicial de Células Rojas (R0):").grid(row=0, column=0)
entry_R0 = Entry(root)
entry_R0.grid(row=0, column=1)

Label(root, text="Número inicial de Células Producidas (M0):").grid(row=1, column=0)
entry_M0 = Entry(root)
entry_M0.grid(row=1, column=1)

Label(root, text="Fracción destruida por el bazo (a):").grid(row=2, column=0)
entry_a = Entry(root)
entry_a.grid(row=2, column=1)

Label(root, text="Producción constante (g):").grid(row=3, column=0)
entry_g = Entry(root)
entry_g.grid(row=3, column=1)

Label(root, text="Número de días a simular:").grid(row=4, column=0)
entry_days = Entry(root)
entry_days.grid(row=4, column=1)

Button(root, text="Calcular", command=calculate).grid(row=5, columnspan=2)

root.mainloop()
