import os
from datetime import datetime


def obtener_informacion():
    ruta = "datos/contactos.dat"

    if not os.path.exists(ruta):
        return None

    datos = os.stat(ruta)

    tamano = datos.st_size
    fecha = datetime.fromtimestamp(datos.st_mtime).strftime("%d/%m/%Y %H:%M:%S")
    lectura = os.access(ruta, os.R_OK)
    escritura = os.access(ruta, os.W_OK)

    return tamano, fecha, lectura, escritura