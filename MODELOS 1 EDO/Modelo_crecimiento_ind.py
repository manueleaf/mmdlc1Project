import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
import pandas as pd
from tkinter import Toplevel, Label, Entry, Button, Text, Scrollbar, LEFT, RIGHT, Y, BOTH, END, VERTICAL

# Definición del modelo de crecimiento exponencial
def modelo_exponencial(N, t, r):
    dN_dt = r * N
    return dN_dt  # Devolver un valor unidimensional

# Solución del modelo de crecimiento exponencial usando odeint y RK4
def solve_exponential_model(r, N0, time, num_points):
    condiciones_iniciales = N0
    t = np.linspace(0, time, num_points)
    sol_exacta = odeint(modelo_exponencial, condiciones_iniciales, t, args=(r,))
    N_exacta = sol_exacta.T[0]

    sol_rk4 = runge_kutta_4(modelo_exponencial, condiciones_iniciales, t, r)
    N_rk4 = sol_rk4.T[0]

    error_N = np.abs(N_exacta - N_rk4)

    df_comparativa = pd.DataFrame({
        'Tiempo': t,
        'N_Exacta': N_exacta,
        'N_RK4': N_rk4,
        'Error_N': error_N
    })

    # Mostrar la tabla comparativa en una ventana
    show_comparative_table(df_comparativa)

    # Graficar la comparación entre la solución exacta y RK4
    plt.figure(figsize=(10, 8))
    plt.plot(t, N_exacta, label='Tamaño de la población (N) - Exacta')
    plt.plot(t, N_rk4, '--', label='Tamaño de la población (N) - RK4')
    plt.xlabel('Tiempo')
    plt.ylabel('Tamaño de la población')
    plt.legend()
    plt.title('Comparación entre la solución exacta y RK4')
    plt.show()

# Implementación del método de Runge-Kutta de 4º orden
def runge_kutta_4(f, y0, t, r):
    n = len(t)
    y = np.zeros((n, len([y0])))
    y[0] = y0
    h = t[1] - t[0]

    for i in range(1, n):
        k1 = h * f(y[i-1], t[i-1], r)
        k2 = h * f(y[i-1] + 0.5 * k1, t[i-1] + 0.5 * h, r)
        k3 = h * f(y[i-1] + 0.5 * k2, t[i-1] + 0.5 * h, r)
        k4 = h * f(y[i-1] + k3, t[i-1] + h, r)
        y[i] = y[i-1] + (k1 + 2*k2 + 2*k3 + k4) / 6

    return y

# Mostrar la tabla comparativa en una nueva ventana
def show_comparative_table(df):
    table_window = Toplevel()
    table_window.title("Tabla Comparativa")
    
    text = Text(table_window, wrap='none')
    text.pack(side=LEFT, fill=BOTH, expand=True)
    
    scrollbar = Scrollbar(table_window, orient=VERTICAL, command=text.yview)
    scrollbar.pack(side=RIGHT, fill=Y)
    
    text.configure(yscrollcommand=scrollbar.set)
    
    # Configurar Pandas para mostrar más decimales
    pd.set_option('display.float_format', lambda x: '%.5f' % x)
    
    # Agregar los datos del DataFrame al widget de Text
    text.insert(END, df.to_string(index=False))

# Función para graficar el plano de fase
def plot_phase_plane(r, N0, time, num_points):
    condiciones_iniciales = N0
    t = np.linspace(0, time, num_points)
    sol = odeint(modelo_exponencial, condiciones_iniciales, t, args=(r,))
    N = sol.T[0]

    dN_dt = r * N

    plt.figure(figsize=(10, 8))
    plt.plot(N, dN_dt, label='Plano de fase')
    plt.xlabel('Tamaño de la población (N)')
    plt.ylabel('dN/dt')
    plt.title('Plano de fase del modelo de crecimiento exponencial')
    plt.legend()
    plt.grid(True)
    plt.show()

# Función para ingresar los datos del modelo de crecimiento exponencial
def input_exponential_data():
    input_window = Toplevel()
    input_window.title("Ingresar Datos del Modelo de Crecimiento Exponencial")

    Label(input_window, text="r:").grid(row=0, column=0, padx=10, pady=5)
    r_entry = Entry(input_window)
    r_entry.grid(row=0, column=1, padx=10, pady=5)

    Label(input_window, text="Tamaño inicial de la población (N0):").grid(row=1, column=0, padx=10, pady=5)
    N0_entry = Entry(input_window)
    N0_entry.grid(row=1, column=1, padx=10, pady=5)

    Label(input_window, text="Tiempo total:").grid(row=2, column=0, padx=10, pady=5)
    time_entry = Entry(input_window)
    time_entry.grid(row=2, column=1, padx=10, pady=5)

    Label(input_window, text="Número de puntos:").grid(row=3, column=0, padx=10, pady=5)
    num_points_entry = Entry(input_window)
    num_points_entry.grid(row=3, column=1, padx=10, pady=5)

    def on_submit():
        r = float(r_entry.get())
        N0 = float(N0_entry.get())
        time = float(time_entry.get())
        num_points = int(num_points_entry.get())
        input_window.destroy()
        
        solve_exponential_model(r, N0, time, num_points)

    def on_phase_plane():
        r = float(r_entry.get())
        N0 = float(N0_entry.get())
        time = float(time_entry.get())
        num_points = int(num_points_entry.get())
        input_window.destroy()
        
        plot_phase_plane(r, N0, time, num_points)

    submit_button = Button(input_window, text="Generar Gráfica", command=on_submit)
    submit_button.grid(row=4, column=0, pady=10)

    phase_plane_button = Button(input_window, text="Generar Plano de Fase", command=on_phase_plane)
    phase_plane_button.grid(row=4, column=1, pady=10)

# Punto de entrada principal
if __name__ == "__main__":
    import tkinter as tk
    root = tk.Tk()
    root.withdraw()  # Ocultar la ventana principal

    input_exponential_data()
    root.mainloop()