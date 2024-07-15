import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from scipy.integrate import odeint
import numpy as np
from ..POO.Implement import ImplementacionModelos
from ..POO.Matematicas import solve
import pandas as pd



class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Ventana Principal con Pestañas Coloreadas")
        self.root.geometry("700x400")

        # Crear el frame principal
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill="both", expand=True)

        # Crear el primer panel (izquierda) con un tamaño fijo y su contenido
        self.panel1 = tk.Frame(self.main_frame, bg="lightblue", width=250, height=400)
        self.panel1.pack(side="left", fill="y", anchor="n")

        self.combo_box = ttk.Combobox(self.panel1, values=["Modelo riñon artificial", "Modelo exponencial", "Modelo de producción de celulas rojas", "Opción 3"], state="readonly")
        self.combo_box.pack(padx=10, pady=10, fill="x")

        # Crear un frame para widgets dinámicos
        self.dynamic_frame = tk.Frame(self.panel1, bg="lightblue")
        self.dynamic_frame.pack(padx=10, pady=10, fill="both", expand=True)

        self.combo_box.bind("<<ComboboxSelected>>", self.update_label)

        # Crear el segundo panel (derecha) que se expande y su contenido
        self.panel2 = tk.Frame(self.main_frame, bg="green")
        self.panel2.pack(side="left", fill="both", expand=True)

        self.notebook = ttk.Notebook(self.panel2)
        self.tab1 = tk.Frame(self.notebook, bg="lightblue")
        self.tab2 = tk.Frame(self.notebook, bg="lightgreen")
        self.tab3 = tk.Frame(self.notebook, bg="lightcoral")
        self.notebook.add(self.tab1, text="Pestaña 1")
        self.notebook.add(self.tab2, text="Pestaña 2")
        self.notebook.add(self.tab3, text="Pestaña 3")
        self.notebook.pack(expand=True, fill="both")

    def clear_panel(self):
        for widget in self.dynamic_frame.winfo_children():
            widget.pack_forget()

    def update_label(self, event):
        self.clear_panel()
        selected_option = self.combo_box.get()
        if selected_option == "Modelo riñon artificial":
            tk.Label(self.dynamic_frame, text="Eficacia del líquido de diálisis :", bg="lightblue").pack(padx=10, pady=5, anchor="w")
            self.a_entry_value = tk.StringVar()
            a_entry = tk.Entry(self.dynamic_frame, textvariable=self.a_entry_value)
            a_entry.pack(padx=10, pady=5, anchor="w")

            tk.Label(self.dynamic_frame, text="Tasas de flujo volumétrico de la sangre :", bg="lightblue").pack(padx=10, pady=5, anchor="w")
            self.v_entry_value = tk.StringVar()
            v_entry = tk.Entry(self.dynamic_frame, textvariable=self.v_entry_value)
            v_entry.pack(padx=10, pady=5, anchor="w")
            
            tk.Label(self.dynamic_frame, text="Tasas de flujo del líquido de diálisis :", bg="lightblue").pack(padx=10, pady=5, anchor="w")
            self.V_entry_value = tk.StringVar()
            V_entry = tk.Entry(self.dynamic_frame, textvariable=self.V_entry_value)
            V_entry.pack(padx=10, pady=5, anchor="w")

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

                    def modelo_riñon_artificial_wrapper(r_, t, a, v, V):
                        modelo = ImplementacionModelos()
                        return modelo.modelo_riñon_artificial(r_, a, v, V)
                    condiciones_iniciales = [0.5, -0.5]
                    t = np.linspace(0,t_, 5)
                    soluciones = solve(modelo_riñon_artificial_wrapper, condiciones_iniciales, t, a, v, V)
                    df=pd.DataFrame(soluciones)
                    print(df.transpose())
                    self.update_treeview(df.transpose())
                except ValueError:
                    messagebox.showerror("Error", "Por favor, ingrese números válidos en todos los campos.")
            calculate_button = tk.Button(self.dynamic_frame, text="Calcular", command=on_calculate)
            calculate_button.pack(pady=10)
        elif selected_option == "Opción 2":
            print(2)
        elif selected_option == "Opción 3":
            print(3)
        elif selected_option == "Modelo exponencial":
            self.create_exponential_model_widgets()
        elif selected_option == "Modelo de producción de celulas rojas":
            self.create_celular_model_widgets()

    def create_exponential_model_widgets(self):
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

        tk.Button(self.dynamic_frame, text="Graficar", command=self.actualizar_grafica_exp).pack(padx=10, pady=5)

    def create_celular_model_widgets(self):
        # Crear widgets específicos para el modelo exponencial
        tk.Label(self.dynamic_frame, text="Número inicial de Células Rojas (R0):", bg="lightblue").pack(padx=10, pady=5, anchor="w")
        self.entry_R0 = tk.Entry(self.dynamic_frame)
        self.entry_R0.pack(padx=10, pady=5, anchor="e")

        tk.Label(self.dynamic_frame, text="Número inicial de Células Producidas (M0):", bg="lightblue").pack(padx=10, pady=5, anchor="w")
        self.entry_M0 = tk.Entry(self.dynamic_frame)
        self.entry_M0.pack(padx=10, pady=5, anchor="e")

        tk.Label(self.dynamic_frame, text="Fracción destruida por el bazo (a):", bg="lightblue").pack(padx=10, pady=5, anchor="w")
        self.entry_a = tk.Entry(self.dynamic_frame)
        self.entry_a.pack(padx=10, pady=5, anchor="e")

        tk.Label(self.dynamic_frame, text="Producción constante (g):", bg="lightblue").pack(padx=10, pady=5, anchor="w")
        self.entry_g = tk.Entry(self.dynamic_frame)
        self.entry_g.pack(padx=10, pady=5, anchor="e")

        tk.Label(self.dynamic_frame, text="Tiempo:", bg="lightblue").pack(padx=10, pady=5, anchor="w")
        self.entry_tiempo = tk.Entry(self.dynamic_frame)
        self.entry_tiempo.pack(padx=10, pady=5, anchor="e")

        tk.Button(self.dynamic_frame, text="Graficar", command=self.actualizar_grafica_cel).pack(padx=10, pady=5)


    def create_widgets(self):
        self.fig1, self.ax1 = plt.subplots()
        self.canvas1 = FigureCanvasTkAgg(self.fig1, master=self.tab1)
        self.canvas1.get_tk_widget().pack(padx=10, pady=5, fill="both", expand=True)

        self.fig2, self.ax2 = plt.subplots()
        self.canvas2 = FigureCanvasTkAgg(self.fig2, master=self.tab2)
        self.canvas2.get_tk_widget().pack(padx=10, pady=5, fill="both", expand=True)

        self.fig3, self.ax3 = plt.subplots()
        self.canvas3 = FigureCanvasTkAgg(self.fig3, master=self.tab3)
        self.canvas3.get_tk_widget().pack(padx=10, pady=5, fill="both", expand=True)

    def actualizar_grafica_exp(self):
        A0 = float(self.entry_A0.get())
        k = float(self.entry_k.get())
        T = float(self.entry_tiempo.get())

        condiciones_iniciales = [A0]
        t = np.linspace(0, T, 100)
        solucion = odeint(self.modelo_exponencial, condiciones_iniciales, t, args=(k,))

        A = solucion[:, 0]

        # Análisis Analítico
        self.ax1.clear()
        self.ax1.plot(t, A, label='Población (A)', color='blue')
        self.ax1.set_xlabel('Tiempo (t)')
        self.ax1.set_ylabel('Población (A)')
        self.ax1.set_title('Análisis Analítico')
        self.ax1.legend()
        self.ax1.grid(True)
        self.canvas1.draw()

        # Análisis Cualitativo
        self.ax2.clear()
        self.ax2.plot(t, A, label='Población (A)', color='red')
        self.ax2.set_xlabel('Tiempo (t)')
        self.ax2.set_ylabel('Población (A)')
        self.ax2.set_title('Análisis Cualitativo')
        self.ax2.legend()
        self.ax2.grid(True)
        self.canvas2.draw()

        # Análisis Numérico
        self.ax3.clear()
        self.ax3.plot(t, A, label='Población (A)', color='green')
        self.ax3.set_xlabel('Tiempo (t)')
        self.ax3.set_ylabel('Población (A)')
        self.ax3.set_title('Análisis Numérico')
        self.ax3.legend()
        self.ax3.grid(True)
        self.canvas3.draw()

    def actualizar_grafica_cel(self):
        A0 = float(self.entry_A0.get())
        k = float(self.entry_k.get())
        T = float(self.entry_tiempo.get())

        condiciones_iniciales = [A0]
        t = np.linspace(0, T, 100)
        solucion = odeint(self.modelo_exponencial, condiciones_iniciales, t, args=(k,))

        A = solucion[:, 0]

        # Análisis Analítico
        self.ax1.clear()
        self.ax1.plot(t, A, label='Población (A)', color='blue')
        self.ax1.set_xlabel('Tiempo (t)')
        self.ax1.set_ylabel('Población (A)')
        self.ax1.set_title('Análisis Analítico')
        self.ax1.legend()
        self.ax1.grid(True)
        self.canvas1.draw()

        # Análisis Cualitativo
        self.ax2.clear()
        self.ax2.plot(t, A, label='Población (A)', color='red')
        self.ax2.set_xlabel('Tiempo (t)')
        self.ax2.set_ylabel('Población (A)')
        self.ax2.set_title('Análisis Cualitativo')
        self.ax2.legend()
        self.ax2.grid(True)
        self.canvas2.draw()

        # Análisis Numérico
        self.ax3.clear()
        self.ax3.plot(t, A, label='Población (A)', color='green')
        self.ax3.set_xlabel('Tiempo (t)')
        self.ax3.set_ylabel('Población (A)')
        self.ax3.set_title('Análisis Numérico')
        self.ax3.legend()
        self.ax3.grid(True)
        self.canvas3.draw()

    def modelo_exponencial(self, A, t, k):
        dA_dt = k * A
        return dA_dt

    def update_treeview(self, df):
        # Limpiar Treeview
        self.treeview.delete(*self.treeview.get_children())
        # Configurar columnas y cabeceras
        self.treeview["columns"] = list(df.columns)
        for col in df.columns:
            self.treeview.heading(col, text=f"Columna {col+1}")
            self.treeview.column(col, width=100,anchor="center")
        # Insertar datos en Treeview
        for index, row in df.iterrows():
            rounded_values = [f"{value:.4f}" if isinstance(value, float) else value for value in row]
            self.treeview.insert("", "end", values=rounded_values)

if __name__ == "__main__":
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()
