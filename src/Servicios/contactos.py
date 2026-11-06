import os
from src.Configuracion.constantes import TAMANIO_REGISTRO
from src.Repositorio.contactos import guardar_contacto
from src.Repositorio.indice import cargar_indice, agregar_al_indice
from src.Repositorio.contactos import modificar_registro
from src.Repositorio.indice import buscar_por_id
from src.Modelos.contactos import Contacto


def registrar_contacto(contacto):
    indice = cargar_indice()

    if str(contacto.id) in indice:
        return False

    if os.path.exists("datos/contactos.dat"):
        tamano = os.path.getsize("datos/contactos.dat")
    else:
        tamano = 0

    if tamano % TAMANIO_REGISTRO != 0:
        return False

    numero_registro = tamano // TAMANIO_REGISTRO

    if not guardar_contacto(contacto):
        return False

    return agregar_al_indice(contacto.id, numero_registro)

def modificar_contacto(id, nombre, telefono, correo, ciudad):
    indice = cargar_indice()

    if str(id) not in indice:
        return False

    contacto_actual = buscar_por_id(id)

    if contacto_actual is None:
        return False

    numero_registro = indice[str(id)]

    contacto = Contacto(id, nombre, telefono, correo, ciudad)

    return modificar_registro(numero_registro, contacto)