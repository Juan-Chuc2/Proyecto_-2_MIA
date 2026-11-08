import flet as ft
from src.Modelos.contactos import Contacto
from src.Servicios.contactos import registrar_contacto, modificar_contacto
from src.Repositorio.indice import buscar_por_id
from src.Reportes.exportarJson import exportar_json
from src.Reportes.reportePDF import generar_pdf

def ventana_principal(page: ft.Page):
    page.title, page.window.maximized = "Agenda de Contactos", True
    id_c, nombre, telefono, correo, ciudad = ft.TextField(label="ID"), ft.TextField(label="Nombre"), ft.TextField(label="Teléfono"), ft.TextField(label="Correo"), ft.TextField(label="Ciudad")
    mensaje, id_buscar, resultado_busqueda = ft.Text(), ft.TextField(label="ID del contacto"), ft.Text()
    id_modificar, nombre_modificar, telefono_modificar, correo_modificar, ciudad_modificar, mensaje_modificar = ft.TextField(label="ID del contacto"), ft.TextField(label="Nombre"), ft.TextField(label="Teléfono"), ft.TextField(label="Correo"), ft.TextField(label="Ciudad"), ft.Text()
    campos_modificar = [nombre_modificar, telefono_modificar, correo_modificar, ciudad_modificar]
    mensaje_exportar = ft.Text()

    def guardar_contacto(e):
        campos = [id_c, nombre, telefono, correo, ciudad]
        if not all(c.value for c in campos): mensaje.value = "Debe completar todos los campos."
        elif not id_c.value.isdigit(): mensaje.value = "El ID debe ser un número entero."
        elif registrar_contacto(Contacto(int(id_c.value), nombre.value, telefono.value, correo.value, ciudad.value)):
            mensaje.value = "Contacto registrado correctamente."
            for c in campos: c.value = ""
        else: mensaje.value = "Error No se pudo registrar, verifique el ID y tamaños permitidos."
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
        mensaje_exportar.value = "Contactos exportados correctamente a la carpeta  exportaciones, nombre del archivo:contactos.json" if exportar_json() else "No se pudieron exportar los contactos."
        page.update()

    def generar__pdf(e):
        if generar_pdf():
            mensaje_exportar.value = "Reporte PDF generado correctamente esta en carpeta: exportaciones archivo:reporte_contactos.pdf"
        else:
            mensaje_exportar.value = "No se pudo generar el reporte PDF."

        page.update()

    formulario = ft.Column(controls=[ft.Text("AGREGAR CONTACTO", size=22, weight=ft.FontWeight.BOLD), id_c, nombre, telefono, correo, ciudad, ft.Button("Guardar contacto", on_click=guardar_contacto), mensaje], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=15, width=400, visible=False)
    formulario_busqueda = ft.Column(controls=[ft.Text("BUSCAR CONTACTO", size=22, weight=ft.FontWeight.BOLD), id_buscar, ft.Button("Buscar", on_click=buscar_contacto), resultado_busqueda], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=15, width=400, visible=False)

    for campo in campos_modificar: campo.disabled = True
    boton_guardar_cambios = ft.Button("Guardar cambios", on_click=guardar_cambios, disabled=True)

    formulario_modificar = ft.Column(controls=[ft.Text("MODIFICAR CONTACTO", size=22, weight=ft.FontWeight.BOLD), id_modificar, ft.Button("Buscar", on_click=buscar_para_modificar), nombre_modificar, telefono_modificar, correo_modificar, ciudad_modificar, boton_guardar_cambios, mensaje_modificar],
    horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=15, width=400, visible=False)
    formulario_exportar = ft.Column(controls=[ft.Text("EXPORTAR CONTACTOS",size=22,weight=ft.FontWeight.BOLD),ft.Button("Exportar a JSON", on_click=exportar_contactos),
    ft.Button("Generar reporte PDF", on_click=generar__pdf),mensaje_exportar],horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    spacing=15,width=400,visible=False)

    def mostrar_seccion(seccion):
        formulario.visible, formulario_busqueda.visible, formulario_modificar.visible, formulario_exportar.visible = seccion == "agregar", seccion == "buscar", seccion == "modificar", seccion == "exportar"
        page.update()

    page.add(ft.Column(controls=[ft.Text("AGENDA DE CONTACTOS", size=28, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER), ft.Divider(), ft.Row(controls=[ft.Button("Contactos", on_click=lambda _: mostrar_seccion("agregar")), ft.Button("Buscar contacto", on_click=lambda _: mostrar_seccion("buscar")),
    ft.Button("Modificar contacto", on_click=lambda _: mostrar_seccion("modificar")), ft.Button("Exportar", on_click=lambda _: mostrar_seccion("exportar")), ft.Button("Herramientas"), ft.Button("Ayuda")], alignment=ft.MainAxisAlignment.CENTER, spacing=15, wrap=True), formulario, formulario_busqueda, formulario_modificar, formulario_exportar],
    horizontal_alignment=ft.CrossAxisAlignment.CENTER, scroll=ft.ScrollMode.AUTO, expand=True))