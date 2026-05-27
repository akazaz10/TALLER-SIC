import flet as ft
import controlador
from V_factura import datos_factura
# import controlador
# from V_factura import datos_factura


def caja_textor_registro(nombre, campo_texto):

    caja = ft.Column(
                controls = [
                    ft.Text(nombre, color = "black", weight = ft.FontWeight.BOLD),
                    campo_texto
                    ],
                spacing = 5
    )
    return caja

def centrar_celdas(mi_celda, mi_color):

    texto = str(mi_celda)

    return ft.DataCell(ft.Container(content = ft.Text(texto, color = mi_color), alignment = ft.Alignment.CENTER))


class VistaRecepcion(ft.View):

    def __init__(self, page:ft.Page):
##################################################################################################################################################################################################
        panel_grid = ft.ResponsiveRow(
            spacing = 30,
            run_spacing = 20,
            controls = [
            Body("Citas del día", columnas={"sm": 6}, contenido = ContenidoCitas()),
            Body("Mecánicos disponibles", columnas={"sm": 6}, contenido = MecanicosDisponibles()),
            Body("Registro rápido", columnas={"sm":6}, contenido = ContenidoRegistro()),
            ft.Column(col = {"sm": 6},controls = [Body("Facturas", columnas={"sm":6}, contenido = Facturas()), Body("Eliminar Ticket", columnas={"sm": 6}, contenido = Eliminacion())])]
        )
##################################################################################################################################################################################################
        super().__init__(
            route="/recepcionista",
            padding=30,
            spacing=0,
            scroll=ft.ScrollMode.AUTO, #PROVISIONAL
            appbar = Header(),
            controls=[panel_grid]
        )
        self.recepcionista = page

# ******************************************************************

class Header(ft.AppBar):

    def __init__(self):
        super().__init__()

        self.toolbar_height = 70
        self.shape = ft.RoundedRectangleBorder(radius = 10)
        self.leading = ft.Image(src = "/logomec.png", width = 40, height = 40,)
        self.title = ft.Text("Bienvenido/a, Recepcionista", size = 20)
        self.center_title = True
        self.bgcolor = ft.Colors.SURFACE_CONTAINER
        self.actions = [
            ft.IconButton(icon = ft.Icons.REFRESH, on_click = self.refresh),
            ft.PopupMenuButton(
                            menu_position = ft.PopupMenuPosition.UNDER,
                            items = [
                                ft.PopupMenuItem(content = "Cerrar Sesión", on_click=self.cerrarSesion)
                            ]
                        ),
                    ]

    def refresh(self, e):
        self.page.views.clear()
        self.page.views.append(VistaRecepcion(self.page))
        self.page.update()

    def cerrarSesion(self, e):
        self.page.go("/login")

class Body(ft.Container):

    def __init__(self, nombre, columnas, contenido = None):
        super().__init__()
        self.nombre = nombre
        self.col = columnas
        self.border_radius = 10
        self.bgcolor = "white"
        self.padding = 20
        self.content = ft.Column(controls = [ft.Text(self.nombre, weight = ft.FontWeight.BOLD, color = "black"), contenido if contenido else ft.Container()])

