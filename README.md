# Análisis de Estabilidad - Sistema Lineal

Este programa analiza el tipo y estabilidad del punto crítico (0,0) del sistema de ecuaciones diferenciales:

```
x' = a₁x + b₁y
y' = a₂x + b₂y
```

## Características

- **Análisis matemático completo**: Determina el tipo de punto crítico y su estabilidad según los teoremas de sistemas dinámicos
- **Visualización gráfica**: Muestra las trayectorias alrededor del punto crítico
- **Interfaz mejorada**: Diseño moderno y fácil de usar
- **Modularidad**: Código organizado en módulos separados
- **Implementación correcta**: Sigue estrictamente los teoremas matemáticos para clasificación

## Archivos del Proyecto

- `main.py`: Programa principal con la interfaz de usuario
- `analisis_estabilidad.py`: Módulo con la lógica de análisis matemático
- `visualizador_sistema.py`: Módulo para la visualización gráfica
- `app_pcritico_python.py`: Versión original (mantenida como referencia)

## Requisitos

- Python 3.7+
- numpy
- matplotlib
- tkinter (incluido con Python)

## Instalación

1. Instalar las dependencias:
```bash
pip install numpy matplotlib
```

## Uso

1. Ejecutar el programa:
```bash
python main.py
```

2. Ingresar los coeficientes del sistema (a₁, b₁, a₂, b₂)

3. Hacer clic en "Analizar Estabilidad"

4. El programa mostrará:
   - El tipo de punto crítico
   - Su estabilidad
   - Los valores propios
   - Una gráfica con las trayectorias

## Teoremas Implementados

El programa implementa correctamente los siguientes teoremas para clasificar puntos críticos:

### Clasificación por Tipo de Punto Crítico:

1. **Nodo**: Si M₁ y M₂ son valores propios reales diferentes del mismo signo
2. **Silla**: Si M₁ y M₂ son valores propios reales con signos opuestos
3. **Foco o Espiral**: Si M₁ y M₂ son valores propios complejos conjugados (no imaginarios puros)
4. **Centro**: Si M₁ y M₂ son valores propios imaginarios puros (parte real = 0)
5. **Nodo Especial**: Si M₁ = M₂ (valores propios iguales)

### Clasificación por Estabilidad:

- **Asintóticamente Estable**: Si todos los valores propios tienen parte real negativa
- **Estable**: Si todos los valores propios tienen parte real no positiva (≤ 0)
- **Inestable**: Si existe algún valor propio con parte real positiva

## Casos Especiales

Si el determinante es cero (o muy cercano a cero), el programa mostrará:
**"El punto crítico (0,0) no es único"**

Esto indica que hay infinitos puntos críticos o que el sistema es degenerado.

## Ejemplos de Uso

### Ejemplo 1: Nodo Estable
- Coeficientes: a₁=-2, b₁=0, a₂=0, b₂=-3
- Resultado: Nodo, Asintóticamente Estable
- Valores propios: -2.000, -3.000

### Ejemplo 2: Silla Inestable
- Coeficientes: a₁=2, b₁=0, a₂=0, b₂=-1
- Resultado: Silla, Inestable
- Valores propios: 2.000, -1.000

### Ejemplo 3: Foco Estable
- Coeficientes: a₁=-1, b₁=2, a₂=-2, b₂=-1
- Resultado: Foco o Espiral, Asintóticamente Estable
- Valores propios: -1.000±2.000i

### Ejemplo 4: Centro
- Coeficientes: a₁=0, b₁=1, a₂=-1, b₂=0
- Resultado: Centro, Estable
- Valores propios: ±1.000i

## Cambios Recientes

- ✅ **Corrección de la lógica**: Implementación correcta de los teoremas de clasificación
- ✅ **Mejora en la precisión**: Uso de valores propios en lugar de determinante/traza
- ✅ **Casos especiales**: Manejo correcto del Nodo Especial y valores propios complejos
- ✅ **Verificación**: Pruebas exhaustivas de todos los casos posibles
