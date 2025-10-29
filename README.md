# Análisis de Estabilidad - Sistema Lineal

Este programa analiza el tipo y estabilidad del punto crítico (0,0) del sistema de ecuaciones diferenciales:

```
x' = a₁x + b₁y
y' = a₂x + b₂y
```

## Características

- **Análisis matemático completo**: Determina el tipo de punto crítico y su estabilidad según los teoremas de sistemas dinámicos
- **Visualización gráfica responsiva**: Muestra las trayectorias alrededor del punto crítico con tamaño adaptativo
- **Interfaz moderna**: Diseño profesional con campos vacíos y resultados estructurados
- **Modularidad**: Código organizado en módulos separados con responsabilidades claras
- **Implementación correcta**: Sigue estrictamente los teoremas matemáticos para clasificación
- **Integración numérica robusta**: Usa scipy para trayectorias precisas con fallback automático

## Archivos del Proyecto

- `main.py`: Programa principal con la interfaz de usuario
- `analisis_estabilidad.py`: Módulo con la lógica de análisis matemático
- `visualizador_sistema.py`: Módulo para la visualización gráfica

## Requisitos

- Python 3.7+
- numpy
- matplotlib
- scipy (opcional, mejora precisión de trayectorias)
- tkinter (incluido con Python)

## Instalación

1. Instalar las dependencias:
```bash
pip install numpy matplotlib scipy
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
   - Una gráfica responsiva con trayectorias adaptativas

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

## Arquitectura del Programa

Este programa fue desarrollado desde cero con una arquitectura modular que separa claramente las responsabilidades:

### **Módulos Principales:**

1. **`main.py`**: Interfaz de usuario y controlador principal
2. **`analisis_estabilidad.py`**: Lógica matemática y análisis de estabilidad
3. **`visualizador_sistema.py`**: Generación y manejo de gráficos

### **Características de Diseño:**

- ✅ **Modularidad**: Cada módulo tiene una responsabilidad específica
- ✅ **Separación de concerns**: UI, lógica matemática y visualización están separados
- ✅ **Reutilización**: Los módulos pueden ser reutilizados independientemente
- ✅ **Mantenibilidad**: Código organizado y fácil de mantener
