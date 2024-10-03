import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Inicializa Firebase con tu clave de servicio
cred = credentials.Certificate('C:\\Users\\sergi\\Desktop\\parking-66bb4-firebase-adminsdk-5x5f0-810cb338ec.json')  # Reemplaza con la ruta correcta
firebase_admin.initialize_app(cred)
db = firestore.client()

# Función para cambiar el estado de un documento
def cambiar_estado(identificador, nuevo_estado):
    doc_ref = db.collection(u'lugares').document(str(identificador))
    doc_ref.update({
        u'estado': nuevo_estado
    })

# Función para crear un nuevo lugar
def crear_lugar(identificador, estado):
    doc_ref = db.collection(u'lugares').document(str(identificador))
    doc_ref.set({
        u'estado': estado
    })

# Crear 10 lugares
#crear_lugar(i, 'VERDE')  # Puedes cambiar el estado inicial si lo deseas
# Ejemplo de uso:

cambiar_estado(11, "ROJO")

print("Estado actualizado con éxito!")