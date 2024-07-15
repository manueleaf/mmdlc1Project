import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from Matematicas import solve
import pandas as pd
import numpy as np
from Implement import ImplementacionModelos
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def exponencial(self):
             # Crear widgets específicos para el modelo exponencial
        tk.Label(self.dynamic_frame, text="Población inicial (A0):", bg="lightblue").pack(padx=10, pady=5, anchor="w")
        self.entry_A0 = tk.Entry(self.dynamic_frame)
        self.entry_A0.pack(padx=10, pady=5, anchor="e")

        tk.Label(self.dynamic_frame, text="Tasa de crecimiento (k):", bg="lightblue").pack(padx=10, pady=5, anchor="w")
        self.entry_k = tk.Entry(self.dynamic_frame)
        self.entry_k.pack(padx=10, pady=5, anchor="e")

        tk.Label(self.dynamic_frame, text="Tiempo:", bg="lightblue").pack(padx=10, pady=5, anchor="w")
        self.entry_tiempo = tk.Entry(self.dynamic_frame)
        self.entry_tiempo.pack(padx=10, pady=5, anchor="e")
            
        def on_calculate():
                try:
                    A0 = float(self.entry_A0.get())
                    k = float(self.entry_k.get())
                    T = float(self.entry_tiempo.get())
                    
                    t_puntos = int(self.t_puntos_entry_value.get())
                    
                    def modelo_riñon_artificial_wrapper(r_, t, a, v, V):
                        modelo = ImplementacionModelos()
                        return modelo.modelo_riñon_artificial(r_, a, v, V)
                    
                    condiciones_iniciales = [x0_, y0_]
                    t = np.linspace(0, t_, t_puntos)
                    soluciones = solve(modelo_riñon_artificial_wrapper, condiciones_iniciales, t, a, v, V)
                    df = pd.DataFrame({
                        't' : t,
                        'x_exacta': soluciones[0],
                        'y_exacta': soluciones[1],
                        'x_rk4': soluciones[2],
                        'y_rk4': soluciones[3]
                    })
                    #print(df)
                    self.update_treeview(df)

                    x_exacta, y_exacta, x_rk4, y_rk4 = soluciones
                    self.plot_graph(t, x_exacta, y_exacta, x_rk4, y_rk4)
                    
                    # Mostrar el plano de fases
                    def modelo_riñon_artificial_phase_plane(r_, a, v, V):
                        modelo = ImplementacionModelos()
                        return modelo.modelo_riñon_artificial(r_, a, v, V)
                    

                    self.show_phase_plane(modelo_riñon_artificial_phase_plane, a, v, V)
                    
                except ValueError:
                    messagebox.showerror("Error", "Por favor, ingrese números válidos en todos los campos.")
            
        calculate_button = tk.Button(self.dynamic_frame, text="Calcular", command=on_calculate)
        calculate_button.pack(pady=10)