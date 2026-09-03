import cv2 as cv
import numpy as np

# Variable global para HSV
hsv = None
frame = None

# Función para obtener HSV al hacer clic
def getHSV(event, x, y, flags, param):
    global hsv

    if event == cv.EVENT_LBUTTONDOWN:
        print(f"Pixel ({x},{y}) -> HSV:", hsv[y, x])

cap = cv.VideoCapture(0)

# Ventana y callback
cv.namedWindow("Camara")
cv.setMouseCallback("Camara", getHSV)

# Rangos HSV
lowerBound = np.array([120,60,50])
upperBound = np.array([150,100,70])

while True:
    ret, frame = cap.read()

    if not ret:
        break

    # Convertir a HSV
    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

    # Crear máscara
    mask = cv.inRange(hsv, lowerBound, upperBound)

    # Filtrado morfológico
    kernel = np.ones((5,5), np.uint8)

    mask = cv.morphologyEx(mask, cv.MORPH_OPEN, kernel)
    mask = cv.morphologyEx(mask, cv.MORPH_CLOSE, kernel)

    # Aplicar máscara
    result = cv.bitwise_and(frame, frame, mask=mask)

    # Mostrar ventanas
    cv.imshow("Camara", frame)
    cv.imshow("Mascara", mask)
    cv.imshow("Resultado", result)

    key = cv.waitKey(1)
    if key == 27:
        break

cap.release()
cv.destroyAllWindows()    