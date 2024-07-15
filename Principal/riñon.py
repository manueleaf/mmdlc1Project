import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from Matematicas import solve
import pandas as pd
import numpy as np
from Implement import ImplementacionModelos
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def riñon(self):
            tk.Label(self.dynamic_frame, text="Eficacia del líquido de diálisis (a):", bg="lightblue").pack(padx=10, pady=5, anchor="w")
            self.a_entry_value = tk.StringVar()
            a_entry = tk.Entry(self.dynamic_frame, textvariable=self.a_entry_value)
            a_entry.pack(padx=10, pady=5, anchor="w")

            tk.Label(self.dynamic_frame, text="Tasas de flujo volumétrico de la sangre (v):", bg="lightblue").pack(padx=10, pady=5, anchor="w")
            self.v_entry_value = tk.StringVar()
            v_entry = tk.Entry(self.dynamic_frame, textvariable=self.v_entry_value)
            v_entry.pack(padx=10, pady=5, anchor="w")
            
            tk.Label(self.dynamic_frame, text="Tasas de flujo del líquido de diálisis (V):", bg="lightblue").pack(padx=10, pady=5, anchor="w")
            self.V_entry_value = tk.StringVar()
            V_entry = tk.Entry(self.dynamic_frame, textvariable=self.V_entry_value)
            V_entry.pack(padx=10, pady=5, anchor="w")

            tk.Label(self.dynamic_frame, text="Condición inicial (x0) :", bg="lightblue").pack(padx=10, pady=5, anchor="w")
            self.x0_entry_value = tk.StringVar()
            x0_entry = tk.Entry(self.dynamic_frame, textvariable=self.x0_entry_value)
            x0_entry.pack(padx=10, pady=5, anchor="w")

            tk.Label(self.dynamic_frame, text="Condición inicial (y0) :", bg="lightblue").pack(padx=10, pady=5, anchor="w")
            self.y0_entry_value = tk.StringVar()
            y0_entry = tk.Entry(self.dynamic_frame, textvariable=self.y0_entry_value)
            y0_entry.pack(padx=10, pady=5, anchor="w")
            
            tk.Label(self.dynamic_frame, text="Cantidad de puntos  :", bg="lightblue").pack(padx=10, pady=5, anchor="w")
            self.t_puntos_entry_value = tk.StringVar()
            t_puntos_entry = tk.Entry(self.dynamic_frame, textvariable=self.t_puntos_entry_value)
            t_puntos_entry.pack(padx=10, pady=5, anchor="w")
            

            tk.Label(self.dynamic_frame, text="Tiempo :", bg="lightblue").pack(padx=10, pady=5, anchor="w")
            self.t_entry_value = tk.StringVar()
            t_entry = tk.Entry(self.dynamic_frame, textvariable=self.t_entry_value)
            t_entry.pack(padx=10, pady=5, anchor="w")
            
            def on_calculate():
                try:
                    a = float(self.a_entry_value.get())
                    v = float(self.v_entry_value.get())
                    V = float(self.V_entry_value.get())
                    t_ = float(self.t_entry_value.get())
                    x0_ = float(self.x0_entry_value.get())
                    y0_ = float(self.y0_entry_value.get())
                    
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
            