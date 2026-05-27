import flet as ft
import  sqlite3

class Vistalogin(ft.View):
        def __init__(self,page:ft.Page):
                super().__init__(
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        padding=ft.padding.only(top =30),
                        bgcolor=ft.Colors.WHITE,
                        route="/login"
                )
                self.login = page
                self.usuario = ft.TextField(label = 'Usuario',width=200,border_color=ft.Colors.BLUE,
                icon = ft.Icons.PERSON)
        
                self.contrasenya = ft.TextField(label = 'Contraseña',width=200,border_color=ft.Colors.BLUE,password=True,
                can_reveal_password=True,icon = ft.Icons.PASSWORD, )
        
                self.logo = ft.Image(src='/transparent-logo.png',width=300,height=300)

                self.btnlog = ft.Button(content="Iniciar Sesion",style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),on_click=self.button_clicked)

                self.mensaje = ft.Text(value= 'Bienvenid@ introduzca sus credenciales para acceder', size=30, color=ft.Colors.BLUE_300,text_align=ft.TextAlign.CENTER, weight=ft.FontWeight.BOLD)

                self.controls = [
                        self.mensaje,self.logo,ft.Divider(height=20,color='transparent'),self.usuario,ft.Divider(height=20,color='transparent'),self.contrasenya,ft.Divider(height=20,color='transparent'),self.btnlog
                ]

        async def button_clicked(self,e):
                conexion = sqlite3.connect('SIC.DB')
                valor_usuario = self.usuario.value
                valor_contrasenya = self.contrasenya.value
                cursor = conexion.execute(f"SELECT contrasenya, rol FROM TBL_USUARIOS WHERE usuario_id = '{valor_usuario}'")
                fila = cursor.fetchone()

                if fila is not None:
                        contrasenya = fila[0]
                        rol = fila[1]

                        if valor_contrasenya == contrasenya:
                                if rol =="admin":
                                        await self.page.push_route("/admin")
                                elif rol == 'recepcion':
                                        await self.page.push_route("/recepcionista")
                                elif rol =='mecanico':
                                        await self.page.push_route("/mecanico")
                        else:
                                self.mensaje.value ="Contraseña incorrecta"

                conexion.close()
                self.page.update()
