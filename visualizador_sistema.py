"""
Módulo para la visualización gráfica de sistemas dinámicos
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk


class VisualizadorSistema:
    """Clase para crear visualizaciones del sistema dinámico"""
    
    def __init__(self, figura_tamano=(8, 6)):
        """
        Inicializa el visualizador
        
        Args:
            figura_tamano: Tupla con el tamaño de la figura (ancho, alto)
        """
        self.figura_tamano = figura_tamano
        
    def calcular_campo_vectorial(self, x_range, y_range, a1, b1, a2, b2, densidad=20):
        """
        Calcula el campo vectorial del sistema
        
        Args:
            x_range: Tupla (x_min, x_max) para el rango de x
            y_range: Tupla (y_min, y_max) para el rango de y
            a1, b1, a2, b2: Coeficientes del sistema
            densidad: Número de puntos en cada dirección
            
        Returns:
            tuple: (X, Y, U, V) donde U,V son las componentes del campo
        """
        x = np.linspace(x_range[0], x_range[1], densidad)
        y = np.linspace(y_range[0], y_range[1], densidad)
        X, Y = np.meshgrid(x, y)
        
        # Calcular campo vectorial
        U = a1 * X + b1 * Y
        V = a2 * X + b2 * Y
        
        return X, Y, U, V
    
    def calcular_trayectoria(self, x0, y0, a1, b1, a2, b2, t_max=2, puntos=100):
        """
        Calcula una trayectoria específica del sistema
        
        Args:
            x0, y0: Condiciones iniciales
            a1, b1, a2, b2: Coeficientes del sistema
            t_max: Tiempo máximo de integración
            puntos: Número de puntos en la trayectoria
            
        Returns:
            tuple: (x_trayectoria, y_trayectoria)
        """
        t = np.linspace(0, t_max, puntos)
        X0 = np.array([x0, y0])
        A = np.array([[a1, b1], [a2, b2]])
        
        trayectoria = np.zeros((len(t), 2))
        
        for i in range(len(t)):
            trayectoria[i] = np.exp(A * t[i]) @ X0
        
        return trayectoria[:, 0], trayectoria[:, 1]
    
    def crear_grafica_completa(self, a1, b1, a2, b2, titulo="Trayectorias del Sistema"):
        """
        Crea una gráfica completa con campo vectorial y trayectorias
        
        Args:
            a1, b1, a2, b2: Coeficientes del sistema
            titulo: Título de la gráfica
            
        Returns:
            matplotlib.figure.Figure: Figura con la gráfica
        """
        fig = plt.Figure(figsize=self.figura_tamano)
        ax = fig.add_subplot(111)
        
        # Crear campo vectorial
        X, Y, U, V = self.calcular_campo_vectorial((-2, 2), (-2, 2), a1, b1, a2, b2)
        
        # Normalizar vectores para mejor visualización
        norm = np.sqrt(U**2 + V**2)
        U_norm = np.divide(U, norm, out=np.zeros_like(U), where=norm!=0)
        V_norm = np.divide(V, norm, out=np.zeros_like(V), where=norm!=0)
        
        # Graficar campo vectorial
        ax.quiver(X, Y, U_norm, V_norm, norm, cmap='viridis', alpha=0.7, scale=20)
        
        # Graficar trayectorias desde diferentes puntos iniciales
        puntos_iniciales = [-1.5, -1.0, -0.5, 0.5, 1.0, 1.5]
        
        for x0 in puntos_iniciales:
            for y0 in puntos_iniciales:
                if abs(x0) > 0.1 or abs(y0) > 0.1:  # Evitar el punto crítico
                    x_traj, y_traj = self.calcular_trayectoria(x0, y0, a1, b1, a2, b2)
                    ax.plot(x_traj, y_traj, 'r-', linewidth=0.8, alpha=0.6)
        
        # Marcar el punto crítico
        ax.plot([0], [0], 'ko', markersize=12, label='Punto crítico (0,0)', 
                markeredgecolor='white', markeredgewidth=2)
        
        # Configurar gráfica
        ax.set_xlabel('x', fontsize=12)
        ax.set_ylabel('y', fontsize=12)
        ax.set_title(titulo, fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3)
        ax.set_aspect('equal')
        ax.legend(loc='upper right')
        
        # Establecer límites de los ejes
        ax.set_xlim(-2, 2)
        ax.set_ylim(-2, 2)
        
        return fig
    
    def crear_canvas_tkinter(self, parent_frame, figura):
        """
        Crea un canvas de Tkinter para mostrar la figura
        
        Args:
            parent_frame: Frame padre donde se colocará el canvas
            figura: Figura de matplotlib a mostrar
            
        Returns:
            FigureCanvasTkAgg: Canvas de Tkinter
        """
        # Limpiar frame anterior
        for widget in parent_frame.winfo_children():
            widget.destroy()
        
        # Crear nuevo canvas
        canvas = FigureCanvasTkAgg(figura, parent_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        return canvas
