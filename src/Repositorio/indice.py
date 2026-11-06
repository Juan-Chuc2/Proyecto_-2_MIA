import json
import os
from src.Repositorio.contactos import leer_registro, convertir_a_contacto

def cargar_indice():
    if not os.path.exists("datos/indice.json"):
        return {}

    with open("datos/indice.json", "r", encoding="utf-8") as archivo:
        return json.load(archivo)

def guardar_indice(indice):
    with open("datos/indice.json", "w", encoding="utf-8") as archivo:
        json.dump(indice, archivo, indent=4)

def agregar_al_indice(id, numero_registro):
    indice = cargar_indice()

    if str(id) in indice:
        return False

    indice[str(id)] = numero_registro

    guardar_indice(indice)

    return True

def buscar_por_id(id):
    indice = cargar_indice()

    if str(id) not in indice:
        return None

    numero_registro = indice[str(id)]

    posicion, registro = leer_registro(numero_registro)

    if len(registro) == 0:
        return None

    contacto = convertir_a_contacto(registro)

    if contacto.id != int(id):
        return None

    return contacto

