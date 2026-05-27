import sqlite3

conexion = sqlite3.connect('SIC.DB')
conexion.execute("PRAGMA foreign_keys = ON;")  #ESTO SE PONE PORQUE POR DEFECTO SQLITE TIENE LAS FOREGIN KEY DESACTIVADAS


try:
    conexion.execute("""create table if not exists TBL_CUSTOMERS(
        customer_id TEXT PRIMARY KEY,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL)""")
    
    conexion.execute("""create table if not exists TBL_CARS(
        car_id TEXT PRIMARY KEY,
        brand TEXT NOT NULL,
        model TEXT NOT NULL,
        year INTEGER NOT NULL)""")
    
    conexion.execute("""create table if not exists TBL_MECHANICS(
        mechanic_id TEXT PRIMARY KEY,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL)""")
    
    conexion.execute("""create table if not exists TBL_SERVICES(
        service_id INTEGER PRIMARY KEY AUTOINCREMENT,
        service_name TEXT NOT NULL,
        hourly_rate REAL NOT NULL)""")
    
    conexion.execute("""create table if not exists TBL_SERVICE_TICKETS(
        service_ticket_id INTEGER PRIMARY KEY AUTOINCREMENT,
        car_id TEXT NOT NULL,
        customer_id TEXT NOT NULL,
        date_received DATETIME NOT NULL,
        comments TEXT,
        date_returned DATETIME,

        FOREIGN KEY (car_id) REFERENCES TBL_CARS(car_id),
        FOREIGN KEY (customer_id) REFERENCES TBL_CUSTOMERS(customer_id))""")
    
    conexion.execute("""create table if not exists TBL_SERVICE_MECHANICS(
        service_mechanic_id INTEGER PRIMARY KEY AUTOINCREMENT,
        service_ticket_id INTEGER NOT NULL,
        service_id INTEGER,
        mechanic_id TEXT,
        hours REAL,
        comments TEXT,
        rate REAL,
    
        FOREIGN KEY (service_ticket_id) REFERENCES TBL_SERVICE_TICKETS(service_ticket_id),
        FOREIGN KEY (service_id) REFERENCES TBL_SERVICES(service_id),
        FOREIGN KEY (mechanic_id) REFERENCES TBL_MECHANICS(mechanic_id))""")             

    conexion.execute("""create table if not exists TBL_PARTS(
        part_id INTEGER PRIMARY KEY AUTOINCREMENT,
        part_number TEXT NOT NULL,
        descripcion TEXT,
        purchase_price REAL NOT NULL,
        retail_price REAL NOT NULL)""")    
    
    conexion.execute("""create table if not exists TBL_PARTS_USED(
        part_used_id INTEGER PRIMARY KEY AUTOINCREMENT,
        part_id INTEGER NOT NULL,
        service_ticket_id INTEGER NOT NULL,
        number_used INTEGER NOT NULL,
        price REAL NOT NULL,
                     
        FOREIGN KEY (part_id) REFERENCES TBL_PARTS(part_id),
        FOREIGN KEY (service_ticket_id) REFERENCES TBL_SERVICE_TICKETS(service_ticket_id))""") 
    
    conexion.execute("""create table if not exists TBL_USUARIOS(
        usuario_id TEXT PRIMARY KEY ,
        contrasenya TEXT NOT NULL,
        rol TEXT NOT NULL)""") 
                     
except sqlite3.Error as e:
    print('Base de datos ya existe',e)
    
conexion.commit()
conexion.close()
