import hashlib
import os

def calcular_hash():
    sha256 = hashlib.sha256()

    with open("datos/contactos.dat", "rb") as archivo:
        while True:
            bloque = archivo.read(4096)

            if not bloque:
                break

            sha256.update(bloque)

    return sha256.hexdigest()

def guardar_hash():
    hash_actual = calcular_hash()

    with open("datos/contactos.sha256", "w", encoding="utf-8") as archivo:
        archivo.write(hash_actual)

    return True

def verificar_integridad():
    if not os.path.exists("datos/contactos.dat"):
        return False

    if not os.path.exists("datos/contactos.sha256"):
        return False

    with open("datos/contactos.sha256", "r", encoding="utf-8") as archivo:
        hash_guardado = archivo.read().strip()

    hash_actual = calcular_hash()

    return hash_guardado == hash_actual