class ContenidoRegistro(ft.Column):
    def __init__(self):
        super().__init__()
        #--------------------------------------------------------------------------------------------------------------------------------------------------
        self.dni = ft.TextField(label="Introduce el DNI", height=40, color="black")
        self.nombre = ft.TextField(label="Introduce el nombre", height=40, color="black")
        self.apellido = ft.TextField(label="Introduce el apellido", height=40, color="black")
        self.matricula = ft.TextField(label="Introduce la matrícula", height=40, color="black")
        self.marca = ft.TextField(label="Introduce la marca del coche", height=40, color="black")
        self.modelo = ft.TextField(label="Modelo", height=40, color="black")
        self.anio = ft.TextField(label="Año", height=40, color="black")
        self.observaciones = ft.TextField(label="Introduce las incidencias", multiline=True, min_lines=3, max_lines=5, color="black")
        self.mecanico = ft.TextField(label="Introduce el mecánico", height=40, color="black")

        self.mensaje_mecanico = ft.Text("", size = 12, weight = ft.FontWeight.BOLD, color = "black")
        self.mensaje_general = ft.Text("", size = 16, weight = ft.FontWeight.BOLD, color = "red")
        #--------------------------------------------------------------------------------------------------------------------------------------------------

        caja_interna_izquierda = ft.Container(
            bgcolor = "white",
            padding = 10,
            expand = 1,
            content = ft.Column(
                controls = [
                        caja_textor_registro("DNI", self.dni),
                        caja_textor_registro("Nombre", self.nombre), #ft.Text("Nombre", color = "black", weight = ft.FontWeight.BOLD),ft.TextField(label = "Introduce el nombre del Cliente", height = 40, color = "black"),
                        caja_textor_registro("Apellido", self.apellido),#ft.Text("Número de Teléfono", color = "black", weight = ft.FontWeight.BOLD),ft.TextField(label = "Nombre del Cliente", height = 40, color = "black"),
                ], spacing = 10
            )
        )

        caja_interna_derecha = ft.Container(
            bgcolor = "white",
            padding = 10,
            expand = 1,
            content = ft.Column(
                controls = [
                        caja_textor_registro("Matrícula", self.matricula),#ft.Text("Dirección", color = "black", weight = ft.FontWeight.BOLD), ft.TextField(label = "Nombre del Cliente", height = 40, color = "black"),
                        caja_textor_registro("Marca", self.marca),#ft.Text("Apellido", color = "black", weight = ft.FontWeight.BOLD), ft.TextField(label = "Nombre del Cliente", height = 40, color = "black"),
                        ft.Row(controls = [ft.Container(caja_textor_registro("Modelo", self.modelo), expand = 1), ft.Container(caja_textor_registro("Año", self.anio), expand = 1)])
                ], spacing = 10
            )
        )

        fila_superior = ft.Row(controls = [caja_interna_izquierda, caja_interna_derecha])
#--BOTON COMPROBACION--------------------------------------------------------------------------------------------------------------------------------------
        self.btn_comprobar = ft.Button(
                            content=ft.Text("Comprobar Mecánico"),
                            bgcolor=ft.Colors.BLUE_500,
                            color="white",
                            on_click = self.comprobar_disponibilidad_mecanico
                        )
#----------------------------------------------------------------------------------------------------------------------------------------------------------
        caja_interna_inferior = ft.Container(
            bgcolor="white",
            padding=10,
            expand=1,
            content=ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Container(
                                ft.Column(controls = [caja_textor_registro("Observaciones",self.observaciones), self.mensaje_general]), expand=2
                            ),
                            ft.Container(
                                ft.Column(
                                    controls=[
                                        caja_textor_registro("Mecánico", self.mecanico),
                                        self.mensaje_mecanico,
                                        ft.Container(
                                            ft.Row(alignment=ft.MainAxisAlignment.CENTER, controls=[self.btn_comprobar])
                                        ),
                                    ],
                                    spacing=20,
                                ),
                                expand=1,
                            ),
                        ],
                    )
                ],
                spacing=10,
            ),
        )

        fila_inferior = ft.Row(controls = [caja_interna_inferior])

#--BOTON CAMBIANTE REGISTRO--------------------------------------------------------------------------------------------------------------------------------------
        self.btn_regitrar = ft.Button(
            content = ft.Text("Registrar datos"),
            bgcolor = ft.Colors.GREY_300,
            color = "black",
            disabled = True,
            on_click = self.comprobar_disponibilidad_registro
        )

        fila_boton = ft.Row(alignment = ft.MainAxisAlignment.CENTER, controls = [self.btn_regitrar])
#---------------------------------------------------------------------------------------------------------------------------------------------------------------
        # PARA EL CONTROL PRINCIPAL
        self.controls = [ft.Text("Datos de ingreso", weight=ft.FontWeight.W_500, color = "black"), fila_superior, fila_inferior, fila_boton]
