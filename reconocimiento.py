import cv2  # type: ignore
import random
import os

LOWE_RATIO = 0.95

usuario_aleatorio = random.randint(101, 110)
print(f"Usuario seleccionado al azar: {usuario_aleatorio}")

ruta_base = "Huellas"
huellas = [f"{usuario_aleatorio}_{i}.tif" for i in range(1, 9)]
rutas_huellas = [os.path.join(ruta_base, huella) for huella in huellas]

imagenes_originales_gris = []
imagenes_procesadas = []

for ruta in rutas_huellas:
    img = cv2.imread(ruta, cv2.IMREAD_GRAYSCALE)
    if img is None:
        continue
    imagenes_originales_gris.append(img.copy())

    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    img = clahe.apply(img)

    img = cv2.GaussianBlur(img, (5, 5), 0)

    img = cv2.adaptiveThreshold(
        img, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY_INV,
        11, 2
    )
    imagenes_procesadas.append(img)

orb = cv2.ORB_create(nfeatures=500)
porcentajes_coincidencia = []

pc1, des1 = orb.detectAndCompute(imagenes_procesadas[0], None)

mejor_match_original = None
mejor_match_binarizada = None
mejor_porcentaje = -1
mejor_indice = -1

for i in range(1, len(imagenes_procesadas)):
    pc2, des2 = orb.detectAndCompute(imagenes_procesadas[i], None)
    if des2 is None:
        continue

    bf = cv2.BFMatcher(cv2.NORM_HAMMING)
    matches = bf.knnMatch(des1, des2, k=2)

    buenos_matches = []
    for match_list in matches:
        if len(match_list) == 2:
            m, n = match_list
            if m.distance < LOWE_RATIO * n.distance:
                buenos_matches.append(m)

    puntos_similares = len(buenos_matches)
    total_puntos = min(len(pc1), len(pc2))
    porcentaje_coincidencia = (
        (puntos_similares / total_puntos) * 100
        if total_puntos > 0 else 0
    )

    porcentajes_coincidencia.append(porcentaje_coincidencia)
    print(f"Porcentaje de coincidencia entre huella 1 y huella {i+1}: {porcentaje_coincidencia:.2f}%")

    if porcentaje_coincidencia > mejor_porcentaje:
        mejor_porcentaje = porcentaje_coincidencia
        mejor_indice = i
        mejor_match_original = cv2.drawMatches(
            imagenes_originales_gris[0], pc1,
            imagenes_originales_gris[i], pc2,
            buenos_matches, None,
            flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS
        )
        mejor_match_binarizada = cv2.drawMatches(
            imagenes_procesadas[0], pc1,
            imagenes_procesadas[i], pc2,
            buenos_matches, None,
            flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS
        )

if porcentajes_coincidencia:
    promedio_coincidencia = sum(porcentajes_coincidencia) / len(porcentajes_coincidencia)
    print(f"Porcentaje de coincidencia promedio para el usuario {usuario_aleatorio}: {promedio_coincidencia:.2f}%")

    if mejor_match_original is not None:
        print(f"\nMostrando la mejor coincidencia (Huella 1 vs Huella {mejor_indice+1}) con {mejor_porcentaje:.2f}%")
        cv2.imshow(f"Mejor Coincidencia Originales (1 vs {mejor_indice+1})", mejor_match_original)
        cv2.imshow(f"Mejor Coincidencia Binarizadas (1 vs {mejor_indice+1})", mejor_match_binarizada)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
