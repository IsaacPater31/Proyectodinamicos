"""
Módulo para el análisis de estabilidad de sistemas lineales
Sistema: x' = a1*x + b1*y, y' = a2*x + b2*y
"""

import numpy as np


class AnalizadorEstabilidad:
    """Clase para analizar la estabilidad del punto crítico (0,0)"""
    
    def __init__(self, a1, b1, a2, b2):
        """
        Inicializa el analizador con los coeficientes del sistema
        
        Args:
            a1, b1, a2, b2: Coeficientes del sistema lineal
        """
        self.a1 = a1
        self.b1 = b1
        self.a2 = a2
        self.b2 = b2
        self.matriz = np.array([[a1, b1], [a2, b2]])
        
    def calcular_determinante(self):
        """Calcula el determinante de la matriz del sistema"""
        return np.linalg.det(self.matriz)
    
    def calcular_traza(self):
        """Calcula la traza de la matriz del sistema"""
        return np.trace(self.matriz)
    
    def calcular_valores_propios(self):
        """Calcula los valores propios de la matriz del sistema"""
        return np.linalg.eigvals(self.matriz)
    
    def es_punto_critico_unico(self):
        """
        Verifica si el punto crítico (0,0) es único
        
        Returns:
            bool: True si es único, False si no es único
        """
        det = self.calcular_determinante()
        return abs(det) >= 1e-10  # Usar tolerancia numérica
    
    def analizar_tipo_y_estabilidad(self):
        """
        Analiza el tipo y estabilidad del punto crítico
        
        Returns:
            str: Descripción del tipo de punto crítico y su estabilidad
        """
        # Verificar si el punto crítico es único
        if not self.es_punto_critico_unico():
            return "El punto crítico (0,0) no es único"
        
        det = self.calcular_determinante()
        traza = self.calcular_traza()
        valores_propios = self.calcular_valores_propios()
        
        # Determinar tipo de punto crítico y estabilidad
        if det > 0:
            if traza < 0:
                return f"Nodo estable (atractor)\nValores propios: {valores_propios[0]:.2f}, {valores_propios[1]:.2f}"
            elif traza > 0:
                return f"Nodo inestable (repulsor)\nValores propios: {valores_propios[0]:.2f}, {valores_propios[1]:.2f}"
            else:
                return f"Centro\nValores propios: {valores_propios[0]:.2f}, {valores_propios[1]:.2f}"
        
        elif det < 0:
            return f"Punto silla (inestable)\nValores propios: {valores_propios[0]:.2f}, {valores_propios[1]:.2f}"
        
        else:
            if abs(traza) > 1e-10:
                return f"Nodo impropio\nValores propios: {valores_propios[0]:.2f}, {valores_propios[1]:.2f}"
            else:
                return f"Caso degenerado\nValores propios: {valores_propios[0]:.2f}, {valores_propios[1]:.2f}"
    
    def obtener_informacion_completa(self):
        """
        Obtiene toda la información del análisis
        
        Returns:
            dict: Diccionario con toda la información del análisis
        """
        return {
            'coeficientes': {'a1': self.a1, 'b1': self.b1, 'a2': self.a2, 'b2': self.b2},
            'matriz': self.matriz,
            'determinante': self.calcular_determinante(),
            'traza': self.calcular_traza(),
            'valores_propios': self.calcular_valores_propios(),
            'es_unico': self.es_punto_critico_unico(),
            'tipo_estabilidad': self.analizar_tipo_y_estabilidad()
        }
