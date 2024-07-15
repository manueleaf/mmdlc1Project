import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from tkinter import Toplevel, Label, Entry, Button, Tk

# Función para dibujar la cadena de Markov y calcular distribución futura
def draw_markov_chain(transition_matrix, states, t):
    G = nx.DiGraph()

    # Agregar nodos
    for state in states:
        G.add_node(state)

    # Agregar aristas con probabilidades
    num_states = len(states)
    for i in range(num_states):
        for j in range(num_states):
            prob = transition_matrix[i][j]
            if prob > 0:
                G.add_edge(states[i], states[j], weight=prob, label=f'{prob:.2f}')

    # Dibujar el grafo con un diseño mejorado
    pos = nx.spring_layout(G)  # layout for better visualization
    edge_labels = nx.get_edge_attributes(G, 'label')
    
    # Dibujar nodos y aristas
    nx.draw_networkx_nodes(G, pos, node_size=500, node_color='skyblue', edgecolors='black')
    nx.draw_networkx_edges(G, pos, arrows=True, arrowstyle='->', arrowsize=20, edge_color='gray', connectionstyle='arc3,rad=0.1')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red', font_size=8, label_pos=0.2, bbox=dict(facecolor='white', edgecolor='none', alpha=0.01))
    nx.draw_networkx_labels(G, pos, font_size=13, font_weight='bold')

    # Mostrar el grafo de la cadena de Markov
    plt.title("Cadena de Markov")
    plt.show()

    # Calcular A^t para distribución futura
    A = np.array(transition_matrix)
    eigenvalues, eigenvectors = np.linalg.eig(A)
    D = eigenvectors
    D_inv = np.linalg.inv(D)
    M = np.diag(eigenvalues)
    A_t = np.dot(D, np.dot(np.linalg.matrix_power(M, t), D_inv))

    # Mostrar la matriz A^t en una nueva ventana
    show_matrix_result(A_t.real, t)

# Función para mostrar la matriz A^t en una nueva ventana
def show_matrix_result(matrix, t):
    result_window = Toplevel()
    result_window.title(f"Matriz A^{t}")

    Label(result_window, text=f"Matriz A^{t} calculada:").pack(padx=10, pady=5)

    matrix_text = "\n".join(["\t".join([f"{value:.4f}" for value in row]) for row in matrix])
    Label(result_window, text=matrix_text, justify="left").pack(padx=10, pady=5)

# Función para manejar la entrada de datos de la cadena de Markov
def input_markov_chain_data():
    input_window = Toplevel()
    input_window.title("Ingresar Datos de la Cadena de Markov")

    Label(input_window, text="Estados (separados por comas):").grid(row=0, column=0, padx=10, pady=5)
    states_entry = Entry(input_window)
    states_entry.grid(row=0, column=1, padx=10, pady=5)

    Label(input_window, text="Matriz de transición (filas separadas por punto y coma, valores por comas):").grid(row=1, column=0, padx=10, pady=5)
    matrix_entry = Entry(input_window)
    matrix_entry.grid(row=1, column=1, padx=10, pady=5)

    Label(input_window, text="Número de pasos t:").grid(row=2, column=0, padx=10, pady=5)
    t_entry = Entry(input_window)
    t_entry.grid(row=2, column=1, padx=10, pady=5)

    def on_submit():
        states = [state.strip() for state in states_entry.get().split(',')]
        matrix_str = matrix_entry.get().split(';')
        transition_matrix = [[float(value) for value in row.split(',')] for row in matrix_str]
        t = int(t_entry.get())
        input_window.destroy()

        # Dibujar la cadena de Markov y calcular A^t
        draw_markov_chain(transition_matrix, states, t)

    submit_button = Button(input_window, text="Generar Diagrama y Calcular A^t", command=on_submit)
    submit_button.grid(row=3, columnspan=2, pady=10)

# Punto de entrada principal
if __name__ == "__main__":
    root = Tk()
    root.withdraw()  # Ocultar la ventana principal

    input_markov_chain_data()
    root.mainloop()