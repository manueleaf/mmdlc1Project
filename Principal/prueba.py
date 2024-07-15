import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from Matematicas import solve
import pandas as pd
import numpy as np
from Implement import ImplementacionModelos
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from riñon import riñon
from exponencial import exponencial

class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Ventana Principal con Pestañas Coloreadas")
        self.root.geometry("900x600")

        # Crear el frame principal
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill="both", expand=True)
        self.main_frame.pack_propagate(False)

        # Crear el primer panel (izquierda) con un tamaño fijo y su contenido
        self.panel1 = tk.Frame(self.main_frame, bg="lightblue", width=500, height=400)
        self.panel1.pack(side="left", fill="y")

        self.combo_box = ttk.Combobox(self.panel1, values=["Modelo riñon artificial", "Modelo Exponencial", "Modelo de producción de celulas rojas"], state="readonly")
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
            riñon(self)
        elif selected_option == "Modelo Exponencial":
            exponencial(self)
        elif selected_option == "Modelo de producción de celulas rojas":
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
