from src.Configuracion.constantes import *
from src.Modelos.contactos import Contacto

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

def guardar_contacto(contacto):
    registro = convertir_a_bytes(contacto)

    if registro is None:
        return False

    with open("datos/contactos.dat", "ab") as archivo:
        archivo.write(registro)

    return True

def leer_registro(numero_registro):
    with open("datos/contactos.dat", "rb") as archivo:
        archivo.seek(numero_registro * TAMANIO_REGISTRO)

        posicion = archivo.tell()

        registro = archivo.read(TAMANIO_REGISTRO)

        return posicion, registro

def convertir_a_contacto(registro):
    posicion = 0

    id = int(registro[posicion:posicion + ID_BYTES].decode("utf-8").strip())
    posicion += ID_BYTES

    nombre = registro[posicion:posicion + NOMBRE_BYTES].decode("utf-8").strip()
    posicion += NOMBRE_BYTES

    telefono = registro[posicion:posicion + TELEFONO_BYTES].decode("utf-8").strip()
    posicion += TELEFONO_BYTES

    correo = registro[posicion:posicion + CORREO_BYTES].decode("utf-8").strip()
    posicion += CORREO_BYTES

    ciudad = registro[posicion:posicion + CIUDAD_BYTES].decode("utf-8").strip()

    return Contacto(id, nombre, telefono, correo, ciudad)

def modificar_registro(numero_registro, contacto):
    registro = convertir_a_bytes(contacto)

    if registro is None:
        return False

    with open("datos/contactos.dat", "r+b") as archivo:
        archivo.seek(numero_registro * TAMANIO_REGISTRO)
        archivo.write(registro)
        return True
