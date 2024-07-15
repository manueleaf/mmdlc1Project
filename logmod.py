import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk

def runge_kutta_4(f, y0, t0, tf, h):
    t = np.arange(t0, tf + h, h)
    y = np.zeros(t.shape)
    y[0] = y0

    for i in range(1, len(t)):
        k1 = h * f(t[i-1], y[i-1])
        k2 = h * f(t[i-1] + h / 2, y[i-1] + k1 / 2)
        k3 = h * f(t[i-1] + h / 2, y[i-1] + k2 / 2)
        k4 = h * f(t[i-1] + h, y[i-1] + k3)
        y[i] = y[i-1] + (k1 + 2*k2 + 2*k3 + k4) / 6

    return t, y

def logistic_model(t, y, a, M, N):
    return a * y * (1 - (y / M)) * ((y / N) - 1)

class LogisticModelApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Modelo Logístico Modificado")

        self.create_widgets()

    def create_widgets(self):
        # Etiquetas y entradas para parámetros
        self.label_a = ttk.Label(self.root, text="a:")
        self.label_a.grid(column=0, row=0, padx=10, pady=5)
        self.entry_a = ttk.Entry(self.root)
        self.entry_a.grid(column=1, row=0, padx=10, pady=5)

        self.label_M = ttk.Label(self.root, text="M:")
        self.label_M.grid(column=0, row=1, padx=10, pady=5)
        self.entry_M = ttk.Entry(self.root)
        self.entry_M.grid(column=1, row=1, padx=10, pady=5)

        self.label_N = ttk.Label(self.root, text="N:")
        self.label_N.grid(column=0, row=2, padx=10, pady=5)
        self.entry_N = ttk.Entry(self.root)
        self.entry_N.grid(column=1, row=2, padx=10, pady=5)

        self.label_y0 = ttk.Label(self.root, text="y0:")
        self.label_y0.grid(column=0, row=3, padx=10, pady=5)
        self.entry_y0 = ttk.Entry(self.root)
        self.entry_y0.grid(column=1, row=3, padx=10, pady=5)

        self.label_t0 = ttk.Label(self.root, text="t0:")
        self.label_t0.grid(column=0, row=4, padx=10, pady=5)
        self.entry_t0 = ttk.Entry(self.root)
        self.entry_t0.grid(column=1, row=4, padx=10, pady=5)

        self.label_tf = ttk.Label(self.root, text="tf:")
        self.label_tf.grid(column=0, row=5, padx=10, pady=5)
        self.entry_tf = ttk.Entry(self.root)
        self.entry_tf.grid(column=1, row=5, padx=10, pady=5)

        self.label_h = ttk.Label(self.root, text="h:")
        self.label_h.grid(column=0, row=6, padx=10, pady=5)
        self.entry_h = ttk.Entry(self.root)
        self.entry_h.grid(column=1, row=6, padx=10, pady=5)

        # Botón para graficar
        self.button_plot = ttk.Button(self.root, text="Graficar", command=self.plot_model)
        self.button_plot.grid(column=0, row=7, columnspan=2, pady=10)

    def plot_model(self):
        try:
            a = float(self.entry_a.get())
            M = float(self.entry_M.get())
            N = float(self.entry_N.get())
            y0 = float(self.entry_y0.get())
            t0 = float(self.entry_t0.get())
            tf = float(self.entry_tf.get())
            h = float(self.entry_h.get())
        except ValueError:
            print("Por favor, ingrese valores numéricos válidos.")
            return

        def f(t, y):
            return logistic_model(t, y, a, M, N)

        t, y = runge_kutta_4(f, y0, t0, tf, h)

        plt.figure()
        plt.plot(t, y, label=f'a={a}, M={M}, N={N}')
        plt.xlabel('Tiempo (t)')
        plt.ylabel('y(t)')
        plt.title('Modelo Logístico Modificado')
        plt.legend()
        plt.grid(True)
        plt.show()

if __name__ == "__main__":
    root = tk.Tk()
    app = LogisticModelApp(root)
    root.mainloop()
