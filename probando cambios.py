import cv2
import numpy as np
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import json

# Inicializa Firebase con tu clave de servicio
cred = credentials.Certificate('C:\\Users\\sergi\\Desktop\\parking-66bb4-firebase-adminsdk-5x5f0-810cb338ec.json')  # Reemplaza con la ruta correcta
firebase_admin.initialize_app(cred)
db = firestore.client()

# Cargar la base de datos local desde un archivo JSON
def cargar_base_datos_local():
    with open('db_local.json', 'r') as file:
        return json.load(file)

# Guardar los cambios en la base de datos local
def guardar_base_datos_local(estado_local):
    with open('db_local.json', 'w') as file:
        json.dump(estado_local, file)

# Inicializar la base de datos local con todos los lugares en estado "ROJO"
estado_local = cargar_base_datos_local()

# Actualizar en Firebase solo si el estado ha cambiado
def cambiar_estado_en_firebase(identificador, nuevo_estado):
    doc_ref = db.collection(u'lugares').document(str(identificador))
    doc_ref.update({
        u'estado': nuevo_estado
    })

# Cambiar estado solo si es diferente al estado local
def cambiar_estado_si_necesario(identificador, nuevo_estado):
    global estado_local
    if estado_local[str(identificador)] != nuevo_estado:
        # Actualizar en Firebase y también localmente
        cambiar_estado_en_firebase(identificador, nuevo_estado)
        estado_local[str(identificador)] = nuevo_estado
        guardar_base_datos_local(estado_local)  # Guardar el cambio en la base de datos local
        print(f"Actualizado el lugar {identificador} a {nuevo_estado}")
    else:
        print(f"Lugar {identificador} no cambió, no se actualiza.")

# Lista de posiciones de los lugares de estacionamiento
posList = [
    (1, 55, 100), (2, 163, 98), (3, 56, 146), (4, 164, 146),
    (5, 50, 193)
]

cap = cv2.VideoCapture('CarPark.mp4')
width, height = 107, 48  # Dimensiones de cada espacio de estacionamiento

def checkParkingSpace(imgPro, img):
    global posList
    contadorEspacios = 0

    for i, pos in enumerate(posList):
        x, y = pos[1], pos[2]
        text_size = cv2.getTextSize(str(i+1), cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2)[0]
        text_x = x + (width - text_size[0]) // 2
        text_y = y + (height + text_size[1]) // 2
        cv2.putText(img, str(i+1), (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

    for pos in posList:
        x, y = pos[1], pos[2]
        imgCrop = imgPro[y:y + height, x:x + width]  # Extraer cada espacio de estacionamiento

        count = cv2.countNonZero(imgCrop)  # Contar píxeles no cero

        if count < 800:  # Umbral ajustable
            color = (0, 255, 0)  # Verde para espacios vacíos
            contadorEspacios += 1
            nuevo_estado = "VERDE"
        else:
            color = (0, 0, 255)  # Rojo para espacios ocupados
            nuevo_estado = "ROJO"
        
        identificador = pos[0]
        cambiar_estado_si_necesario(identificador, nuevo_estado)  # Solo actualizar si cambia el estado

        # Dibujar rectángulo y conteo
        cv2.rectangle(img, (x, y), (x + width, y + height), color, 2)
        cv2.putText(img, str(count), (x, y + height - 3), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)

    # Mostrar el número total de espacios libres
    cv2.putText(img, f"Libres: {contadorEspacios}/{len(posList)}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 200, 0), 2)

while True:
    success, img = cap.read()
    if not success:
        print("No se puede recibir más frames. Saliendo...")
        break

    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # Convertir a escala de grises
    imgBlur = cv2.GaussianBlur(imgGray, (3, 3), 1)  # Aplicar desenfoque
    imgThreshold = cv2.adaptiveThreshold(imgBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 17, 20)
    imgMedian = cv2.medianBlur(imgThreshold, 5) #Elimina ruido y sal 
    kernel = np.ones((3, 3), np.uint8)
    imgDilate = cv2.dilate(imgThreshold, kernel, iterations=1)
    cv2.imshow("Imagen a procesar: ", imgDilate)

    # Verificación de los espacios de parking
    checkParkingSpace(imgDilate, img)
    cv2.imshow("Detección de espacios libres de Parking", img)  # Mostrar imagen

    if cv2.waitKey(50) & 0xFF == ord('q'):  # Salir con la tecla 'q'
        break

cap.release()
cv2.destroyAllWindows()


