import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
import tkinter as tk
from tkinter import simpledialog

def dydt(t, y, ve, vs, ce, V):
    return ve * ce - (vs / (V + (ve - vs))) * y

def runge_kutta_4(f, y0, t0, t1, h, ve, vs, ce, V):
    t = np.arange(t0, t1, h)
    y = np.zeros(len(t))
    y[0] = y0
    for i in range(1, len(t)):
        k1 = h * f(t[i-1], y[i-1], ve, vs, ce, V)
        k2 = h * f(t[i-1] + 0.5*h, y[i-1] + 0.5*k1, ve, vs, ce, V)
        k3 = h * f(t[i-1] + 0.5*h, y[i-1] + 0.5*k2, ve, vs, ce, V)
        k4 = h * f(t[i], y[i-1] + k3, ve, vs, ce, V)
        y[i] = y[i-1] + (k1 + 2*k2 + 2*k3 + k4) / 6
    return t, y

def plot_solution(t, y):
    plt.figure()
    plt.plot(t, y, label='y(t)')
    plt.xlabel('Tiempo')
    plt.ylabel('Cantidad de sustancia')
    plt.title('Modelo de disolución de sustancia')
    plt.legend()
    plt.grid(True)
    plt.show()

def main():
    root = tk.Tk()
    root.withdraw()

    y0 = float(simpledialog.askstring("Input", "Cantidad inicial de sustancia y0:"))
    t0 = float(simpledialog.askstring("Input", "Tiempo inicial t0:"))
    t1 = float(simpledialog.askstring("Input", "Tiempo final t1:"))
    h = float(simpledialog.askstring("Input", "Tamaño de paso h:"))
    ve = float(simpledialog.askstring("Input", "Velocidad de entrada ve:"))
    vs = float(simpledialog.askstring("Input", "Velocidad de salida vs:"))
    ce = float(simpledialog.askstring("Input", "Concentracion ce:"))
    V = float(simpledialog.askstring("Input", "Volumen V:"))

    t, y = runge_kutta_4(dydt, y0, t0, t1, h, ve, vs, ce, V)
    plot_solution(t, y)

if __name__ == "__main__":
    main()
