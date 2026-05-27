import sqlite3
conexion = sqlite3.connect('SIC.DB')
conexion.execute("PRAGMA foreign_keys = ON;") #ESTO SE PONE PORQUE POR DEFECTO SQLITE TIENE LAS FOREGIN KEY DESACTIVADAS
cursor = conexion.cursor()   
try:
    conexion.execute("INSERT INTO TBL_MECHANICS VALUES ('M01', 'Carla', 'Turegano')")
    conexion.execute("INSERT INTO TBL_MECHANICS VALUES ('M02', 'Ivan', 'Mesa')")
    conexion.execute("INSERT INTO TBL_MECHANICS VALUES ('M03', 'Sebastian', 'Martinez')")
    conexion.execute("INSERT INTO TBL_MECHANICS VALUES ('M04', 'Miguel Angel', 'Perez')")
    conexion.execute("INSERT INTO TBL_MECHANICS VALUES ('M05', 'Andrea', 'Vidal')")
    
    
except sqlite3.Error as e:
    print('no se pueden meter datos',e)
conexion.commit()
conexion.close()



