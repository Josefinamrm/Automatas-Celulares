# Autómatas Celulares - Simulación de Sistemas

Trabajo Práctico Nro. 2 de la materia (72.25) Simulación de Sistemas - ITBA

## Descripción

Este proyecto implementa una simulación de autómatas celulares para modelar el comportamiento de partículas en un sistema con posibles líderes. La simulación explora conceptos de polarización, ruido (eta) y efectos de liderazgo en sistemas de partículas.

El código está dividido en:

- **Java**: Lógica de simulación (App.java, Particle.java, etc.)
- **Python**: Scripts de visualización y análisis (visualize.py, plot_va.py, etc.)

## Requisitos

- **Java**: JDK 8 o superior
- **Python**: 3.x con las siguientes librerías:
  - matplotlib
  - numpy
  - (instalar con `pip install matplotlib numpy`)

## Compilación

Para compilar el código Java:

```bash
javac *.java
```

## Ejecución

Ejecutar la simulación con parámetros específicos:

```bash
java App <N> <L> <M> <rc> <periodic> <iterations> <eta> <withLeader> <leaderID> <circleLeader>
```

### Parámetros:

- `N`: Número de partículas
- `L`: Tamaño del espacio
- `M`: Otro parámetro (ver código para detalles)
- `rc`: Radio de interacción
- `periodic`: Condiciones de contorno periódicas (0/1)
- `iterations`: Número de iteraciones
- `eta`: Nivel de ruido
- `withLeader`: Si hay líder (0/1)
- `leaderID`: ID del líder
- `circleLeader`: Tipo de líder circular (0/1)

## Scripts

- `run.sh`: Ejecuta una simulación individual
- `run_all_scenarios.sh`: Ejecuta múltiples escenarios para análisis comparativo

## Visualización

### Crear animación:

```bash
python3 visualize.py
```

### Crear gráfico de evolución temporal:

```bash
python3 plot_va.py <T-Estacionario>
```

Donde `<T-Estacionario>` es el tiempo de estacionario.

### Gráfico de polarización vs ruido:

```bash
./run_all_scenarios.sh
```

(Modificar parámetros dentro del script según sea necesario)

## Resultados

Los resultados se almacenan en las carpetas `results/`, `results-p2/`, `results-p4/` con subcarpetas por tipo de líder y valor de eta.

## Estructura del Proyecto

- `java/`: Código fuente Java
- `results/`: Resultados de simulaciones
- `png-old/`: Imágenes antiguas
- Scripts de Python para análisis

## Contribución

Proyecto académico para la materia Simulación de Sistemas - ITBA.

## Licencia

Este proyecto es para fines educativos.
