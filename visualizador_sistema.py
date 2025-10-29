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
    
    def calcular_trayectoria(self, x0, y0, a1, b1, a2, b2, t_max=3, puntos=200):
        """
        Calcula una trayectoria específica del sistema usando integración numérica
        
        Args:
            x0, y0: Condiciones iniciales
            a1, b1, a2, b2: Coeficientes del sistema
            t_max: Tiempo máximo de integración
            puntos: Número de puntos en la trayectoria
            
        Returns:
            tuple: (x_trayectoria, y_trayectoria)
        """
        from scipy.integrate import solve_ivp
        
        def sistema_dinamico(t, y):
            return [a1 * y[0] + b1 * y[1], a2 * y[0] + b2 * y[1]]
        
        # Integrar hacia adelante y hacia atrás
        t_span = (0, t_max)
        t_eval = np.linspace(0, t_max, puntos)
        
        try:
            sol = solve_ivp(sistema_dinamico, t_span, [x0, y0], t_eval=t_eval, 
                          rtol=1e-8, atol=1e-10)
            if sol.success:
                return sol.y[0], sol.y[1]
        except:
            pass
        
        # Fallback: usar método de Euler mejorado
        dt = t_max / puntos
        x_traj = [x0]
        y_traj = [y0]
        
        for i in range(puntos - 1):
            x_curr, y_curr = x_traj[-1], y_traj[-1]
            dx = a1 * x_curr + b1 * y_curr
            dy = a2 * x_curr + b2 * y_curr
            
            x_next = x_curr + dt * dx
            y_next = y_curr + dt * dy
            
            x_traj.append(x_next)
            y_traj.append(y_next)
        
        return np.array(x_traj), np.array(y_traj)
    
    def crear_grafica_completa(self, a1, b1, a2, b2, titulo="Trayectorias del Sistema", parent_frame=None):
        """
        Crea una gráfica completa con campo vectorial y trayectorias
        
        Args:
            a1, b1, a2, b2: Coeficientes del sistema
            titulo: Título de la gráfica
            parent_frame: Frame padre para calcular tamaño dinámico
            
        Returns:
            matplotlib.figure.Figure: Figura con la gráfica
        """
        # Calcular tamaño dinámico si se proporciona el frame padre
        if parent_frame:
            try:
                # Obtener dimensiones del frame padre
                parent_frame.update_idletasks()
                width = parent_frame.winfo_width()
                height = parent_frame.winfo_height()
                
                # Convertir píxeles a pulgadas (DPI típico: 100)
                dpi = 100
                fig_width = max(width / dpi, 6)  # Mínimo 6 pulgadas
                fig_height = max(height / dpi, 4)  # Mínimo 4 pulgadas
                
                fig = plt.Figure(figsize=(fig_width, fig_height), dpi=dpi)
            except:
                fig = plt.Figure(figsize=self.figura_tamano)
        else:
            fig = plt.Figure(figsize=self.figura_tamano)
            
        ax = fig.add_subplot(111)
        
        # Determinar el rango dinámico basado en los valores propios
        valores_propios = np.linalg.eigvals([[a1, b1], [a2, b2]])
        max_real = max(np.abs(np.real(valores_propios)))
        
        # Verificar si es una silla (valores propios reales con signos opuestos)
        es_silla = False
        if np.isreal(valores_propios[0]) and np.isreal(valores_propios[1]):
            if np.sign(np.real(valores_propios[0])) != np.sign(np.real(valores_propios[1])):
                es_silla = True
        
        # Ajustar rango según el comportamiento del sistema
        if es_silla:
            # Para sillas, usar rango más amplio para mostrar mejor el comportamiento divergente
            rango = 4.0
        elif max_real > 2:
            rango = 1.5
        elif max_real > 1:
            rango = 2.0
        else:
            rango = 3.0
        
        # Crear campo vectorial con mayor densidad
        X, Y, U, V = self.calcular_campo_vectorial((-rango, rango), (-rango, rango), 
                                                  a1, b1, a2, b2, densidad=25)
        
        # Calcular magnitud para colorear las flechas
        magnitud = np.sqrt(U**2 + V**2)
        
        # Graficar campo vectorial con mejor visualización
        ax.quiver(X, Y, U, V, magnitud, cmap='plasma', alpha=0.8, scale=30, 
                 scale_units='xy', width=0.003)
        
        # Seleccionar puntos iniciales estratégicos según el tipo de sistema
        if es_silla:
            # Para sillas, usar más puntos iniciales distribuidos en el rango amplio
            puntos_iniciales = [-rango*0.9, -rango*0.6, -rango*0.3, rango*0.3, rango*0.6, rango*0.9]
        elif max_real > 1:  # Sistema rápido
            puntos_iniciales = [-rango*0.8, -rango*0.4, rango*0.4, rango*0.8]
        else:  # Sistema lento
            puntos_iniciales = [-rango*0.9, -rango*0.6, -rango*0.3, rango*0.3, rango*0.6, rango*0.9]
        
        colores = ['red', 'blue', 'green', 'orange', 'purple', 'brown']
        
        # Graficar trayectorias con diferentes colores y grosores
        for i, x0 in enumerate(puntos_iniciales):
            for j, y0 in enumerate(puntos_iniciales):
                if abs(x0) > 0.1 or abs(y0) > 0.1:  # Evitar el punto crítico
                    try:
                        # Para sillas, usar tiempo de integración más largo para mostrar mejor la divergencia
                        t_max = 4.0 if es_silla else 3.0
                        x_traj, y_traj = self.calcular_trayectoria(x0, y0, a1, b1, a2, b2, t_max=t_max)
                        
                        # Filtrar trayectorias que se salen del rango
                        mask = (np.abs(x_traj) < rango*1.2) & (np.abs(y_traj) < rango*1.2)
                        x_traj = x_traj[mask]
                        y_traj = y_traj[mask]
                        
                        if len(x_traj) > 10:  # Solo mostrar trayectorias significativas
                            color_idx = (i + j) % len(colores)
                            # Para sillas, usar líneas más gruesas para mejor visibilidad
                            linewidth = 1.5 if es_silla else 1.2
                            ax.plot(x_traj, y_traj, color=colores[color_idx], 
                                   linewidth=linewidth, alpha=0.8)
                            
                            # Marcar punto inicial
                            ax.plot(x0, y0, 'o', color=colores[color_idx], 
                                   markersize=4, alpha=0.7)
                    except:
                        continue
        
        # Marcar el punto crítico con mejor visibilidad
        ax.plot([0], [0], 'ko', markersize=15, 
                markeredgecolor='white', markeredgewidth=3, zorder=10)
        
        # Configurar gráfica con mejor estilo
        ax.set_xlabel('x', fontsize=12, fontweight='bold')
        ax.set_ylabel('y', fontsize=12, fontweight='bold')
        ax.set_title(titulo, fontsize=14, fontweight='bold', pad=20)
        ax.grid(True, alpha=0.4, linestyle='--')
        ax.set_aspect('equal')
        
        # Agregar leyenda del punto crítico en la esquina superior derecha
        ax.text(0.98, 0.98, 'Punto crítico (0,0)', transform=ax.transAxes, 
                fontsize=10, fontweight='bold', ha='right', va='top',
                bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.8, edgecolor='black'))
        
        # Establecer límites de los ejes
        ax.set_xlim(-rango, rango)
        ax.set_ylim(-rango, rango)
        
        # Agregar líneas de referencia
        ax.axhline(y=0, color='black', linestyle='-', alpha=0.3, linewidth=0.5)
        ax.axvline(x=0, color='black', linestyle='-', alpha=0.3, linewidth=0.5)
        
        return fig
    
    def crear_canvas_tkinter(self, parent_frame, figura):
        """
        Crea un canvas de Tkinter para mostrar la figura estática
        
        Args:
            parent_frame: Frame padre donde se colocará el canvas
            figura: Figura de matplotlib a mostrar
            
        Returns:
            FigureCanvasTkAgg: Canvas de Tkinter
        """
        # Limpiar frame anterior
        for widget in parent_frame.winfo_children():
            widget.destroy()
        
        # Crear nuevo canvas estático
        canvas = FigureCanvasTkAgg(figura, parent_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Hacer que el canvas sea completamente responsivo
        canvas.get_tk_widget().configure(width=1, height=1)  # Forzar expansión
        
        return canvas
