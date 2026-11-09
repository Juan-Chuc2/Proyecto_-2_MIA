
import flet as ft
from src.Modelos.contactos import Contacto
from src.Servicios.contactos import registrar_contacto, modificar_contacto
from src.Repositorio.indice import buscar_por_id
from src.Reportes.exportarJson import exportar_json
from src.Reportes.reportePDF import generar_pdf
from src.Servicios.Integridad import verificar_integridad
from src.Servicios.Respaldos import crear_respaldo, comparar_tamanios
from src.Servicios.Informacion import obtener_informacion


def ventana_principal(page: ft.Page):
    page.title, page.window.maximized = "Agenda de Contactos", True
    page.padding, page.spacing, page.theme_mode = 0, 0, ft.ThemeMode.LIGHT

    azul, fondo, blanco = "#5298D3", "#F7FAFC", "#FFFFFF"

    id_c, nombre, telefono, correo, ciudad = ft.TextField(label="ID"), ft.TextField(label="Nombre"), ft.TextField(label="Teléfono"), ft.TextField(label="Correo"), ft.TextField(label="Ciudad")
    mensaje, id_buscar, resultado_busqueda = ft.Text(), ft.TextField(label="ID del contacto"), ft.Text()
    id_modificar, nombre_modificar, telefono_modificar, correo_modificar, ciudad_modificar, mensaje_modificar = ft.TextField(label="ID del contacto"), ft.TextField(label="Nombre"), ft.TextField(label="Teléfono"), ft.TextField(label="Correo"), ft.TextField(label="Ciudad"), ft.Text()
    campos_modificar = [nombre_modificar, telefono_modificar, correo_modificar, ciudad_modificar]
    mensaje_exportar, mensaje_integridad, mensaje_respaldo, mensaje_informacion = ft.Text(), ft.Text(), ft.Text(), ft.Text()

    def guardar_contacto(e):
        campos = [id_c, nombre, telefono, correo, ciudad]
        if not all(c.value for c in campos): mensaje.value = "Debe completar todos los campos."
        elif not id_c.value.isdigit(): mensaje.value = "El ID debe ser un número entero."
        elif registrar_contacto(Contacto(int(id_c.value), nombre.value, telefono.value, correo.value, ciudad.value)):
            mensaje.value = "Contacto registrado correctamente."
            for c in campos: c.value = ""
        else: mensaje.value = "No se pudo registrar, verifique el ID y tamaños permitidos."
        page.update()

    def buscar_contacto(e):
        if not id_buscar.value or not id_buscar.value.strip().isdigit(): resultado_busqueda.value = "Ingrese un ID numérico válido."
        else:
            contacto = buscar_por_id(int(id_buscar.value.strip()))
            resultado_busqueda.value = "Contacto no encontrado." if contacto is None else f"ID: {contacto.id}\nNombre: {contacto.nombre}\nTeléfono: {contacto.telefono}\nCorreo: {contacto.correo}\nCiudad: {contacto.ciudad}"
        page.update()

    def buscar_para_modificar(e):
        for campo in campos_modificar: campo.value, campo.disabled = "", True
        boton_guardar_cambios.disabled = True
        if not id_modificar.value or not id_modificar.value.strip().isdigit(): mensaje_modificar.value = "Ingrese un ID numérico válido."
        else:
            contacto = buscar_por_id(int(id_modificar.value.strip()))
            if contacto is None: mensaje_modificar.value = "Contacto no encontrado."
            else:
                nombre_modificar.value, telefono_modificar.value, correo_modificar.value, ciudad_modificar.value = contacto.nombre, contacto.telefono, contacto.correo, contacto.ciudad
                for campo in campos_modificar: campo.disabled = False
                boton_guardar_cambios.disabled, mensaje_modificar.value = False, "Contacto encontrado. Puede modificar sus datos."
        page.update()

    def guardar_cambios(e):
        if not all(c.value and c.value.strip() for c in campos_modificar): mensaje_modificar.value = "Debe completar todos los campos."
        elif modificar_contacto(int(id_modificar.value), nombre_modificar.value, telefono_modificar.value, correo_modificar.value, ciudad_modificar.value):
            mensaje_modificar.value = "Contacto modificado correctamente."
            for campo in campos_modificar: campo.value, campo.disabled = "", True
            boton_guardar_cambios.disabled, id_modificar.value = True, ""
        else: mensaje_modificar.value = "No se pudo modificar el contacto."
        page.update()

    def exportar_contactos(e):
        mensaje_exportar.value = "Contactos exportados correctamente en exportaciones/contactos.json" if exportar_json() else "No se pudieron exportar los contactos."
        page.update()

    def generar_reporte(e):
        mensaje_exportar.value = "Reporte PDF generado correctamente en exportaciones/reporte_contactos.pdf" if generar_pdf() else "No se pudo generar el reporte PDF."
        page.update()

    def comprobar_integridad(e):
        try:
            if verificar_integridad(): mensaje_integridad.value = "Integridad correcta. El archivo no ha sido modificado externamente."
            else: mensaje_integridad.value = "El archivo fue modificado externamente o de forma manual, no desde el sistema."
        except (OSError, ValueError): mensaje_integridad.value = "No fue posible leer el archivo o su referencia SHA-256."
        page.update()

    def generar_respaldo(e):
        try:
            if crear_respaldo():
                original, comprimido, diferencia = comparar_tamanios()
                mensaje_respaldo.value = f"Respaldo creado correctamente en respaldos/respaldo_contactos.zip\nTamaño original: {original} bytes\nTamaño comprimido: {comprimido} bytes\nDiferencia: {diferencia} bytes"
            else: mensaje_respaldo.value = "No se pudo crear el respaldo."
        except (OSError, ValueError): mensaje_respaldo.value = "Error al crear el respaldo o comparar los tamaños."
        page.update()

    def mostrar_informacion(e):
        try:
            informacion = obtener_informacion()
            if informacion is None: mensaje_informacion.value = "No se encontró el archivo contactos.dat."
            else:
                tamano, fecha, lectura, escritura = informacion
                mensaje_informacion.value = f"Tamaño: {tamano} bytes\nÚltima modificación: {fecha}\nPermiso de lectura: {'Sí' if lectura else 'No'}\nPermiso de escritura: {'Sí' if escritura else 'No'}"
        except OSError: mensaje_informacion.value = "Error al obtener la información del archivo."
        page.update()

    formulario = ft.Column(controls=[ft.Text("AGREGAR CONTACTO", size=22, weight=ft.FontWeight.BOLD), id_c, nombre, telefono, correo, ciudad, ft.Button("Guardar contacto", on_click=guardar_contacto), mensaje],
    horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=15, width=400, visible=False)

    formulario_busqueda = ft.Column(controls=[ft.Text("BUSCAR CONTACTO", size=22, weight=ft.FontWeight.BOLD), id_buscar, ft.Button("Buscar", on_click=buscar_contacto), resultado_busqueda], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=15, width=400, visible=False)

    for campo in campos_modificar: campo.disabled = True
    boton_guardar_cambios = ft.Button("Guardar cambios", on_click=guardar_cambios, disabled=True)

    formulario_modificar = ft.Column(controls=[ft.Text("MODIFICAR CONTACTO", size=22, weight=ft.FontWeight.BOLD), id_modificar, ft.Button("Buscar", on_click=buscar_para_modificar), nombre_modificar, telefono_modificar, correo_modificar, ciudad_modificar, boton_guardar_cambios, mensaje_modificar], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=15, width=400, visible=False)

    formulario_exportar = ft.Column(controls=[ft.Text("EXPORTAR CONTACTOS", size=22, weight=ft.FontWeight.BOLD), ft.Button("Exportar a JSON", on_click=exportar_contactos), ft.Button("Generar reporte PDF", on_click=generar_reporte), mensaje_exportar], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=15, width=400, visible=False)

    formulario_herramientas = ft.Column(controls=[ft.Text("HERRAMIENTAS", size=22, weight=ft.FontWeight.BOLD), ft.Button("Verificar integridad SHA-256", on_click=comprobar_integridad), mensaje_integridad, ft.Divider(), ft.Button("Crear respaldo ZIP", on_click=generar_respaldo), mensaje_respaldo, ft.Divider(),
    ft.Button("Información del archivo", on_click=mostrar_informacion), mensaje_informacion], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=15, width=400, visible=False)

    formulario_ayuda = ft.Column(controls=[ft.Text("AYUDA", size=22, weight=ft.FontWeight.BOLD), ft.Text("Simulado")], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=15, width=400, visible=False)

    formulario_inicio = ft.Column(controls=[ft.Icon(ft.Icons.CONTACT_PAGE, size=55, color="#98A4B3"), ft.Text("Bienvenido a la Agenda de Contactos", size=22, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
    ft.Text("Seleccione una opcion en el menú lateral para comenzar.", size=13, color="#7D8793", text_align=ft.TextAlign.CENTER)], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=20)

    tarjeta_inicio = ft.Container(content=formulario_inicio, bgcolor=blanco, border_radius=12, padding=45, width=430, visible=True)

    titulo_seccion = ft.Text("INICIO", size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE)
    barra_superior = ft.Container(content=titulo_seccion, bgcolor=azul, padding=ft.Padding(20, 15, 20, 15), border_radius=5)

    botones_contactos = ft.Row(controls=[ft.Button("Agregar contacto", on_click=lambda _: mostrar_seccion("agregar")), ft.Button("Buscar contacto", on_click=lambda _: mostrar_seccion("buscar")),
    ft.Button("Modificar contacto", on_click=lambda _: mostrar_seccion("modificar"))], alignment=ft.MainAxisAlignment.CENTER, spacing=12, wrap=True, visible=False)

    contenido = ft.Column(controls=[tarjeta_inicio, botones_contactos, formulario, formulario_busqueda, formulario_modificar, formulario_exportar, formulario_herramientas, formulario_ayuda],
    horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=25, scroll=ft.ScrollMode.AUTO, expand=True)

    def mostrar_seccion(seccion):
        formulario.visible, formulario_busqueda.visible, formulario_modificar.visible, formulario_exportar.visible, formulario_herramientas.visible, formulario_ayuda.visible = seccion == "agregar", seccion == "buscar", seccion == "modificar", seccion == "exportar", seccion == "herramientas", seccion == "ayuda"
        tarjeta_inicio.visible = seccion == "inicio"
        botones_contactos.visible = seccion in ["contactos", "agregar", "buscar", "modificar"]

        if seccion == "inicio": titulo_seccion.value = "INICIO"
        elif seccion in ["contactos", "agregar", "buscar", "modificar"]: titulo_seccion.value = "CONTACTOS"
        elif seccion == "exportar": titulo_seccion.value = "EXPORTAR"
        elif seccion == "herramientas": titulo_seccion.value = "HERRAMIENTAS"
        elif seccion == "ayuda": titulo_seccion.value = "AYUDA"

        page.update()

    def boton_lateral(texto, icono, seccion):
        return ft.Button(texto, icon=icono, width=190, height=45, on_click=lambda _: mostrar_seccion(seccion))

    panel_lateral = ft.Container(content=ft.Column(controls=[
        ft.Container(content=ft.Text("Agenda de Contactos", size=18, weight=ft.FontWeight.BOLD, color=azul, text_align=ft.TextAlign.CENTER),
        bgcolor="#E3EBF1", border_radius=10, padding=12, on_click=lambda _: mostrar_seccion("inicio")),
        ft.Divider(height=35),
        boton_lateral("CONTACTOS", ft.Icons.PERSON, "contactos"),
        boton_lateral("EXPORTAR", ft.Icons.DOWNLOAD, "exportar"),
        boton_lateral("HERRAMIENTAS", ft.Icons.BUILD, "herramientas"),
        boton_lateral("AYUDA", ft.Icons.HELP, "ayuda")
    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=15, expand=True),
    width=240, padding=20, bgcolor=fondo, border=ft.Border(right=ft.BorderSide(1, "#D7E0E7")))

    panel_principal = ft.Container(content=ft.Column(controls=[barra_superior, ft.Container(content=contenido, alignment=ft.Alignment(0, -1), padding=ft.Padding(0, 40, 0, 0), expand=True)],
    spacing=0, expand=True), bgcolor=fondo, padding=12, expand=True)

    page.add(ft.Row(controls=[panel_lateral, panel_principal], spacing=0, expand=True, vertical_alignment=ft.CrossAxisAlignment.STRETCH))
