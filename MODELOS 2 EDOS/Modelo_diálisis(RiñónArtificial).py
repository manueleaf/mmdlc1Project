import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
import pandas as pd
from tkinter import Toplevel, Label, Text, Scrollbar, Entry, Button, LEFT, RIGHT, Y, BOTH, END, VERTICAL

# Definición del modelo de diálisis
def modelo(r, t, a, v, V):
    x, y = r
    dx_dt = a / v * (y - x)
    dy_dt = a / V * (x - y)
    return np.array([dx_dt, dy_dt])

# Solución del modelo de diálisis usando odeint y RK4
def solve_dialysis_model(a, v, V, x0, y0, time, num_points):
    condiciones_iniciales = np.array([x0, y0])
    t = np.linspace(0, time, num_points)
    sol_exacta = odeint(modelo, condiciones_iniciales, t, args=(a, v, V))
    x_exacta, y_exacta = sol_exacta.T

    sol_rk4 = runge_kutta_4(modelo, condiciones_iniciales, t, a, v, V)
    x_rk4, y_rk4 = sol_rk4.T

    error_x = np.abs(x_exacta - x_rk4)
    error_y = np.abs(y_exacta - y_rk4)

    df_comparativa = pd.DataFrame({
        'Tiempo': t,
        'x_Exacta': x_exacta,
        'y_Exacta': y_exacta,
        'x_RK4': x_rk4,
        'y_RK4': y_rk4,
        'Error_x': error_x,
        'Error_y': error_y
    })

    # Mostrar la tabla comparativa en una ventana
    show_comparative_table(df_comparativa)

    # Graficar la comparación entre la solución exacta y RK4
    plt.figure(figsize=(10, 8))
    plt.plot(t, x_exacta, label='Concentración de impurezas en la sangre (x) - Exacta')
    plt.plot(t, y_exacta, label='Concentración de impurezas en el líquido de diálisis (y) - Exacta')
    plt.plot(t, x_rk4, '--', label='Concentración de impurezas en la sangre (x) - RK4')
    plt.plot(t, y_rk4, '--', label='Concentración de impurezas en el líquido de diálisis (y) - RK4')
    plt.xlabel('Tiempo')
    plt.ylabel('Concentración')
    plt.legend()
    plt.title('Comparación entre la solución exacta y RK4')
    plt.show()

# Implementación del método de Runge-Kutta de 4º orden
def runge_kutta_4(f, y0, t, a, v, V):
    n = len(t)
    y = np.zeros((n, len(y0)))
    y[0] = y0
    h = t[1] - t[0]

    for i in range(1, n):
        k1 = h * f(y[i-1], t[i-1], a, v, V)
        k2 = h * f(y[i-1] + 0.5 * k1, t[i-1] + 0.5 * h, a, v, V)
        k3 = h * f(y[i-1] + 0.5 * k2, t[i-1] + 0.5 * h, a, v, V)
        k4 = h * f(y[i-1] + k3, t[i-1] + h, a, v, V)
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

# Función para ingresar los datos del modelo de diálisis
def input_dialysis_data():
    input_window = Toplevel()
    input_window.title("Ingresar Datos del Modelo de Diálisis")

    Label(input_window, text="a:").grid(row=0, column=0, padx=10, pady=5)
    a_entry = Entry(input_window)
    a_entry.grid(row=0, column=1, padx=10, pady=5)

    Label(input_window, text="v:").grid(row=1, column=0, padx=10, pady=5)
    v_entry = Entry(input_window)
    v_entry.grid(row=1, column=1, padx=10, pady=5)

    Label(input_window, text="V:").grid(row=2, column=0, padx=10, pady=5)
    V_entry = Entry(input_window)
    V_entry.grid(row=2, column=1, padx=10, pady=5)

    Label(input_window, text="Concentración inicial de impurezas en la sangre (x0):").grid(row=3, column=0, padx=10, pady=5)
    x0_entry = Entry(input_window)
    x0_entry.grid(row=3, column=1, padx=10, pady=5)

    Label(input_window, text="Concentración inicial de impurezas en el líquido de diálisis (y0):").grid(row=4, column=0, padx=10, pady=5)
    y0_entry = Entry(input_window)
    y0_entry.grid(row=4, column=1, padx=10, pady=5)

    Label(input_window, text="Tiempo total:").grid(row=5, column=0, padx=10, pady=5)
    time_entry = Entry(input_window)
    time_entry.grid(row=5, column=1, padx=10, pady=5)

    Label(input_window, text="Número de puntos:").grid(row=6, column=0, padx=10, pady=5)
    num_points_entry = Entry(input_window)
    num_points_entry.grid(row=6, column=1, padx=10, pady=5)

    def on_submit():
        a = float(a_entry.get())
        v = float(v_entry.get())
        V = float(V_entry.get())
        x0 = float(x0_entry.get())
        y0 = float(y0_entry.get())
        time = float(time_entry.get())
        num_points = int(num_points_entry.get())
        input_window.destroy()
        
        solve_dialysis_model(a, v, V, x0, y0, time, num_points)

    def on_show_phase_plane():
        a = float(a_entry.get())
        v = float(v_entry.get())
        V = float(V_entry.get())
        input_window.destroy()
        
        show_phase_plane(a, v, V)

    submit_button = Button(input_window, text="Generar Gráfica", command=on_submit)
    submit_button.grid(row=7, columnspan=2, pady=10)

    phase_plane_button = Button(input_window, text="Mostrar Plano de Fases", command=on_show_phase_plane)
    phase_plane_button.grid(row=8, columnspan=2, pady=10)

# Función para encontrar puntos críticos
def find_critical_points(a, v, V):
    x_crit = [0]
    y_crit = [0]
    return x_crit, y_crit

# Función para mostrar el plano de fases
def show_phase_plane(a, v, V):
    x = np.linspace(-1, 1, 20)
    y = np.linspace(-1, 1, 20)
    X, Y = np.meshgrid(x, y)
    DX, DY = modelo([X, Y], 0, a, v, V)

    plt.figure(figsize=(10, 8))
    plt.streamplot(X, Y, DX, DY, color='blue')
    plt.quiver(X, Y, DX, DY, color='red')

    x_crit, y_crit = find_critical_points(a, v, V)
    plt.scatter(x_crit, y_crit, color='green', s=100, label='Puntos Críticos')
    plt.title('Plano de Fases con Puntos Críticos y Campo Vectorial')
    plt.xlabel('Concentración de impurezas en la sangre (x)')
    plt.ylabel('Concentración de impurezas en el líquido de diálisis (y)')
    plt.legend()
    plt.show()

# Punto de entrada principal
if __name__ == "__main__":
    import tkinter as tk
    root = tk.Tk()
    root.withdraw()  # Ocultar la ventana principal

    input_dialysis_data()
    root.mainloop()