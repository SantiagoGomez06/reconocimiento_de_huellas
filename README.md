# Actividad desarrollada por los estudiantes:
 ## Jose Luis Herrera
 ## Santiago Gomez Muñoz

---

# Sistema de comparacion de huellas 

Este codigo compara huellas dactilares de un usuario seleccionado aleatoriamente usando el detector de características **ORB** de OpenCV. Selecciona un usuario al azar, preprocesa sus huellas, haciendo binarizacion y calcula el porcentaje de coincidencia entre la primera huella y cada una de las demas huellas del usuario, mostrando de manera grafica la mejor coincidencia encontrada.

---

## Requisitos

- Python 3.8+
- OpenCV (`opencv-python`)

Instala las dependencias con:
Usa bash o cmd segun tu SO

```bash ()
pip install opencv-python
```

---

## Estructura de archivos esperada

El codigo asume la siguiente estructura de directorios:

```
proyecto/
├── reconocimiento.py
└── Huellas/
    ├── 101_1.tif
    ├── 101_2.tif
    ├── ...
    ├── 110_7.tif
    └── 110_8.tif
```

Cada usuario tiene un ID entre **101 y 110**, y tiene registradas **8 huellas**, nombradas con el patrón `{usuario_id}_{numero}.tif`.

> Si alguna imagen no existe o no se puede cargar, el codigo la omite sin interrumpirse.

---

## Ejecución
Usa bash o cmd segun tu SO
```bash
python reconocimiento.py
```

El codigo seleccionará un usuario al azar en cada ejecución.

---

## ¿Qué hace el codigo?

### 1. Selección aleatoria de usuario
Se elige un ID de usuario al azar entre 101 y 110, y se comparan sus 8 huellas alojadas en la carpeta `Huellas/`.

### 2. Preprocesamiento de imágenes
Cada huella se somete a tres transformaciones antes de compararse:

- **Mejora de contraste (CLAHE):** normaliza la iluminación con un histograma adaptativo por zonas.
- **Suavizado gaussiano:** reduce el ruido de la imagen con un kernel de 5×5.
- **Binarización adaptativa:** convierte la imagen a blanco y negro de forma local para resaltar las crestas de la huella.

### 3. Comparación con ORB + BFMatcher
Se detectan hasta 500 puntos clave en cada huella usando **ORB** (Oriented FAST and Rotated BRIEF). Luego se comparan los decodigoores de la primera huella contra cada una de las demás usando un **BFMatcher** con distancia Hamming.

Para filtrar coincidencias falsas se aplica el **test de ratio de Lowe** con un umbral de `0.95`: solo se acepta un match si la distancia al vecino más cercano es significativamente menor que la del segundo vecino.

El porcentaje de coincidencia se calcula como:

```
porcentaje = (buenos_matches / min(keypoints_imagen1, keypoints_imagen2)) × 100
```

### 4. Resultados
- Se imprime el porcentaje de coincidencia entre la huella 1 y cada huella restante.
- Se calcula e imprime el promedio de coincidencia del usuario.
- Se muestra visualmente la mejor coincidencia encontrada, tanto en su versión **original en escala de grises** como en su versión **binarizada**, con líneas que conectan los puntos coincidentes.

---

## Salida en consola

```
Usuario seleccionado al azar: 105
Porcentaje de coincidencia entre huella 1 y huella 2: 72.30%
Porcentaje de coincidencia entre huella 1 y huella 3: 68.45%
...
Porcentaje de coincidencia promedio para el usuario 105: 65.80%

Mostrando la mejor coincidencia (Huella 1 vs Huella 2) con 72.30%
```

Se abrirán dos ventanas de OpenCV con la visualización. Presiona **cualquier tecla** para cerrarlas.

---

## Configuración

Puedes ajustar el comportamiento del codigo modificando la constante al inicio del archivo:

| Variable | Valor por defecto | Descripción |
|---|---|---|
| `LOWE_RATIO` | `0.95` | Umbral del test de ratio de Lowe. Valores más bajos son más estrictos y reducen los falsos positivos. |
