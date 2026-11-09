# Agenda de Contactos con Acceso Aleatorio

##  Descripción del proyecto

Este proyecto consiste en el desarrollo de una aplicación de escritorio en Python que permite administrar una agenda de contactos utilizando archivos binarios de registros de tamaño fijo y técnicas de acceso aleatorio.

El sistema permite agregar, buscar y modificar contactos sin necesidad de recorrer o reescribir completamente el archivo. También incorpora un índice para localizar registros, exportación de información, verificación de integridad mediante SHA-256 y creación de respaldos comprimidos en formato ZIP.

La aplicación cuenta con una interfaz gráfica desarrollada con Flet para facilitar la interacción del usuario.

##  Tecnologías utilizadas

- **Lenguaje:** Python.
- **Interfaz gráfica:** Flet.
- **Entorno de desarrollo:** PyCharm.
- **Almacenamiento:** Archivo binario `.dat`.
- **Índice:** Archivo JSON.
- **Integridad:** Algoritmo SHA-256.
- **Respaldos:** Compresión ZIP.
- **Exportación:** Formatos JSON y PDF.

##  Funcionalidades del sistema

### Gestión de contactos

- Agregar nuevos contactos con un identificador único.
- Buscar contactos mediante su ID.
- Modificar la información de contactos existentes.
- Almacenar los datos en un archivo binario.
- Localizar registros mediante acceso aleatorio.

### Exportación de información

- Exportar los contactos almacenados a un archivo JSON.
- Generar un reporte de contactos en formato PDF.

### Herramientas

- Verificar la integridad del archivo de contactos mediante SHA-256.
- Detectar modificaciones realizadas externamente al sistema.
- Crear respaldos comprimidos en formato ZIP.
- Mostrar información del archivo y sus tamaños.

##  Estructura de los registros

Los contactos se almacenan en el archivo `contactos.dat`, utilizando registros de tamaño fijo.

Cada registro contiene los siguientes campos:

| Campo | Tamaño |
|---|---|
| ID | 6 bytes |
| Nombre | 30 bytes |
| Teléfono | 12 bytes |
| Correo electrónico | 30 bytes |
| Ciudad | 25 bytes |
| **Total** | **103 bytes** |

Los campos se codifican utilizando UTF-8 y se completan con espacios cuando no ocupan toda la longitud asignada.

Esta estructura permite calcular directamente la posición de cualquier contacto dentro del archivo.

##  Acceso aleatorio

El sistema utiliza las funciones `seek()` y `tell()` para administrar las posiciones de los registros dentro del archivo binario.

- `seek()`: permite desplazar el puntero del archivo hasta la posición del registro que se desea consultar o modificar.
- `tell()`: permite conocer la posición actual del puntero dentro del archivo.

La posición de cada registro se calcula mediante la fórmula:

**Posición = Número de registro × 103**

Gracias a este procedimiento, es posible acceder directamente a un contacto sin recorrer todos los registros anteriores.

Cuando se modifica un contacto, el sistema sobrescribe únicamente su registro correspondiente, sin reescribir todo el archivo.

## Índice de contactos

El archivo `indice.json` almacena la relación entre el identificador de cada contacto y su número de registro.

Al realizar una búsqueda, el sistema consulta el índice para obtener la posición del contacto y posteriormente utiliza `seek()` para acceder directamente a sus datos.

Este mecanismo permite realizar búsquedas de manera más eficiente que una búsqueda secuencial dentro del archivo binario.

##  Verificación de integridad

El sistema utiliza el algoritmo SHA-256 para verificar la integridad del archivo `contactos.dat`.

Después de realizar modificaciones desde la aplicación, se actualiza el hash almacenado en `contactos.sha256`.

Al verificar la integridad, el sistema compara el hash actual del archivo con el valor previamente registrado.

Si detecta una diferencia causada por una modificación externa, muestra el mensaje:

**"El archivo fue modificado externamente o de forma manual, no desde el sistema."**

Esto permite identificar alteraciones realizadas fuera de la aplicación.

##  Sistema de respaldos

La aplicación permite generar un respaldo comprimido en formato ZIP que incluye los archivos principales:

- `contactos.dat`
- `indice.json`

Durante el proceso se obtiene información del tamaño original y del tamaño comprimido, permitiendo comparar el espacio utilizado antes y después de la compresión.

Esta funcionalidad facilita la conservación de copias de seguridad de los contactos.

##  Arquitectura del sistema

El proyecto utiliza una arquitectura por capas para separar las responsabilidades del programa.

- **Interfaz gráfica:** permite al usuario interactuar con las funcionalidades del sistema.
- **Lógica del sistema:** administra las operaciones de contactos, validaciones y herramientas.
- **Almacenamiento:** gestiona la lectura, escritura y modificación de los archivos.
- **Seguridad e integridad:** verifica posibles alteraciones mediante SHA-256.

Esta organización facilita el mantenimiento del código y la identificación de errores.

##  Archivos principales

| Archivo | Descripción |
|---|---|
| `contactos.dat` | Almacena los contactos en registros binarios de tamaño fijo. |
| `indice.json` | Relaciona cada ID con su número de registro. |
| `contactos.sha256` | Almacena el hash de referencia para verificar la integridad. |
| Archivos JSON | Contienen información exportada de los contactos. |
| Archivos PDF | Contienen reportes generados por el sistema. |
| Archivos ZIP | Contienen los respaldos comprimidos. |

## Ejecución del proyecto

Para ejecutar la aplicación es necesario contar con Python y la biblioteca Flet instalados.

Instalar Flet:

```bash
pip install flet
```

Posteriormente, abrir el proyecto en PyCharm y ejecutar el archivo principal de la aplicación.

Desde la interfaz gráfica se puede acceder a las opciones de contactos, exportación, herramientas y ayuda.

##  Conclusión

El desarrollo de este proyecto permitió aplicar conceptos fundamentales del manejo de archivos, principalmente el almacenamiento mediante registros de tamaño fijo, acceso aleatorio, utilización de índices, verificación de integridad y compresión de información.

La implementación de `seek()` y `tell()` permitió comprender cómo acceder directamente a posiciones específicas de un archivo, mientras que el índice JSON facilitó la localización de los contactos.

Además, la integración de SHA-256 y los respaldos ZIP permitió incorporar mecanismos para detectar modificaciones externas y conservar copias de seguridad de la información.

En conjunto, el proyecto demuestra cómo implementar un sistema de administración de contactos utilizando archivos binarios y una interfaz gráfica en Python.

## Documentacion
[Documentacion Tecnica](https://github.com/Juan-Chuc2/Proyecto_-2_MIA/blob/main/Manual%20tecnico%20MA.pdf)
