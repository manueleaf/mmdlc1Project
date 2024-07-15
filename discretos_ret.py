import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import simpledialog

def modelo_discreto_con_retardo(X_k, X_k_minus_1, r):
    return X_k * np.exp(r * (1 - X_k_minus_1))

def runge_kutta_discreto(f, X0, X1, r, steps):
    X = [X0, X1]
    for k in range(1, steps):
        X_k = X[-1]
        X_k_minus_1 = X[-2]
        X_k_plus_1 = f(X_k, X_k_minus_1, r)
        X.append(X_k_plus_1)
    return X

def graficar_modelo(X0, X1, r, steps):
    valores = runge_kutta_discreto(modelo_discreto_con_retardo, X0, X1, r, steps)
    plt.figure(figsize=(10, 6))
    plt.plot(range(steps+1), valores, marker='o')
    plt.title('Modelo Discreto con Retardo')
    plt.xlabel('k')
    plt.ylabel('X_k')
    plt.grid(True)
    plt.show()

def obtener_variables():
    root = tk.Tk()
    root.withdraw()  # Oculta la ventana principal

    X0 = float(simpledialog.askstring("Entrada", "Ingrese el valor inicial X0:"))
    X1 = float(simpledialog.askstring("Entrada", "Ingrese el valor inicial X1:"))
    r = float(simpledialog.askstring("Entrada", "Ingrese el valor de r:"))
    steps = int(simpledialog.askstring("Entrada", "Ingrese el número de pasos:"))

    return X0, X1, r, steps

if __name__ == "__main__":
    X0, X1, r, steps = obtener_variables()
    graficar_modelo(X0, X1, r, steps)
