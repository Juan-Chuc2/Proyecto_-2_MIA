import os

from src.Configuracion.constantes import TAMANIO_REGISTRO
from src.Repositorio.contactos import guardar_contacto
from src.Repositorio.indice import cargar_indice, agregar_al_indice


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