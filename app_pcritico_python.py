import numpy as np
import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.gridspec as gridspec

def sistema_dinamico(X, Y, a1, b1, a2, b2):
    """Calcula el campo vectorial del sistema"""
    U = a1*X + b1*Y
    V = a2*X + b2*Y
    return U, V

def graficar_trayectorias(a1, b1, a2, b2):
    """Crea la gráfica de las trayectorias"""
    fig = plt.Figure(figsize=(6, 6))
    ax = fig.add_subplot(111)
    
    # Crear grilla para el campo vectorial
    x = np.linspace(-2, 2, 20)
    y = np.linspace(-2, 2, 20)
    X, Y = np.meshgrid(x, y)
    
    # Calcular campo vectorial
    U, V = sistema_dinamico(X, Y, a1, b1, a2, b2)
    
    # Normalizar vectores para mejor visualización
    norm = np.sqrt(U**2 + V**2)
    U = U / norm
    V = V / norm
    
    # Graficar campo vectorial
    ax.quiver(X, Y, U, V, norm, cmap='viridis', alpha=0.7)
    
    # Graficar algunas trayectorias
    for x0 in [-1.5, -1.0, -0.5, 0.5, 1.0, 1.5]:
        for y0 in [-1.5, -1.0, -0.5, 0.5, 1.0, 1.5]:
            t = np.linspace(0, 2, 100)
            X0 = np.array([x0, y0])
            A = np.array([[a1, b1], [a2, b2]])
            trayectoria = np.zeros((len(t), 2))
            
            for i in range(len(t)):
                trayectoria[i] = np.exp(A * t[i]) @ X0
            
            ax.plot(trayectoria[:,0], trayectoria[:,1], 'r-', linewidth=0.5, alpha=0.5)
    
    # Marcar el punto crítico
    ax.plot([0], [0], 'ko', markersize=10, label='Punto crítico (0,0)')
    
    # Configurar gráfica
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_title('Trayectorias del Sistema')
    ax.grid(True)
    ax.set_aspect('equal')
    ax.legend()
    
    return fig

def analizar_estabilidad(a1, b1, a2, b2):
    # Crear matriz del sistema
    A = np.array([[a1, b1],
                  [a2, b2]])
    
    # Calcular determinante y traza
    det = np.linalg.det(A)
    traza = np.trace(A)
    
    # Calcular valores propios
    valores_propios = np.linalg.eigvals(A)
    
    # Verificar si el punto crítico es único
    if abs(det) < 1e-10:  # Usar tolerancia numérica
        return "El punto crítico (0,0) no es único"
    
    # Determinar tipo de punto crítico y estabilidad
    if det > 0:
        if traza < 0:
            return "Nodo estable (atractor)\nValores propios: {:.2f}, {:.2f}".format(
                valores_propios[0], valores_propios[1])
        elif traza > 0:
            return "Nodo inestable (repulsor)\nValores propios: {:.2f}, {:.2f}".format(
                valores_propios[0], valores_propios[1])
        else:
            return "Centro\nValores propios: {:.2f}, {:.2f}".format(
                valores_propios[0], valores_propios[1])
    
    elif det < 0:
        return "Punto silla (inestable)\nValores propios: {:.2f}, {:.2f}".format(
            valores_propios[0], valores_propios[1])
    
    else:
        if abs(traza) > 1e-10:
            return "Nodo impropio\nValores propios: {:.2f}, {:.2f}".format(
                valores_propios[0], valores_propios[1])
        else:
            return "Caso degenerado\nValores propios: {:.2f}, {:.2f}".format(
                valores_propios[0], valores_propios[1])

def calcular():
    try:
        # Obtener valores de los coeficientes
        a1 = float(entry_a1.get())
        b1 = float(entry_b1.get())
        a2 = float(entry_a2.get())
        b2 = float(entry_b2.get())
        
        # Analizar estabilidad
        resultado = analizar_estabilidad(a1, b1, a2, b2)
        
        # Mostrar resultado
        messagebox.showinfo("Resultado del Análisis", resultado)
        
        # Crear y mostrar gráfica
        fig = graficar_trayectorias(a1, b1, a2, b2)
        
        # Si ya existe un canvas, destruirlo
        for widget in frame_grafica.winfo_children():
            widget.destroy()
        
        # Crear nuevo canvas con la gráfica
        canvas = FigureCanvasTkAgg(fig, frame_grafica)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
    except ValueError:
        messagebox.showerror("Error", "Por favor ingrese valores numéricos válidos")
    except Exception as e:
        messagebox.showerror("Error", f"Ha ocurrido un error: {str(e)}")

# Crear ventana principal
ventana = tk.Tk()
ventana.title("Análisis de Estabilidad - Sistema Lineal")
ventana.geometry("800x800")

# Frame principal con dos columnas
frame_principal = ttk.Frame(ventana, padding="20")
frame_principal.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

# Frame izquierdo para entradas
frame_entradas = ttk.Frame(frame_principal)
frame_entradas.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0,20))

# Título
titulo = ttk.Label(frame_entradas, text="Sistema de ecuaciones:\nx' = a₁x + b₁y\ny' = a₂x + b₂y", 
                   font=('Arial', 12))
titulo.grid(row=0, column=0, columnspan=2, pady=(0,20))

# Entradas para coeficientes
ttk.Label(frame_entradas, text="a₁:").grid(row=1, column=0)
entry_a1 = ttk.Entry(frame_entradas, width=15)
entry_a1.grid(row=1, column=1, pady=5)

ttk.Label(frame_entradas, text="b₁:").grid(row=2, column=0)
entry_b1 = ttk.Entry(frame_entradas, width=15)
entry_b1.grid(row=2, column=1, pady=5)

ttk.Label(frame_entradas, text="a₂:").grid(row=3, column=0)
entry_a2 = ttk.Entry(frame_entradas, width=15)
entry_a2.grid(row=3, column=1, pady=5)

ttk.Label(frame_entradas, text="b₂:").grid(row=4, column=0)
entry_b2 = ttk.Entry(frame_entradas, width=15)
entry_b2.grid(row=4, column=1, pady=5)

# Botón calcular
ttk.Button(frame_entradas, text="Analizar Estabilidad", command=calcular).grid(row=5, column=0, columnspan=2, pady=20)

# Frame derecho para la gráfica
frame_grafica = ttk.Frame(frame_principal)
frame_grafica.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))

# Configurar expansión
ventana.columnconfigure(0, weight=1)
ventana.rowconfigure(0, weight=1)
frame_principal.columnconfigure(1, weight=1)
frame_principal.rowconfigure(0, weight=1)

ventana.mainloop()