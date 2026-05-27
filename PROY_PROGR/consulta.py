import sqlite3
conexion = sqlite3.connect('SIC.DB')
conexion.execute("PRAGMA foreign_keys = ON;")#ESTO SE PONE PORQUE POR DEFECTO SQLITE TIENE LAS FOREGIN KEY DESACTIVADAS
cursor = conexion.cursor()  
try:
    cursor.execute("SELECT * FROM TBL_PARTS_USED")
    print(cursor.fetchall())
except sqlite3.Error as e:
    print('no se pueden meter datos',e)
conexion.close()