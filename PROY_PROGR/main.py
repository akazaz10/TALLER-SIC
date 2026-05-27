import flet as ft
from V_login import Vistalogin
from V_mecanico import Vistamecanico
from V_recepcion import VistaRecepcion

async def main(page:ft.Page):
    page.title = "Taller SIC"
   

    async def route_change(route):
        page.views.clear()
        if page.route == "/login":
            page.views.append(Vistalogin(page))
        elif page.route == "/mecanico":
            page.views.append(Vistamecanico(page))
        elif page.route == "/recepcionista":
            page.views.append(VistaRecepcion(page))
    
        page.update()

    page.on_route_change = route_change
    await page.push_route("/login")

if __name__ == "__main__":
    ft.run(main, assets_dir=".")

    '''elif page.route == "/jefe":
            page.views.append(Vistajefe(page))'''
    '''elif page.route == "/recepcion":
            page.views.append(Vistarecepcion(page))'''