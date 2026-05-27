import sqlite3 
conexion = sqlite3.connect('SIC.DB')
conexion.execute("PRAGMA foreign_keys = OFF;")

try:
    conexion.execute("DELETE FROM TBL_MECHANICS")

except sqlite3.Error as e:
     print("Error al borrar tabla",e)
conexion.commit()
conexion.close()