#---------------------------------------------------------------------------------------------------------------------------------------------------------------

    def comprobar_disponibilidad_mecanico(self, e):

        id = self.mecanico.value

        if not id:
            self.mensaje_mecanico.value = f"Introduce un ID"
            return

        lista = controlador.obtener_mecanicos_activos()

        for mecanico in lista:
            if mecanico[0] == id:
                if mecanico[4] == 'Disponible':
                    self.mensaje_mecanico.value = f"Mecánico {id} disponible"
                    self.btn_regitrar.disabled = False
                    self.btn_regitrar.bgcolor = ft.Colors.GREEN_800
                    self.btn_regitrar.color = "white"
                    self.page.update()
                    return

                else:
                    self.mensaje_mecanico.value = f"Mecánico {id} saturado"
                    self.btn_regitrar.disabled = True
                    self.btn_regitrar.bgcolor = ft.Colors.GREY_300
                    self.btn_regitrar.color = "black"
                    self.page.update()
                    return

        self.mensaje_mecanico.value = f"El mecánico {id} no existe."
        self.btn_regitrar.disabled = True
        self.btn_regitrar.bgcolor = ft.Colors.GREY_300
        self.btn_regitrar.color = "black"
        self.page.update()

    def comprobar_disponibilidad_registro(self, e):

        datos_registro = {
            "dni": self.dni.value,
            "nombre": self.nombre.value,
            "apellido": self.apellido.value,
            "matricula": self.matricula.value,
            "marca": self.marca.value,
            "modelo": self.modelo.value,
            "anio": self.anio.value,
            "observaciones": self.observaciones.value,
            "id_mecanico": self.mecanico.value
        }

        es_correcto = True

        for datos in datos_registro.values():

            if not datos:
                es_correcto = False

        if es_correcto:

            self.btn_regitrar.disabled = True
            self.btn_regitrar.bgcolor = ft.Colors.GREY_300
            self.btn_regitrar.color = "black"
            registro = controlador.registrar_nuevo_ticket(datos_registro)

            if registro:
                self.mensaje_general.value = "DATOS INGRESADOS CORRECTAMENTE"
                self.mensaje_general.color = "green"

                self.dni.value = ""
                self.nombre.value = ""
                self.apellido.value = ""
                self.matricula.value = ""
                self.marca.value = ""
                self.modelo.value = ""
                self.anio.value = ""
                self.mecanico.value = ""
                self.observaciones.value = ""

            self.page.update()
            return

        else:

            self.mensaje_general.value = f"UNO O MÁS CAMPOS ESTÁN VACÍOS"
            self.mensaje_general.color = "red"

            self.page.update()
            return

class ContenidoCitas(ft.Column):
    def __init__(self):
        super().__init__()

        datos_reales = controlador.obtener_citas_activas()

        filas_dinamicas = []

        for cita in datos_reales:
            nueva_fila = ft.DataRow(
                cells = [
                    centrar_celdas(cita[0], "black"),
                    centrar_celdas(cita[1], "black"),
                    centrar_celdas(cita[2], "black"),
                    centrar_celdas(cita[3], "black"),
                    centrar_celdas(cita[4], "black"),
                    centrar_celdas(cita[5], "black")
                ]
            )

            filas_dinamicas.append(nueva_fila)

        self.tabla = ft.DataTable(
            border = ft.Border.all(1, "grey"),
            border_radius = 10,
            heading_row_color = ft.Colors.BLACK_12,
            columns = [
                ft.DataColumn(label = ft.Text("Número de ticket", color = "black", weight = ft.FontWeight.BOLD)),
                ft.DataColumn(label = ft.Text("Nombre", color = "black", weight = ft.FontWeight.BOLD)),
                ft.DataColumn(label = ft.Text("Apellido", color = "black", weight = ft.FontWeight.BOLD)),
                ft.DataColumn(label = ft.Text("Matrícula", color = "black", weight = ft.FontWeight.BOLD)),
                ft.DataColumn(label = ft.Text("Fecha de entrada", color = "black", weight = ft.FontWeight.BOLD)),
                ft.DataColumn(label = ft.Text("Fecha de salida", color = "black", weight = ft.FontWeight.BOLD))
            ],
            rows = filas_dinamicas
        )

        # HACE POSIBLE EL SCROLL EN EL EJE Y

        scroll_vertical = ft.Column(controls = [self.tabla], scroll = ft.ScrollMode.AUTO)

        caja_limitada = ft.Container(height = 300, content = scroll_vertical)

        # HACE POSIBLE EL SCROLL EN EL EJE X

        self.controls = [ft.Row(controls = [caja_limitada], scroll = ft.ScrollMode.AUTO)]

