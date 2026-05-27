import sqlite3 
conexion = sqlite3.connect('SIC.DB')
conexion.execute("PRAGMA foreign_keys = OFF;")

try:
    conexion.execute("DROP DATABASE SIC.DB")
    
except sqlite3.Error as e:
     print("Error al borrar tabla",e)

conexion.close()
