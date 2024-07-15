import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from Matematicas import solve
import pandas as pd
import numpy as np
from Implement import ImplementacionModelos
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Ventana Principal con Pestañas Coloreadas")
        self.root.geometry("900x600")

        # Configuración del ícono de la ventana
        try:
            image = Image.open('C:/Users/Adrian/Desktop/interfazMMCI/Imagenes/logo.png')
            photo = ImageTk.PhotoImage(image)
            self.root.iconphoto(True, photo)
        except Exception as e:
            print(f"No se pudo cargar el ícono: {e}")

        # Crear el frame principal
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill="both", expand=True)
        self.main_frame.pack_propagate(False)

        # Crear el primer panel (izquierda) con un tamaño fijo y su contenido
        self.panel1 = tk.Frame(self.main_frame, bg="lightblue", width=500, height=400)
        self.panel1.pack(side="left", fill="y")

        self.combo_box = ttk.Combobox(self.panel1, values=["Modelo riñon artificial", "Opción 2", "Opción 3"], state="readonly")
        self.combo_box.pack(padx=10, pady=10, fill="x")

        # Crear un frame para widgets dinámicos
        self.dynamic_frame = tk.Frame(self.panel1, bg="lightblue")
        self.dynamic_frame.pack(padx=10, pady=10, fill="both", expand=True)

        self.combo_box.bind("<<ComboboxSelected>>", self.update_label)

        # Crear el segundo panel (derecha) que se expande y su contenido
        self.panel2 = tk.Frame(self.main_frame, bg="green")
        self.panel2.pack(side="right", fill="both", expand=True)

        self.notebook = ttk.Notebook(self.panel2)
        self.tab1 = tk.Frame(self.notebook, bg="lightblue")
        self.tab2 = tk.Frame(self.notebook, bg="lightgreen")
        self.tab3 = tk.Frame(self.notebook, bg="lightcoral")
        self.notebook.add(self.tab1, text="Gráfica en el tiempo")
        self.notebook.add(self.tab2, text="Análisis Cualitativo")
        self.notebook.add(self.tab3, text="Análisis Numérico")
        self.notebook.pack(expand=True, fill="both")

        # Crear el Treeview en la pestaña 3
        self.treeview = ttk.Treeview(self.tab3, show='headings')
        self.treeview.pack(expand=True, fill="both")

        # Área para mostrar la gráfica del plano de fases en la pestaña 2
        self.phase_plane_canvas_frame = tk.Frame(self.tab2)
        self.phase_plane_canvas_frame.pack(expand=True, fill='both')

    def plot_graph(self, t, x_exacta, y_exacta, x_rk4, y_rk4):
        # Crear una figura y ejes
        fig = Figure(figsize=(6, 4), dpi=100)
        ax = fig.add_subplot(111)
        
        # Graficar las soluciones exactas y aproximadas
        ax.plot(t, x_exacta, 'b-', label='x_exacta (odeint)')
        ax.plot(t, y_exacta, 'g-', label='y_exacta (odeint)')
        ax.plot(t, x_rk4, 'r--', label='x_rk4 (RK4)')
        ax.plot(t, y_rk4, 'm--', label='y_rk4 (RK4)')
        
        # Configurar el gráfico
        ax.set_title('Gráfica en el Tiempo')
        ax.set_xlabel('Tiempo')
        ax.set_ylabel('Valor')
        ax.legend()
        
        # Integrar la figura con Tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.tab1)
        canvas.draw()
        canvas.get_tk_widget().pack(expand=True, fill='both')

    def show_phase_plane(self, model_func, *model_params):
        x = np.linspace(-1, 1, 10)
        y = np.linspace(-1, 1, 10)
        X, Y = np.meshgrid(x, y)
        
        # Calcular el campo vectorial
        DX, DY = np.array([model_func([x, y], *model_params) for x, y in zip(np.ravel(X), np.ravel(Y))]).T
        DX = DX.reshape(X.shape)
        DY = DY.reshape(Y.shape)

        fig = Figure(figsize=(6, 4), dpi=100)
        ax = fig.add_subplot(111)
        ax.streamplot(X, Y, DX, DY, color='blue')
        ax.quiver(X, Y, DX, DY, color='red')

        # Encontrar y graficar puntos críticos
        ax.set_xlabel('Concentración de impurezas en la sangre (x)')
        ax.set_ylabel('Concentración de impurezas en el líquido de diálisis (y)')
        # Integrar la figura con Tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.phase_plane_canvas_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(expand=True, fill='both')

    def clear_panel(self):
        for widget in self.dynamic_frame.winfo_children():
            widget.pack_forget()
    
    def update_label(self, event):
        self.clear_panel()
        selected_option = self.combo_box.get()
        if selected_option == "Modelo riñon artificial":
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
            
        elif selected_option == "Opción 2":
            print(2)
        elif selected_option == "Opción 3":
            print(3)

    def update_treeview(self, df):
        # Limpiar Treeview
        self.treeview.delete(*self.treeview.get_children())
        
        # Configurar columnas y cabeceras
        self.treeview["columns"] = list(df.columns)
        for col in df.columns:
            self.treeview.heading(col, text=col)
            self.treeview.column(col, width=100, anchor="center")
        
        # Insertar datos en Treeview
        for _, row in df.iterrows():
            rounded_values = [f"{value:.4f}" if isinstance(value, float) else value for value in row]
            self.treeview.insert("", "end", values=rounded_values)

if __name__ == "__main__":
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()
