import sqlite3

import sqlite3


def obtener_citas_activas():

    conexion = sqlite3.connect('SIC.DB')
    conexion.execute("PRAGMA foreign_keys = ON;")

    cursor = conexion.cursor()

    cursor.execute(
    """
    SELECT
        st.service_ticket_id, 
        cu.first_name,
        cu.last_name,
        ca.car_id,
        st.date_received,
        IFNULL(st.date_returned, 'Pendiente') AS date_returned
    FROM TBL_SERVICE_TICKETS st
    INNER JOIN TBL_CUSTOMERS cu
        ON cu.customer_id = st.customer_id
    INNER JOIN TBL_CARS ca
        ON ca.car_id = st.car_id
    """)

    resultados = cursor.fetchall()

    conexion.close()

    return resultados


def obtener_mecanicos_activos():

    conexion = sqlite3.connect('SIC.DB')
    conexion.execute("PRAGMA foreign_keys = ON;")

    cursor = conexion.cursor()

    cursor.execute("""
    SELECT
        mc.mechanic_id,
        mc.first_name,
        mc.last_name,
        COUNT(sm.service_ticket_id) AS tickets_abiertos,
        CASE
            WHEN COUNT(sm.service_ticket_id) >= 3 THEN 'No Disponible'
            ELSE 'Disponible'
        END AS Disponibilidad
    FROM TBL_MECHANICS mc
    LEFT JOIN TBL_SERVICE_MECHANICS sm
        ON sm.mechanic_id = mc.mechanic_id 
    LEFT JOIN TBL_SERVICE_TICKETS st
        ON st.service_ticket_id = sm.service_ticket_id AND st.date_returned IS NULL
    GROUP BY
        mc.mechanic_id,
        mc.first_name,
        mc.last_name;
    """)

    resultados = cursor.fetchall() 

    conexion.close()

    return resultados


def registrar_nuevo_ticket(datos):

    conexion = sqlite3.connect('SIC.DB')
    conexion.execute("PRAGMA foreign_keys = ON;")
    cursor = conexion.cursor()   

    try:

        cursor.execute("""
        INSERT OR IGNORE INTO TBL_CUSTOMERS (customer_id, first_name, last_name)
        VALUES
            (?, ?, ?);
        """, (datos['dni'], datos['nombre'], datos['apellido']))

        cursor.execute("""
        INSERT OR IGNORE INTO TBL_CARS (car_id, brand, model, year)
        VALUES
            (?, ?, ?, ?);
        """, (datos['matricula'], datos['marca'], datos['modelo'], datos['anio']))


        cursor.execute("""
        INSERT INTO TBL_SERVICE_TICKETS (car_id, customer_id, date_received, comments, date_returned)
        VALUES
            (?, ?, date('now'), ?, NULL);
        """, (datos['matricula'], datos['dni'], datos['observaciones']))

        cursor.execute("""
        SELECT MAX(service_ticket_id) FROM TBL_SERVICE_TICKETS;
        """)

        resultado = cursor.fetchone() 
        service_ticket_id = resultado[0]

        cursor.execute("""
        INSERT INTO TBL_SERVICE_MECHANICS (service_ticket_id, mechanic_id)
        VALUES
            (?, ?)
        """, (service_ticket_id, datos['id_mecanico']))

        conexion.commit()
        return True

    except sqlite3.Error as e:
        print('ERROR: ',e)
        conexion.rollback()
        return False

    finally:
        conexion.close()




##################################################################################################################################################################################################
def eliminar_ticket(ticket_id):
    conexion = sqlite3.connect('SIC.DB')
    conexion.execute("PRAGMA foreign_keys = ON;")
    cursor = conexion.cursor()

    try:
        cursor.execute("DELETE FROM TBL_PARTS_USED WHERE service_ticket_id = ?", (ticket_id,)) #
        cursor.execute("DELETE FROM TBL_SERVICE_MECHANICS WHERE service_ticket_id = ?", (ticket_id,)) #
        

        cursor.execute("DELETE FROM TBL_SERVICE_TICKETS WHERE service_ticket_id = ?", (ticket_id,)) #

        conexion.commit()


    except sqlite3.Error as e:
        print('ERROR: ', e)
        conexion.rollback()

    finally:
        conexion.close()




def obtener_fecha_cita(ticket_id):

    conexion = sqlite3.connect('SIC.DB')
    conexion.execute("PRAGMA foreign_keys = ON;")

    cursor = conexion.cursor()

    cursor.execute(
    """
    SELECT
        st.date_returned IS NOT NULL
    FROM TBL_SERVICE_TICKETS st
    WHERE 
        st.service_ticket_id = ?
    """, (ticket_id,))

    resultado = cursor.fetchone()

    conexion.close()

    if not resultado:
        return "No existe"

    if resultado[0] == 1:
        return "CERRADO"
    else: 
        return "ABIERTO"
##################################################################################################################################################################################################