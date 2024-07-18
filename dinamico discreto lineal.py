import tkinter as tk
from tkinter import Toplevel, Label, Entry, Button, Text, Scrollbar, LEFT, RIGHT, Y, BOTH, END, VERTICAL
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Función para resolver el modelo dinámico discreto lineal
def modelo_dinamico_discreto_lineal(m, b, x0, num_steps):
    estados = [x0]
    x = x0
    for _ in range(num_steps):
        x = m * x + b
        estados.append(x)
    return estados

# Función para resolver el modelo con método de Runge-Kutta de 4º orden
def solve_model(m, b, x0, num_steps):
    def runge_kutta_4(f, y0, t, *args):
        n = len(t)
        y = np.zeros((n, len(y0)))
        y[0] = y0
        h = t[1] - t[0]

        for i in range(1, n):
            k1 = h * f(y[i-1], t[i-1], *args)
            k2 = h * f(y[i-1] + 0.5 * k1, t[i-1] + 0.5 * h, *args)
            k3 = h * f(y[i-1] + 0.5 * k2, t[i-1] + 0.5 * h, *args)
            k4 = h * f(y[i-1] + k3, t[i-1] + h, *args)
            y[i] = y[i-1] + (k1 + 2*k2 + 2*k3 + k4) / 6

        return y

    # Definir la función f para el modelo dinámico discreto lineal
    def f(x, t, m, b):
        return m * x + b

    # Definir el intervalo de tiempo discreto
    t = np.linspace(0, num_steps, num_steps + 1)

    # Convertir x0 a un numpy array para asegurar que sea iterable
    x0_array = np.array([x0])

    # Resolver con Runge-Kutta de 4º orden
    resultados_rk4 = runge_kutta_4(f, x0_array, t, m, b)

    return resultados_rk4.flatten()

# Función para mostrar la tabla comparativa en una nueva ventana
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
    
    # Calcular el error absoluto
    df['Error_c'] = np.abs(df['c_Exacta'] - df['c_RK4'])

    # Agregar los datos del DataFrame al widget de Text
    text.insert(END, df.to_string(index=False))

# Función para graficar la evolución de X en el tiempo
def plot_evolution_graph(resultados):
    plt.figure(figsize=(10, 6))
    plt.plot(resultados, marker='o', linestyle='-', color='b', label='X_k')
    plt.xlabel('k')
    plt.ylabel('Valor de X')
    plt.title('Evolución del modelo dinámico discreto lineal')
    plt.legend()
    plt.grid(True)
    plt.show()

# Función para graficar el diagrama de cobweb
def plot_cobweb_graph(resultados):
    cobweb_x = []
    cobweb_y = []
    for i in range(len(resultados) - 1):
        cobweb_x.extend([resultados[i], resultados[i + 1]])
        cobweb_y.extend([resultados[i + 1], resultados[i + 1]])
    
    plt.figure(figsize=(8, 8))
    plt.plot(cobweb_x, cobweb_y, marker='', linestyle='-', color='b')
    plt.plot([min(resultados), max(resultados)], [min(resultados), max(resultados)], linestyle='--', color='r')
    plt.title('Diagrama de Cobweb - Modelo Dinámico Discreto Lineal')
    plt.xlabel('x_t')
    plt.ylabel('x_{t+1}')
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# Función para ingresar los datos del modelo dinámico discreto lineal
def input_dynamic_data():
    input_window = Toplevel()
    input_window.title("Ingresar Datos del Modelo Dinámico Discreto Lineal")

    Label(input_window, text="Coeficiente m:").grid(row=0, column=0, padx=10, pady=5)
    m_entry = Entry(input_window)
    m_entry.grid(row=0, column=1, padx=10, pady=5)

    Label(input_window, text="Término constante b:").grid(row=1, column=0, padx=10, pady=5)
    b_entry = Entry(input_window)
    b_entry.grid(row=1, column=1, padx=10, pady=5)

    Label(input_window, text="Valor inicial de X (x0):").grid(row=2, column=0, padx=10, pady=5)
    x0_entry = Entry(input_window)
    x0_entry.grid(row=2, column=1, padx=10, pady=5)

    Label(input_window, text="Número de pasos de tiempo:").grid(row=3, column=0, padx=10, pady=5)
    num_steps_entry = Entry(input_window)
    num_steps_entry.grid(row=3, column=1, padx=10, pady=5)

    def on_submit():
        m = float(m_entry.get())
        b = float(b_entry.get())
        x0 = float(x0_entry.get())
        num_steps = int(num_steps_entry.get())
        input_window.destroy()

        # Resolver el modelo dinámico discreto lineal
        resultados = modelo_dinamico_discreto_lineal(m, b, x0, num_steps)
        
        # Resolver con Runge-Kutta 4º orden
        resultados_rk4 = solve_model(m, b, x0, num_steps)

        # Mostrar la gráfica de evolución
        plot_evolution_graph(resultados)
        
        # Mostrar resultados en una nueva ventana
        show_comparative_table(pd.DataFrame({
            'Tiempo': range(num_steps + 1),
            'c_Exacta': resultados,
            'c_RK4': resultados_rk4
        }))

    def on_cobweb():
        m = float(m_entry.get())
        b = float(b_entry.get())
        x0 = float(x0_entry.get())
        num_steps = int(num_steps_entry.get())

        # Resolver el modelo dinámico discreto lineal
        resultados = modelo_dinamico_discreto_lineal(m, b, x0, num_steps)

        plot_cobweb_graph(resultados)

    submit_button = Button(input_window, text="Generar Gráfica", command=on_submit)
    submit_button.grid(row=4, column=0, pady=10)

    cobweb_button = Button(input_window, text="Diagrama de Cobweb", command=on_cobweb)
    cobweb_button.grid(row=4, column=1, pady=10)

# Punto de entrada principal
if __name__ == "__main__":
    import tkinter as tk
    root = tk.Tk()
    root.withdraw()  # Ocultar la ventana principal

    input_dynamic_data()
    root.mainloop()
