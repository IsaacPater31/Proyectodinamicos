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
        Analiza el tipo y estabilidad del punto crítico según los teoremas dados
        
        Returns:
            str: Descripción del tipo de punto crítico y su estabilidad
        """
        # Verificar si el punto crítico es único
        if not self.es_punto_critico_unico():
            return "El punto crítico (0,0) no es único"
        
        valores_propios = self.calcular_valores_propios()
        m1, m2 = valores_propios[0], valores_propios[1]
        
        # Determinar tipo de punto crítico según los teoremas dados
        tipo_punto = self._determinar_tipo_punto_critico(m1, m2)
        estabilidad = self._determinar_estabilidad(m1, m2)
        
        resultado = f"{tipo_punto}\n{estabilidad}\nValores propios: {m1:.3f}, {m2:.3f}"
        return resultado
    
    def _determinar_tipo_punto_critico(self, m1, m2):
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
    
    def _determinar_estabilidad(self, m1, m2):
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