class MecanicosDisponibles(ft.Column):

    def __init__(self):
        super().__init__()

        datos_reales = controlador.obtener_mecanicos_activos()

        filas_dinamicas = []

        for mecanico in datos_reales:
            nueva_fila = ft.DataRow(
                cells = [
                    centrar_celdas(mecanico[0], "black"),
                    centrar_celdas(mecanico[1], "black"),
                    centrar_celdas(mecanico[2], "black"),
                    centrar_celdas(mecanico[3], "black"),
                    centrar_celdas(mecanico[4], "black")
                ]
            )

            filas_dinamicas.append(nueva_fila)

        self.tabla = ft.DataTable(
            border = ft.Border.all(1, "grey"),
            border_radius = 10,
            heading_row_color = ft.Colors.BLACK_12,
            columns = [
                ft.DataColumn(label = ft.Text("Identificador", color = "black", weight = ft.FontWeight.BOLD)),
                ft.DataColumn(label = ft.Text("Nombre", color = "black", weight = ft.FontWeight.BOLD)),
                ft.DataColumn(label = ft.Text("Apellido", color = "black", weight = ft.FontWeight.BOLD)),
                ft.DataColumn(label = ft.Text("Tickets abiertos", color = "black", weight = ft.FontWeight.BOLD)),
                ft.DataColumn(label = ft.Text("Disponible", color = "black", weight = ft.FontWeight.BOLD))

            ],
            rows = filas_dinamicas
        )

        scroll_vertical = ft.Column(controls = [self.tabla], scroll = ft.ScrollMode.AUTO)

        caja_limitada = ft.Container(height = 300, content = scroll_vertical)

        self.controls = [ft.Row(controls = [caja_limitada], scroll = ft.ScrollMode.AUTO)]

class Facturas(ft.Column):

    def __init__(self):
        super().__init__()
        self.ticket_id = ft.TextField(label = "ID de Ticket", color = "black")
        self.btn_gemerarfactura = ft.Button(content = ft.Text("Generar Factura"), on_click = self.generar)
        self.factura_creada = ft.Text("", size = 12, color = "black", weight=ft.FontWeight.W_500)
        self.controls = [
            ft.Text("Escribe el número de ticket para generar la factura ", weight=ft.FontWeight.W_500, color = "black"),
            ft.Row(controls = [self.ticket_id, self.btn_gemerarfactura], spacing = 10),
            self.factura_creada
        ]

    def generar(self, e):
        valor = self.ticket_id.value

##################################################################################################################################################################################################
        if valor.isdigit():
            resultado = controlador.obtener_fecha_cita(valor)
            if resultado == "CERRADO":
                datos_factura(int(valor))
                self.factura_creada.value = f"Factura nº {valor} generada"
            elif resultado == "ABIERTO":
                self.factura_creada.value = f"Ticket {valor} aún no ha sido cerrado"
            elif resultado == "No existe":
                self.factura_creada.value = f"Ticket {valor} no existe"

        else:
            self.factura_creada.value = "Formato incorrecto"

        self.page.update()

class Eliminacion(ft.Column):
    def __init__(self):
        super().__init__()
        self.ticket_id = ft.TextField(label = "ID de Ticket", color = "black")
        self.btn_eliminarticket = ft.Button(content = ft.Text("Eliminar Ticket"), on_click = self.eliminar)
        self.ticket_eliminado = ft.Text("", size = 12, color = "black", weight=ft.FontWeight.W_500)
        self.controls = [
            ft.Text("Escribe el número de ticket para eliminarlo del historial ", weight=ft.FontWeight.W_500, color = "black"),
            ft.Row(controls = [self.ticket_id, self.btn_eliminarticket], spacing = 10),
            self.ticket_eliminado
        ]

    def eliminar(self, e):
        valor = self.ticket_id.value

        if valor.isdigit():
            resultado = controlador.obtener_fecha_cita(valor)
            if resultado == "CERRADO":
                controlador.eliminar_ticket(int(valor))
                self.ticket_eliminado.value = f"Ticket {valor} eliminado con éxito"
            elif resultado == "ABIERTO":
                self.ticket_eliminado.value = f"Ticket {valor} aún no ha sido cerrado"
            elif resultado == "No existe":
                self.ticket_eliminado.value = f"Ticket {valor} no existe"

        else:
            self.ticket_eliminado.value = "Formato incorrecto"

        self.page.update()
##################################################################################################################################################################################################

#******************************************************************

def vista_recepcion(page: ft.Page):

    page.views.clear()
    page.views.append(VistaRecepcion(page))
    page.update()


if __name__ == "__main__":
    ft.run(main = vista_recepcion, assets_dir = "assets")