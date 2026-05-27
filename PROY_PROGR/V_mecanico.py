import flet as ft 
import sqlite3
conexion = sqlite3.connect('SIC.DB')
conexion.execute("PRAGMA foreign_keys = ON;")
cursor = conexion.cursor()  

class Vistamecanico(ft.View):
    def __init__(self, page:ft.Page):
        super().__init__(
            route="/mecanico",
            padding=0,
            spacing=0,
            controls=[
                Header(),
                body()
            ]
        )
        self.mecanico = page



class Header(ft.AppBar):

    def __init__(self):
        super().__init__()
        
        self.toolbar_height = 70
        self.shape = ft.RoundedRectangleBorder(
            radius = 10
        )
        self.leading = ft.Image(
            src = "/logomec.png",
            width = 60,
            height = 60,
        )
        self.title = ft.Text(
            "Bienvenido/a, Mecanico",
            size = 20
            )

        self.center_title = True
        self.bgcolor = ft.Colors.SURFACE_CONTAINER
        self.actions = [
            ft.IconButton(icon = ft.Icons.REFRESH, on_click = self.refresh),
            ft.PopupMenuButton(
                            menu_position = ft.PopupMenuPosition.UNDER,
                            icon=ft.Icons.NOTIFICATIONS,
                            items = [
                                ft.PopupMenuItem(content = ft.Text("Actualmente no posees notificaciones")),
                            ]
            ),
            ft.PopupMenuButton(
                            menu_position = ft.PopupMenuPosition.UNDER,
                            items = [
                                ft.PopupMenuItem(content = "Información de Usuario"),
                                ft.PopupMenuItem(),  
                                ft.PopupMenuItem(content= "Cerrar sesion", on_click=self.cerrarsesion)
                            ]
                        ),
                    ]
    def refresh(self,e):
        self.page.views.clear()
        self.page.views.append(Vistamecanico(self.page))
        self.page.update()
        
    def cerrarsesion(self,e):
        self.page.go("/login")

