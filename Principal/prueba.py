import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Ventana Principal con Pestañas Coloreadas")
        self.root.geometry("700x400")

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

        # Crear el primer panel (izquierda) con un tamaño fijo y su contenido
        self.panel1 = tk.Frame(self.main_frame, bg="lightblue", width=250, height=400)
        self.panel1.pack(side="left", fill="y", anchor="n")

        self.combo_box = ttk.Combobox(self.panel1, values=["Modelo riñon artificial", "Opción 2", "Opción 3"], state="readonly")
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
            tk.Label(self.dynamic_frame, text="Etiqueta:", bg="lightblue").pack(padx=10, pady=5, anchor="w")
            tk.Entry(self.dynamic_frame).pack(padx=10, pady=5, anchor="e")
        elif selected_option == "Opción 2":
            print(2)
        elif selected_option == "Opción 3":
            print(3)

if __name__ == "__main__":
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()
