import sqlite3
conexion = sqlite3.connect('SIC.DB')
conexion.execute("PRAGMA foreign_keys = ON;") #ESTO SE PONE PORQUE POR DEFECTO SQLITE TIENE LAS FOREGIN KEY DESACTIVADAS
cursor = conexion.cursor()   
try:
    cursor.execute("INSERT INTO TBL_USUARIOS VALUES ('Mecanico','123456','mecanico')")
    cursor.execute("INSERT INTO TBL_USUARIOS VALUES ('Recepcion','123456','recepcion')")
    

except sqlite3.Error as e:
    print('no se pueden meter datos',e)
conexion.commit()
conexion.close()