class body(ft.Container):
    def __init__(self):
        super().__init__()
        self.bgcolor = "grey"
        self.expand = True
        self.alignment = ft.Alignment(-1, -1)
        self.padding = 10
        self.content = ft.Row(
            vertical_alignment=ft.CrossAxisAlignment.START,
            controls=[
                ft.Column(
                    scroll=ft.ScrollMode.AUTO,
                    spacing=10,
                    expand = 3,
                    alignment=ft.MainAxisAlignment.START,
                    controls= self.Registro()             
                ),
                ft.Column(
                    scroll=ft.ScrollMode.AUTO,
                    expand=1,
                    alignment=ft.MainAxisAlignment.CENTER,
                    controls = [
                        self.Servicios(),
                        self.Partes()
                    ]
                ) 
            ]
        )
                    
    def Anadir_coche(self):
        cursor.execute( "SELECT " \
                            "ST.service_ticket_id, " \
                            " ST.car_id," \
                            " ST.customer_id," \
                            " ST.date_received," \
                            " C.brand," \
                            " C.model, " \
                            " SM.mechanic_id " \
                        " FROM TBL_SERVICE_TICKETS AS ST " \
                        " INNER JOIN TBL_CARS AS C " \
                            " ON ST.car_id = C.car_id " \
                        " INNER JOIN TBL_SERVICE_MECHANICS  SM" \
                            " ON SM.service_ticket_id = ST.service_ticket_id " \
                            "WHERE date_returned IS NULL " \
                                )
        rows = cursor.fetchall()
        return rows
    
    def Select_Servicios(self):
        cursor.execute( "SELECT " \
            "service_id, " \
            "service_name, " \
            "hourly_rate " \
            "FROM TBL_SERVICES " 
        )
        rows = cursor.fetchall()
        return rows
    
    def Select_Partes(self):
        cursor.execute("SELECT " \
            "part_id, " \
            "descripcion," \
            "retail_price " \
            "FROM TBL_PARTS"
        )
        rows = cursor.fetchall()
        return rows
    

    def Select_Mecanico(self):
        cursor.execute("SELECT " \
            "mechanic_id " 
            "FROM TBL_MECHANICS"
        )
        rows = cursor.fetchall()
        return rows



    def Partes(self):
        select = self.Select_Partes()
        elementos_texto = []
        elementos_texto.append(ft.Text(f"PARTES", color="black",weight="bold"))
        for fila in select:
            id_servicio = fila[0]
            servicio = fila[1]
            partes_precio = fila[2] 
            texto = ft.Text(f" {id_servicio}: {servicio} {partes_precio} ", color="black")
            elementos_texto.append(texto)
            
        contenedor_unico = ft.Container(
            width=float("inf"),
            border_radius=12,
            padding=7,
            bgcolor="white",
            content=ft.Column(
                controls=elementos_texto 
            )
        )
        return contenedor_unico
    

    
    def Servicios(self):
        select = self.Select_Servicios()
        
        elementos_texto = []
        elementos_texto.append(ft.Text(f"SERVICIOS", color="black", weight="bold"))
        for fila in select:
            id_servicio = fila[0]
            servicio = fila[1]
            precio = fila[2]
            
            texto = ft.Text(f" {id_servicio}: {servicio} {precio}", color="black")
            elementos_texto.append(texto)
            
        contenedor_unico = ft.Container(
            width=float("inf"),
            border_radius=12,
            padding=7,
            bgcolor="white",
            content=ft.Column(
                controls= elementos_texto 
            )
        )
        
        return contenedor_unico
        

    def finalizar(self, e, datos):

        def mostrar_error(mensaje_error):
            def cerrar_alerta(ev):
                alerta.open = False 
                self.page.update()  

            alerta = ft.AlertDialog(
                title=ft.Text("ERROR DE VALIDACIÓN"),
                content=ft.Text(mensaje_error),
                actions=[ft.TextButton("Cerrar", on_click=cerrar_alerta)],
                open=True,
            )
            self.page.overlay.append(alerta)
            self.page.update()

        if not datos["ticket"] or not datos["mecanico"].value or not datos["servicios"].value or not datos["horas"].value or not datos["comentarios"].value \
            or not datos["rate"].value or not  datos["fecha_regreso"].value or not datos["precio_pieza"].value or not datos["parts_used"].value or not datos["id_partes"].value:
            mostrar_error("Por favor, rellene todos los campos.")
            return

        if not datos["servicios"].value.isdigit():
            mostrar_error("El campo ID Servicio debe ser un numero entero. El ID esta indicado en la parte Servicios")
            return

        if not datos["parts_used"].value.isdigit():
            mostrar_error("El campo Cantidad Piezas usadas ser un numero entero.")
            return
        
        if not datos["id_partes"].value.isdigit():
            mostrar_error("El campo ID Parte ser un numero entero. El ID esta indicado en la parte Partes")
            return
        
        if not datos["horas"].value.replace('.', '', 1).isdigit():
            mostrar_error("El campo Horas de servicio debe ser un numero decimal.")
            return

        if not datos["rate"].value.replace('.', '', 1).isdigit():
            mostrar_error("El campo Precio de servicio debe ser decimal. Esta indicado en el parte de Servicios")
            return
        
        if not datos["precio_pieza"].value.replace('.', '', 1).isdigit():
            mostrar_error("El campo Precio Parte debe ser un número decimal.Esta indicado en el parte de Partes")
            return
        

        registro = (
            int(datos["ticket"]),                 
            int(datos["servicios"].value),        
            datos["mecanico"].value,              
            float(datos["horas"].value),          
            datos["comentarios"].value,           
            float(datos["rate"].value),
            datos["fecha_regreso"].value,
            float(datos["precio_pieza"].value),  
            (datos["parts_used"].value),
            (datos["id_partes"].value)  
        )

        try:

            cursor.execute("""
                INSERT INTO TBL_PARTS_USED(
                    part_id,
                    service_ticket_id,       
                    number_used,
                    price
                    ) VALUES (?,?,?,?)
                """,(datos["id_partes"].value, datos["ticket"], datos["parts_used"].value, datos["precio_pieza"].value))
        
            cursor.execute("""
                UPDATE TBL_SERVICE_MECHANICS 
                    SET service_id = ?,
                    hours = ?,
                    comments = ?,
                    rate = ?
                    WHERE service_ticket_id = ?
                    """, (datos["servicios"].value, datos["horas"].value, datos["comentarios"].value,datos["rate"].value,datos["ticket"]
                ))

#---------------------------------------------------------------------
            cursor.execute("""
                SELECT sm.mechanic_id 
                    FROM TBL_SERVICE_MECHANICS sm
                    INNER JOIN TBL_SERVICE_TICKETS st
                    ON st.service_ticket_id = sm.service_ticket_id
                    WHERE st.service_ticket_id = ?
                    """, (datos["ticket"],))

            resultado = cursor.fetchone()
            st_mecanico = resultado[0]


            if datos["mecanico"].value != st_mecanico:

                def cerrar(e):
                    alerta.open = False 
                    self.page.update()  

                alerta = ft.AlertDialog(
                title=ft.Text("ERROR"),
                content=ft.Text(f"Mecánico incorrecto, introduce el mecanico asignado"),
                actions=[ft.TextButton("Cerrar", on_click = cerrar)],
                open=True,
                )
    
                self.page.overlay.append(alerta)
                self.page.update()                
                conexion.rollback()


            else:

                cursor.execute("""
                    UPDATE TBL_SERVICE_TICKETS
                    SET date_returned = ?
                    WHERE service_ticket_id = ?
                """, (datos["fecha_regreso"].value, datos["ticket"]))
