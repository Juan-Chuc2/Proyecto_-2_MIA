import json
import os
from src.Repositorio.contactos import leer_registro, convertir_a_contacto

def cargar_indice():
    if not os.path.exists("datos/indice.json"):
        return {}

    try:
        with open("datos/indice.json", "r", encoding="utf-8") as archivo:
            indice = json.load(archivo)

        if not isinstance(indice, dict):
            return None

        return indice

    except (OSError, UnicodeError, json.JSONDecodeError):
        return None

def guardar_indice(indice):
    with open("datos/indice.json", "w", encoding="utf-8") as archivo:
        json.dump(indice, archivo, indent=4)

def agregar_al_indice(id, numero_registro):
    indice = cargar_indice()

    if indice is None:
        return False

    if str(id) in indice:
        return False

    if not isinstance(numero_registro, int) or numero_registro < 0:
        return False

    indice[str(id)] = numero_registro

    guardar_indice(indice)

    return True

def buscar_por_id(id):
    indice = cargar_indice()

    if indice is None:
        return None

    if str(id) not in indice:
        return None

    numero_registro = indice[str(id)]

    if not isinstance(numero_registro, int) or numero_registro < 0:
        return None

    posicion, registro = leer_registro(numero_registro)

    if registro is None:
        return None

    contacto = convertir_a_contacto(registro)

    if contacto.id != int(id):
        return None

    return contacto