import sqlite3 

def borrar_tabla(nombre):
    try:
        conexion = sqlite3.connect('SIC.DB')
        conexion.execute("PRAGMA foreign_keys = OFF;")
        conexion.execute(f"DROP TABLE IF EXISTS {nombre}")
        print(f"tabla {nombre} Borrada")
    except sqlite3.Error as e:
        print("Error al borrar tabla",e)

    conexion.close()


borrar_tabla("TBL_USUARIOS")