#---------------------------------------------------------------------

            e.control.style = ft.ButtonStyle(
                bgcolor={ft.ControlState.DEFAULT: "green"}
            )
            e.control.update()
            self.page.views.clear()
            self.page.views.append(Vistamecanico(self.page))
            self.page.update()

            conexion.commit()

        except sqlite3.Error as e:
            print('Error: ', e)
            conexion.rollback()
    

    def make_finalizar(self, datos):
        return lambda e: self.finalizar(e, datos)


    def Registro(self):
        select = self.Anadir_coche()
        contenedores = []
        for i in range(len(select)):
            # datos de entrada
            Servicios = ft.TextField( width=150, height= 20, content_padding=0, text_style=ft.TextStyle(size=10, color="black"))
            Partes = ft.TextField( width=150, height= 20, content_padding=0, text_style=ft.TextStyle(size=10, color="black"))
            fecha_regreso = ft.TextField( width=150, height= 20, content_padding=0, text_style=ft.TextStyle(size=10, color="black"))
            comentarios = ft.TextField(width=150, height= 20, content_padding=0, text_style=ft.TextStyle(size=10, color="black"))
            horas = ft.TextField(width=150, height= 20, content_padding=0, text_style=ft.TextStyle(size=10, color="black"))
            mecanico = ft.TextField(width=150, height= 20, content_padding=0, text_style=ft.TextStyle(size=10, color="black"))
            rate = ft.TextField(width=150, height= 20, content_padding=0, text_style=ft.TextStyle(size=10, color="black"))
            precio_pieza = ft.TextField(width=150, height= 20, content_padding=0, text_style=ft.TextStyle(size=10, color="black"))
            parts_used = ft.TextField(width=150, height= 20, content_padding=0, text_style=ft.TextStyle(size=10, color="black"))
            button = ft.ElevatedButton("Finalizar")
            for j in range(len(select[i])):
                if j == 0:
                    ticket = select[i][j]
                elif j == 4:
                    marca = select[i][j]
                elif j == 5:
                    modelo = select[i][j]
                elif j == 1:
                    matricula = select[i][j]
                elif j == 3:
                    fecha = select[i][j]
                elif j == 6:
                    nombre_mecanico = select[i][j]

            datos = {
                "ticket": ticket,
                "servicios": Servicios,
                "mecanico": mecanico,  
                "horas": horas,
                "comentarios": comentarios,
                "rate": rate,
                "fecha_regreso": fecha_regreso,
                "precio_pieza": precio_pieza,
                "parts_used":parts_used,
                "id_partes":Partes
            }

            button.on_click = self.make_finalizar(datos)          

            contenedor = ft.Container(
                width= float("inf"),
                height = 230,
                border_radius=15,
                padding=7,
                bgcolor = "white",
                content= ft.Row(
                    controls=[
                        ft.Column(
                            expand= 2,
                            controls=[
                                ft.Text(f"Coche y matrícula: {marca} {modelo} {matricula}", color= "black",weight='BOLD'), #funcion conectar service_ticket
                                ft.Text("ID Servicio a realizar", color="black"),
                                Servicios,
                                ft.Text("ID Parte", color="black"),
                                Partes,
                                ft.Text("Precio parte", color="black"),
                                precio_pieza
                            ]
                        ),
                        ft.Column(
                            expand= 2,
                            controls=[
                                ft.Text(f"Fecha recibido: {fecha}", color= "black",weight='BOLD'), #funcion conectar service_ticket
                                ft.Text("Fecha de entrega", color="black"),
                                fecha_regreso,
                                ft.Text("Comentarios", color="black"),
                                comentarios,
                                ft.Text("Cantidad Piezas Usadas", color="black"),
                                parts_used

                            ]
                        ),
                        ft.Column(
                            expand= 1,
                            controls=[
                                ft.Text(f"Mecanico asign: {nombre_mecanico} ", color= "black",weight='BOLD'),
                                ft.Text("Horas de servicio", color="black"),
                                horas,
                                ft.Text("ID Mecanico", color="black"),
                                mecanico,
                                ft.Text("Precio de Servicio", color="black"),
                                rate
                            ]
                        ),
                        button                       
                    ]
                )
            )
            contenedores.append(contenedor)
        return contenedores