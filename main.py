"""
Programa principal para el análisis de estabilidad de sistemas lineales
Sistema: x' = a1*x + b1*y, y' = a2*x + b2*y

Módulos:
- analisis_estabilidad.py: Lógica de análisis matemático
- visualizador_sistema.py: Visualización gráfica
"""

import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt

from analisis_estabilidad import AnalizadorEstabilidad
from visualizador_sistema import VisualizadorSistema


class InterfazAnalisisEstabilidad:
    """Clase principal para la interfaz de usuario"""
    
    def __init__(self):
        """Inicializa la interfaz principal"""
        self.ventana = tk.Tk()
        self.visualizador = VisualizadorSistema()
        self.configurar_ventana()
        self.crear_widgets()
        
    def configurar_ventana(self):
        """Configura la ventana principal"""
        self.ventana.title("Análisis de Estabilidad - Sistema Lineal")
        self.ventana.geometry("1000x700")
        self.ventana.configure(bg='#f0f0f0')
        
        # Configurar estilo
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configurar expansión de la ventana
        self.ventana.columnconfigure(0, weight=1)
        self.ventana.rowconfigure(0, weight=1)
        
    def crear_widgets(self):
        """Crea todos los widgets de la interfaz"""
        # Frame principal
        self.frame_principal = ttk.Frame(self.ventana, padding="20")
        self.frame_principal.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.frame_principal.configure(relief='raised', borderwidth=1)
        
        # Configurar expansión del frame principal
        self.frame_principal.columnconfigure(1, weight=1)
        self.frame_principal.rowconfigure(0, weight=1)
        
        # Frame izquierdo - Panel de entrada
        self.crear_panel_entrada()
        
        # Frame derecho - Panel de visualización
        self.crear_panel_visualizacion()
        
    def crear_panel_entrada(self):
        """Crea el panel de entrada de datos"""
        self.frame_entrada = ttk.LabelFrame(self.frame_principal, text="Parámetros del Sistema", 
                                          padding="15")
        self.frame_entrada.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), 
                               padx=(0, 15))
        
        # Título del sistema
        titulo_sistema = ttk.Label(self.frame_entrada, 
                                 text="Sistema de Ecuaciones Diferenciales",
                                 font=('Arial', 12, 'bold'))
        titulo_sistema.grid(row=0, column=0, columnspan=2, pady=(0, 10))
        
        # Ecuaciones del sistema
        ecuaciones = ttk.Label(self.frame_entrada,
                              text="x' = a₁x + b₁y\ny' = a₂x + b₂y",
                              font=('Courier', 11),
                              foreground='#2c3e50')
        ecuaciones.grid(row=1, column=0, columnspan=2, pady=(0, 20))
        
        # Entradas para coeficientes
        self.crear_entradas_coeficientes()
        
        # Botones de control
        self.crear_botones_control()
        
        # Panel de resultados
        self.crear_panel_resultados()
        
    def crear_entradas_coeficientes(self):
        """Crea las entradas para los coeficientes"""
        # Configurar estilo para las entradas
        style = ttk.Style()
        style.configure('Entrada.TEntry', fieldbackground='white', borderwidth=2)
        
        # Coeficiente a1
        ttk.Label(self.frame_entrada, text="a₁:", font=('Arial', 10, 'bold')).grid(
            row=2, column=0, sticky=tk.W, pady=5)
        self.entry_a1 = ttk.Entry(self.frame_entrada, width=15, style='Entrada.TEntry')
        self.entry_a1.grid(row=2, column=1, pady=5, padx=(10, 0))
        self.entry_a1.insert(0, "1")  # Valor por defecto
        
        # Coeficiente b1
        ttk.Label(self.frame_entrada, text="b₁:", font=('Arial', 10, 'bold')).grid(
            row=3, column=0, sticky=tk.W, pady=5)
        self.entry_b1 = ttk.Entry(self.frame_entrada, width=15, style='Entrada.TEntry')
        self.entry_b1.grid(row=3, column=1, pady=5, padx=(10, 0))
        self.entry_b1.insert(0, "0")  # Valor por defecto
        
        # Coeficiente a2
        ttk.Label(self.frame_entrada, text="a₂:", font=('Arial', 10, 'bold')).grid(
            row=4, column=0, sticky=tk.W, pady=5)
        self.entry_a2 = ttk.Entry(self.frame_entrada, width=15, style='Entrada.TEntry')
        self.entry_a2.grid(row=4, column=1, pady=5, padx=(10, 0))
        self.entry_a2.insert(0, "0")  # Valor por defecto
        
        # Coeficiente b2
        ttk.Label(self.frame_entrada, text="b₂:", font=('Arial', 10, 'bold')).grid(
            row=5, column=0, sticky=tk.W, pady=5)
        self.entry_b2 = ttk.Entry(self.frame_entrada, width=15, style='Entrada.TEntry')
        self.entry_b2.grid(row=5, column=1, pady=5, padx=(10, 0))
        self.entry_b2.insert(0, "-1")  # Valor por defecto
        
    def crear_botones_control(self):
        """Crea los botones de control"""
        # Frame para botones
        frame_botones = ttk.Frame(self.frame_entrada)
        frame_botones.grid(row=6, column=0, columnspan=2, pady=20)
        
        # Botón analizar
        self.btn_analizar = ttk.Button(frame_botones, text="🔍 Analizar Estabilidad",
                                     command=self.analizar_sistema,
                                     style='Accent.TButton')
        self.btn_analizar.pack(side=tk.LEFT, padx=5)
        
        # Botón limpiar
        self.btn_limpiar = ttk.Button(frame_botones, text="🗑️ Limpiar",
                                    command=self.limpiar_campos)
        self.btn_limpiar.pack(side=tk.LEFT, padx=5)
        
    def crear_panel_resultados(self):
        """Crea el panel de resultados"""
        self.frame_resultados = ttk.LabelFrame(self.frame_entrada, text="Resultado del Análisis",
                                             padding="10")
        self.frame_resultados.grid(row=7, column=0, columnspan=2, sticky=(tk.W, tk.E), 
                                 pady=(10, 0))
        
        # Área de texto para resultados
        self.texto_resultados = tk.Text(self.frame_resultados, height=6, width=30,
                                       font=('Arial', 9), wrap=tk.WORD,
                                       bg='#f8f9fa', relief='sunken', borderwidth=1)
        self.texto_resultados.pack(fill=tk.BOTH, expand=True)
        
        # Scrollbar para el texto
        scrollbar = ttk.Scrollbar(self.frame_resultados, orient=tk.VERTICAL,
                                command=self.texto_resultados.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.texto_resultados.configure(yscrollcommand=scrollbar.set)
        
    def crear_panel_visualizacion(self):
        """Crea el panel de visualización"""
        self.frame_visualizacion = ttk.LabelFrame(self.frame_principal, text="Visualización Gráfica",
                                                padding="10")
        self.frame_visualizacion.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Frame para la gráfica
        self.frame_grafica = ttk.Frame(self.frame_visualizacion)
        self.frame_grafica.pack(fill=tk.BOTH, expand=True)
        
    def obtener_coeficientes(self):
        """Obtiene los coeficientes de las entradas"""
        try:
            a1 = float(self.entry_a1.get())
            b1 = float(self.entry_b1.get())
            a2 = float(self.entry_a2.get())
            b2 = float(self.entry_b2.get())
            return a1, b1, a2, b2
        except ValueError:
            raise ValueError("Por favor ingrese valores numéricos válidos en todos los campos")
    
    def mostrar_resultado(self, resultado):
        """Muestra el resultado en el panel de resultados"""
        self.texto_resultados.delete(1.0, tk.END)
        self.texto_resultados.insert(tk.END, resultado)
        
    def analizar_sistema(self):
        """Analiza el sistema y muestra los resultados"""
        try:
            # Obtener coeficientes
            a1, b1, a2, b2 = self.obtener_coeficientes()
            
            # Crear analizador
            analizador = AnalizadorEstabilidad(a1, b1, a2, b2)
            
            # Realizar análisis
            resultado = analizador.analizar_tipo_y_estabilidad()
            
            # Mostrar resultado
            self.mostrar_resultado(resultado)
            
            # Crear y mostrar gráfica
            figura = self.visualizador.crear_grafica_completa(a1, b1, a2, b2)
            self.visualizador.crear_canvas_tkinter(self.frame_grafica, figura)
            
        except ValueError as e:
            messagebox.showerror("Error de Entrada", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"Ha ocurrido un error inesperado: {str(e)}")
    
    def limpiar_campos(self):
        """Limpia todos los campos de entrada"""
        self.entry_a1.delete(0, tk.END)
        self.entry_b1.delete(0, tk.END)
        self.entry_a2.delete(0, tk.END)
        self.entry_b2.delete(0, tk.END)
        self.texto_resultados.delete(1.0, tk.END)
        
        # Limpiar gráfica
        for widget in self.frame_grafica.winfo_children():
            widget.destroy()
    
    def ejecutar(self):
        """Ejecuta la aplicación"""
        self.ventana.mainloop()


def main():
    """Función principal"""
    app = InterfazAnalisisEstabilidad()
    app.ejecutar()


if __name__ == "__main__":
    main()
