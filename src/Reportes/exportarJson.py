import json
import os

from src.Repositorio.contactos import obtener_todos_contactos


def exportar_json():
    contactos = obtener_todos_contactos()
    datos = []

    for contacto in contactos:
        datos.append({
            "id": contacto.id,
            "nombre": contacto.nombre,
            "telefono": contacto.telefono,
            "correo": contacto.correo,
            "ciudad": contacto.ciudad
        })

    os.makedirs("exportaciones", exist_ok=True)

    with open("exportaciones/contactos.json", "w", encoding="utf-8") as archivo:
        json.dump(datos, archivo, indent=4, ensure_ascii=False)

    return True