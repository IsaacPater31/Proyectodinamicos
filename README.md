# Análisis de Estabilidad - Sistema Lineal

Este programa analiza el tipo y estabilidad del punto crítico (0,0) del sistema de ecuaciones diferenciales:

```
x' = a₁x + b₁y
y' = a₂x + b₂y
```

## Características

- **Análisis matemático completo**: Determina el tipo de punto crítico y su estabilidad
- **Visualización gráfica**: Muestra las trayectorias alrededor del punto crítico
- **Interfaz mejorada**: Diseño moderno y fácil de usar
- **Modularidad**: Código organizado en módulos separados

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

## Tipos de Puntos Críticos

El programa puede identificar:

- **Nodo estable (atractor)**: det > 0, traza < 0
- **Nodo inestable (repulsor)**: det > 0, traza > 0
- **Centro**: det > 0, traza = 0
- **Punto silla (inestable)**: det < 0
- **Nodo impropio**: det = 0, traza ≠ 0
- **Caso degenerado**: det = 0, traza = 0

## Casos Especiales

Si el determinante es cero (o muy cercano a cero), el programa mostrará:
"El punto crítico (0,0) no es único"

Esto indica que hay infinitos puntos críticos o que el sistema es degenerado.
