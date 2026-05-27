import sqlite3
from fpdf import FPDF

def datos_factura(ticket_id):
    conexion = sqlite3.connect('SIC.DB')
    conexion.execute("PRAGMA foreign_keys = ON;") #ESTO SE PONE PORQUE POR DEFECTO SQLITE TIENE LAS FOREGIN KEY DESACTIVADAS
    cursor = conexion.cursor()   
    try:
        cursor.execute(f"SELECT service_ticket_id, car_id, customer_id FROM TBL_SERVICE_TICKETS where service_ticket_id = {ticket_id}")
        info = cursor.fetchone()
        cursor.execute(f"SELECT S.service_name, M.mechanic_id, IFNULL((M.hours *  M.rate),0) as Precio_servicio "
        f"FROM TBL_SERVICE_MECHANICS M "
        f"JOIN TBL_SERVICES S ON M.service_id = S.service_id "
        f"where service_ticket_id = {ticket_id}")      
        servicios = cursor.fetchall()

        cursor.execute(f"SELECT P.descripcion, PU.number_used, PU.price, (PU.number_used * PU.price) as precio_piezas "
        f" FROM TBL_PARTS_USED PU "
        f"JOIN TBL_PARTS P ON PU.part_id = P.part_id "
        f"WHERE PU.service_ticket_id = {ticket_id}")
        partes = cursor.fetchall()

        pdf = FPDF (orientation="P", unit="mm", format="A4")
        pdf.add_page()
        pdf.image("logomec.png",x=150, y=15 , w=55)
        pdf.set_font("helvetica","B",12)

        pdf.cell(0,10,f"Factura TICKET: nº{info[0]}",ln=True, align="C")
        pdf.cell(0,10,f"ID Cliente: {info[2]}",ln=True) 
        pdf.cell(0,10,f"ID Vehiculo: {info[1]}", ln=True)
        pdf.ln(7)

        pdf.set_draw_color(52, 73, 94)
        pdf.set_line_width(1)
        pdf.line(10, 42, 200, 42)

        """x1,y1,x2,y2"""
        pdf.ln(5)
        pdf.set_line_width(0.5)
        pdf.set_fill_color(240, 240, 240)
        pdf.cell(0,7,"Servicio",border=1, ln=True, fill=True)
        total = 0
        for servicio in servicios:
            pdf.cell(140,8,f"Servicio realizado: {servicio[0]}")
            pdf.cell(50,8,f"Precio: {servicio[2]} EUR", ln=True,align="R")
            pdf.cell(140,8,f"ID_Mecanico: {servicio[1]}", ln=True)

            total += servicio[2]
        pdf.ln(5)

        pdf.set_draw_color(52, 73, 94)
        pdf.set_line_width(1)
        pdf.line(10, 45, 200,45) 
        """x1,y1,x2,y2"""
        pdf.ln(5)
        pdf.set_line_width(0.5)
        pdf.set_fill_color(240, 240, 240)
        pdf.cell(0,7, "Piezas",border=1, ln= True,fill=True)
        for pieza in partes:
            pdf.cell(140,10,f"Nombre : {pieza[0]}")
            pdf.cell(50,10,f"Precio por pieza : {pieza[2]} EUR",align="R",ln=True)
            pdf.cell(140,10,f"Numero de piezas usadas : {pieza[1]}")
            pdf.cell(50,10,f"Precio total de piezas : {pieza[3]} EUR",align="R",ln=True)

            total += pieza[3]

        pdf.ln(10)
        pdf.set_font("helvetica","B",14)
        pdf.set_fill_color(240, 240, 240)

        pdf.cell(150,12,"Total a pagar: ",align="R")
        pdf.cell(40,12,f"{total} EUR",border=1, ln=True, align="C", fill=True)

        
        archivo = f"Factura_de_{ticket_id}.pdf"
        pdf.output(archivo)
    except sqlite3.Error as e:
        print('Error en la base de datos',e)
    conexion.close()

"""
pdf.cell(w, h, txt, border, ln, align, fill)
"""

if __name__ == "__main__":
    datos_factura(1)
