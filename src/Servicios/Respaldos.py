import os
import zipfile


def crear_respaldo():
    os.makedirs("Respaldos", exist_ok=True)

    with zipfile.ZipFile("Respaldos/respaldo_contactos.zip", "w",
                         compression=zipfile.ZIP_DEFLATED) as zip_archivo:

        zip_archivo.write("datos/contactos.dat", "contactos.dat")
        zip_archivo.write("datos/indice.json", "indice.json")

    return True

def comparar_tamanios():
    tamano_contactos = os.path.getsize("datos/contactos.dat")
    tamano_indice = os.path.getsize("datos/indice.json")

    tamano_original = tamano_contactos + tamano_indice

    tamano_zip = os.path.getsize("Respaldos/respaldo_contactos.zip")

    diferencia = tamano_original - tamano_zip

    return tamano_original, tamano_zip, diferencia