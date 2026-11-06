from src.Configuracion.constantes import *

def convertir_a_bytes(contacto):

    if not validar_tamanos(contacto):
        return None

    id_bytes = str(contacto.id).encode("utf-8").ljust(ID_BYTES, b" ")
    nombre_bytes = contacto.nombre.encode("utf-8").ljust(NOMBRE_BYTES, b" ")
    telefono_bytes = contacto.telefono.encode("utf-8").ljust(TELEFONO_BYTES, b" ")
    correo_bytes = contacto.correo.encode("utf-8").ljust(CORREO_BYTES, b" ")
    ciudad_bytes = contacto.ciudad.encode("utf-8").ljust(CIUDAD_BYTES, b" ")

    return id_bytes + nombre_bytes + telefono_bytes + correo_bytes + ciudad_bytes

def validar_tamanos(contacto):
    if len(str(contacto.id).encode("utf-8")) > ID_BYTES:
        return False

    if len(contacto.nombre.encode("utf-8")) > NOMBRE_BYTES:
        return False

    if len(contacto.telefono.encode("utf-8")) > TELEFONO_BYTES:
        return False

    if len(contacto.correo.encode("utf-8")) > CORREO_BYTES:
        return False

    if len(contacto.ciudad.encode("utf-8")) > CIUDAD_BYTES:
        return False

    return True