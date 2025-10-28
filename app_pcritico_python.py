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
    m1, m2 = valores_propios[0], valores_propios[1]
    
    # Verificar si el punto crítico es único
    if abs(det) < 1e-10:  # Usar tolerancia numérica
        return "El punto crítico (0,0) no es único"
    
    # Determinar tipo de punto crítico según los teoremas dados
    tipo_punto = determinar_tipo_punto_critico(m1, m2)
    estabilidad = determinar_estabilidad(m1, m2)
    
    resultado = f"{tipo_punto}\n{estabilidad}\nValores propios: {m1:.3f}, {m2:.3f}"
    return resultado

def determinar_tipo_punto_critico(m1, m2):
    """
    Determina el tipo de punto crítico según los teoremas dados
    
    Args:
        m1, m2: Valores propios del sistema
        
    Returns:
        str: Tipo de punto crítico
    """
    # Verificar si son valores propios reales
    if np.isreal(m1) and np.isreal(m2):
        # Caso 1: M1 y M2 son reales diferentes
        if abs(m1 - m2) > 1e-10:
            if np.sign(m1) == np.sign(m2):
                return "Nodo"
            else:
                return "Silla"
        # Caso 5: M1 = M2 (Nodo Especial)
        else:
            return "Nodo Especial"
    
    # Verificar si son valores propios complejos
    elif not np.isreal(m1) and not np.isreal(m2):
        # Verificar si son conjugados complejos
        if abs(m1 - np.conj(m2)) < 1e-10:
            # Verificar si son imaginarios puros (parte real = 0)
            if abs(np.real(m1)) < 1e-10 and abs(np.real(m2)) < 1e-10:
                return "Centro"
            else:
                return "Foco o Espiral"
        else:
            return "Caso especial complejo"
    
    # Caso mixto (no debería ocurrir en sistemas lineales 2x2)
    else:
        return "Caso degenerado"

def determinar_estabilidad(m1, m2):
    """
    Determina la estabilidad según los teoremas dados
    
    Args:
        m1, m2: Valores propios del sistema
        
    Returns:
        str: Tipo de estabilidad
    """
    # Obtener partes reales
    parte_real_m1 = np.real(m1)
    parte_real_m2 = np.real(m2)
    
    # Teorema de estabilidad:
    # - Estable si todos los autovalores tienen parte real no positiva
    # - Asintóticamente estable si todos tienen parte real negativa
    # - Inestable si existe algún autovalor con parte real positiva
    
    if parte_real_m1 < 0 and parte_real_m2 < 0:
        return "Asintóticamente Estable"
    elif parte_real_m1 <= 0 and parte_real_m2 <= 0:
        return "Estable"
    else:
        return "Inestable"

def formatear_resultado(resultado):
    """Formatea el resultado con estructura clara"""
    lineas = resultado.split('\n')
    if len(lineas) >= 3:
        tipo = lineas[0]
        estabilidad = lineas[1]
        valores_propios = lineas[2]
        
        texto_formateado = f"Tipo: {tipo}\n"
        texto_formateado += f"Estabilidad: {estabilidad}\n"
        texto_formateado += f"Valores propios: {valores_propios}"
        return texto_formateado
    else:
        return resultado

def calcular():
    try:
        # Obtener valores de los coeficientes
        a1 = float(entry_a1.get())
        b1 = float(entry_b1.get())
        a2 = float(entry_a2.get())
        b2 = float(entry_b2.get())
        
        # Analizar estabilidad
        resultado = analizar_estabilidad(a1, b1, a2, b2)
        
        # Formatear y mostrar resultado
        resultado_formateado = formatear_resultado(resultado)
        messagebox.showinfo("Resultado del Análisis", resultado_formateado)
        
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