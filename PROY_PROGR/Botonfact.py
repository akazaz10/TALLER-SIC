import flet as ft
from V_factura import datos_factura
ticket_id = ft.TextField(label="Ticket ID", width=200)

def generar_factura(e):
    factura_ticket_id = ticket_id.value
    datos_factura(int(factura_ticket_id))
    
botonfactura = ft.ElevatedButton(Text="Genera Factura",on_click=generar_factura)
