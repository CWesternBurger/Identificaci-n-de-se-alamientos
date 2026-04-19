import numpy as np
import cv2
import os

def load_reference_contours(rutas):
    contornos_ref = []
    for ruta in rutas:
        if not os.path.exists(ruta):
            print(f"Warning: File {ruta} not found.")
            continue
        
        img_ref = cv2.imread(ruta)
        if img_ref is not None:
            hsv_ref = cv2.cvtColor(img_ref, cv2.COLOR_BGR2HSV)

            # Define color ranges for red and yellow
            rojo_b1 = np.array([0, 80, 80], np.uint8)
            rojo_a1 = np.array([10, 255, 255], np.uint8)
            rojo_b2 = np.array([160, 80, 80], np.uint8)
            rojo_a2 = np.array([180, 255, 255], np.uint8)
            amarillo_b = np.array([18, 80, 80], np.uint8)
            amarillo_a = np.array([35, 255, 255], np.uint8)

            m_rojo_1 = cv2.inRange(hsv_ref, rojo_b1, rojo_a1)
            m_rojo_2 = cv2.inRange(hsv_ref, rojo_b2, rojo_a2)
            m_rojo = m_rojo_1 + m_rojo_2
            m_amarillo = cv2.inRange(hsv_ref, amarillo_b, amarillo_a)
            m_total = m_rojo + m_amarillo

            contornos_r, _ = cv2.findContours(m_total, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            area_max_r = 0
            contorno_max_r = None
            for c in contornos_r:
                area_r = cv2.contourArea(c)
                if area_r > area_max_r:
                    area_max_r = area_r
                    contorno_max_r = c

            if contorno_max_r is not None and area_max_r > 200:
                contornos_ref.append(contorno_max_r)
    return contornos_ref

def main():
    rutas = [
        'img/sinfondo/20kmh.png',
        'img/sinfondo/altosin.png',
        'img/sinfondo/cedapaso2.png',
        'img/sinfondo/cruce2.png',
        'img/sinfondo/curva2.png',
        'img/sinfondo/estacionarno.png',
        'img/sinfondo/norebasar2.png',
        'img/sinfondo/separacion2.png'
    ]

    print("Loading reference contours...")
    contornos_ref = load_reference_contours(rutas)
    print(f"Loaded {len(contornos_ref)} reference contours.")

    print("Initializing camera...")
    cam = cv2.VideoCapture(0)
    if not cam.isOpened():
        print("Error: Could not open camera.")
        return

    print("Starting detection loop. Press '0' to exit.")
    while True:
        ret, frame = cam.read()

        if ret:
            salida = frame.copy()
            h_frame, w_frame = frame.shape[:2]

            x1 = int(w_frame * 0.25)
            y1 = int(h_frame * 0.20)
            x2 = int(w_frame * 0.75)
            y2 = int(h_frame * 0.85)

            roi = frame[y1:y2, x1:x2].copy()
            hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)

            rojo_b1 = np.array([0, 80, 80], np.uint8)
            rojo_a1 = np.array([10, 255, 255], np.uint8)
            rojo_b2 = np.array([160, 80, 80], np.uint8)
            rojo_a2 = np.array([180, 255, 255], np.uint8)
            amarillo_b = np.array([18, 80, 80], np.uint8)
            amarillo_a = np.array([35, 255, 255], np.uint8)

            mask_rojo_1 = cv2.inRange(hsv, rojo_b1, rojo_a1)
            mask_rojo_2 = cv2.inRange(hsv, rojo_b2, rojo_a2)
            mask_rojo = mask_rojo_1 + mask_rojo_2
            mask_amarillo = cv2.inRange(hsv, amarillo_b, amarillo_a)
            mask_senal = mask_rojo + mask_amarillo

            contornos, _ = cv2.findContours(mask_senal, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            mejor_match = 999
            mejor_contorno = None
            area_roi = (x2 - x1) * (y2 - y1)

            for c in contornos:
                area = cv2.contourArea(c)
                if area > area_roi * 0.02 and area < area_roi * 0.95:
                    for i in range(len(contornos_ref)):
                        similitud = cv2.matchShapes(c, contornos_ref[i], cv2.CONTOURS_MATCH_I1, 0.0)
                        if similitud < mejor_match:
                            mejor_match = similitud
                            mejor_contorno = c

            if mejor_contorno is not None and mejor_match < 0.35:
                hull = cv2.convexHull(mejor_contorno)
                cv2.drawContours(roi, [hull], -1, (0, 255, 255), 3)

            salida[y1:y2, x1:x2] = roi
            cv2.rectangle(salida, (x1, y1), (x2, y2), (255, 255, 0), 2)
            cv2.imshow("Camara detector", salida)

        if cv2.waitKey(1) & 0xFF == ord('0'):
            break

    cam.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
