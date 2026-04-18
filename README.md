# Identificacion de senalamientos con vision por computadora

Este proyecto detecta y clasifica senales de transito usando color + forma con OpenCV.

Hay dos notebooks principales:

- `proyecto.ipynb`: version DOC1 (incluye logica para CURVA, ALTO PROXIMO y CRUCE/CRUCENAR).
- `proyecto2.ipynb`: version DOC2 (incluye OBRAS y CRUCE naranja con reglas un poco distintas).

## 1) Que hace cada notebook

Cada notebook tiene 2 partes de codigo:

1. **Prueba con imagenes**
   - Lee imagenes de `img/sinfondo`.
   - Convierte a HSV.
   - Crea mascaras por color (azul, rojo, amarillo, naranja, verde, negro segun el caso).
   - Limpia ruido con operaciones morfologicas.
   - Busca contornos y los dibuja.

2. **Deteccion en tiempo real con camara**
   - Abre la camara.
   - Analiza solo una zona central (ROI).
   - Detecta colores.
   - Clasifica por forma (triangulo, rombo, octagono, circulo).
   - Muestra etiqueta y porcentaje aproximado de confianza.

## 2) Logica de deteccion (explicacion facil)

El flujo general es este:

1. **Color primero**: separa posibles senales por color en HSV.
2. **Limpieza**: quita ruido pequeno con MORPH_OPEN y rellena huecos con MORPH_CLOSE.
3. **Contornos**: encuentra figuras candidatas.
4. **Clasificacion por forma**:
   - Circulo -> puede ser 20KMH.
   - Octagono -> puede ser ALTO.
   - Triangulo invertido -> CEDA EL PASO.
   - Triangulo normal (en DOC2) -> OBRAS.
   - Rombo amarillo/naranja -> CURVA, ALTO PROXIMO, CRUCE.
5. **Prioridades**: en `proyecto.ipynb`, si hay ALTO PROXIMO, se evita mostrar CRUCE en el mismo frame.

## 3) Lo mas importante para mejorar deteccion (partes a editar)

Esta es la seccion clave cuando cambias de camara, luz o tipo de senal.

### 5.1 Rangos HSV (lo mas importante)

Busca variables como:

- `azul_b`, `azul_a`
- `amarillo_b`, `amarillo_a`
- `naranja_b`, `naranja_a`
- `rojo_b1`, `rojo_a1`, `rojo_b2`, `rojo_a2`
- `verde_b`, `verde_a`
- `negro_b`, `negro_a`

Si falla color:

- Amplia el rango si no detecta.
- Reduce el rango si detecta cosas que no son.
- Ajusta sobre todo `S` y `V` cuando cambia la iluminacion.

Tip rapido:

- Si hay mucho brillo, sube el minimo de `S` o baja el maximo de `V` en el color conflictivo.
- Si la senal sale "apagada", baja minimos de `S`/`V`.

### 5.2 `min_area`

Variable: `min_area`.

- Si detecta mucho ruido -> **sube** `min_area`.
- Si no detecta senales pequenas -> **baja** `min_area`.

### 5.3 Tamano de ROI (recuadro central)

Variables:

- `x1, y1, x2, y2`

Si quieres detectar en mas zona de la imagen:

- Haz el ROI mas grande.

Si quieres reducir falsos positivos:

- Haz el ROI mas pequeno y centrado.

### 5.4 Suavizado y morfologia

Variables importantes:

- `cv2.GaussianBlur(roi,(7,7),0)`
- `kernel=np.ones((3,3),np.uint8)`

Reglas:

- Mas blur (ej. `(9,9)`) = menos ruido, pero puede borrar detalles finos.
- Kernel mayor (ej. `(5,5)`) = limpia mas, pero puede comerse senales pequenas.

### 5.5 Umbrales geometricos (forma)

En celdas de camara veras reglas como:

- `lados==3`, `7<=lados<=9`
- `circ > ...`
- `fill_circ > ...`
- `0.70 < asp < 1.35`

Estas reglas mandan en la clasificacion final.

Si hay confusiones entre ALTO y 20KMH:

- Endurece condicion de circularidad para 20KMH.
- Endurece rango de lados/circularidad para ALTO.

Si no detecta triangulos:

- Relaja tolerancias de orientacion y proporcion.

## 4) Como adaptarlo a otras situaciones (guia practica)

Si quieres detectar otro objeto/senal:

1. Junta 20-50 imagenes de ejemplo con distintas luces.
2. Define color principal del objeto en HSV.
3. Crea mascara para ese color.
4. Limpia mascara con open/close.
5. Extrae contornos y filtra por `min_area`.
6. Mide forma (lados, aspect ratio, circularidad).
7. Crea reglas de clasificacion simples.
8. Prueba en camara real y ajusta umbrales.
9. Repite hasta tener estabilidad.

## 5) Problemas comunes y solucion rapida

- **No detecta nada**:
  - Revisa que la camara abra.
  - Baja `min_area`.
  - Amplia rangos HSV.

- **Detecta demasiadas cosas falsas**:
  - Sube `min_area`.
  - Reduce rangos HSV.
  - Aumenta kernel morfologico.

- **Falla con cambios de luz**:
  - Ajusta `S` y `V` en HSV.
  - Evita reflejos directos.
  - Prueba iluminacion mas uniforme.

## 6) Diferencia rapida entre notebooks

- `proyecto.ipynb`:
  - Incluye reglas para CURVA y ALTO PROXIMO.
  - Tiene prioridad para evitar CRUCE cuando aparece ALTO PROXIMO.

- `proyecto2.ipynb`:
  - Incluye OBRAS (triangulo normal).
  - Enfocado en CRUCE naranja y clasificacion roja alternativa.

## 7) Recomendacion final

Empieza siempre ajustando en este orden:

1. Rangos HSV
2. `min_area`
3. ROI
4. Morfologia y blur
5. Reglas geometricas

Ese orden ahorra mucho tiempo y suele mejorar la deteccion mas rapido.