# ProyectoExitoso: Sistema de Detección de Señalización Vial

  Este proyecto implementa un sistema de visión artificial en tiempo real diseñado para identificar y resaltar señales de tránsito basándose en el análisis de
  morfología y segmentación por color.

### Metodología Técnica

  El funcionamiento del sistema se divide en tres fases operativas principales:

  1. Extracción de Patrones de Referencia
  El algoritmo procesa un conjunto de imágenes predefinidas de señales de tránsito (alojadas en la ruta img/sinfondo/). Para cada referencia, se ejecutan los
  siguientes pasos:
   * Conversión de Espacio de Color: Transformación de BGR a HSV para facilitar la segmentación cromática independiente de la iluminación.
   * Segmentación Cromática: Aplicación de máscaras binarias para aislar tonos rojos (considerando ambos rangos de saturación en el espectro HSV) y amarillos.
   * Análisis de Contornos: Identificación y almacenamiento del contorno externo más significativo para utilizarlo como huella morfológica.
  2. Procesamiento de Video en Tiempo Real
  Durante la captura mediante periféricos de video, el sistema optimiza la carga computacional y la precisión mediante:
   * Definición de ROI (Region of Interest): Delimitación de un área central en el cuadro de video donde se concentra la búsqueda de señales.
   * Filtrado Dinámico: Replicación del proceso de segmentación de color sobre cada fotograma capturado dentro de la región delimitada.

  3. Clasificación y Validación
  Para determinar la presencia de una señal válida, el sistema emplea:
  Stack Tecnológico
   * OpenCV: Procesamiento de imágenes, análisis de contornos y captura de video.
   * NumPy: Manipulación de arreglos multidimensionales y operaciones matriciales.
   * Matplotlib: Visualización y depuración de resultados en el entorno de desarrollo.

### Consideraciones Operativas
  El sistema está optimizado para la detección de señales con perímetros rojos o amarillos (como señales de ALTO, Ceda el Paso o advertencias de curva). La
  precisión del modelo es dependiente de la calibración de los rangos HSV y la calidad de la iluminación ambiental durante la captura.