import sqlite3

# Conectamos a la base de datos
conexion = sqlite3.connect('SIC.DB')
conexion.execute("PRAGMA foreign_keys = ON;")
cursor = conexion.cursor()

try:
    # --- DATOS PARA TBL_SERVICES ---
    #(service_name, hourly_rate)
    servicios_data = [
        ("Cambio de Aceite y Filtro", 35.00),
        ("Revisión y Cambio de Frenos", 45.00),
        ("Alineación y Balanceo", 40.00),
        ("Diagnóstico por Escáner Eléctrico", 50.00),
        ("Mantenimiento del Sistema de AC", 42.50),
        ("Cambio de Kit de Distribución", 55.00),
        ("Reparación de Suspensión y Amortiguadores", 48.00),
        ("Cambio de Embrague", 60.00),
        ("Limpieza de Inyectores", 38.00),
        ("Revisión General Pre-ITV", 30.00)
    ]

    # Insertamos los servicios
    cursor.executemany("""
        INSERT INTO TBL_SERVICES (service_name, hourly_rate)
        VALUES (?, ?)
    """, servicios_data)
    

    # --- DATOS PARA TBL_PARTS ---
    # (part_number, descripcion, purchase_price, retail_price)
    partes_data = [
        ("AC-5W30-4L", "Aceite Sintético 5W30 (4L)", 22.50, 42.00),
        ("FL-OIL-01", "Filtro de Aceite Premium", 4.20, 9.50),
        ("FR-PA-CER02", "Pastillas de Freno Cerámicas", 18.00, 35.00),
        ("FR-DI-VENT", "Disco de Freno Ventilado", 28.50, 55.00),
        ("AM-DEL-HYU", "Amortiguador Delantero Hidráulico", 32.00, 64.00),
        ("BT-12V-75AH", "Batería de Coche 12V 75Ah", 45.00, 89.90),
        ("BU-NGK-IRID", "Bujía de Iridio NGK (Unidad)", 3.80, 8.50),
        ("KI-DIST-GATES", "Kit de Correa de Distribución", 65.00, 120.00),
        ("FL-AIR-ECO", "Filtro de Aire de Motor", 5.00, 12.00),
        ("LIQ-REFR-5L", "Líquido Refrigerante 50% (5L)", 6.50, 14.00)
    ]

    # Insertamos las partes
    cursor.executemany("""
        INSERT INTO TBL_PARTS (part_number, descripcion, purchase_price, retail_price)
        VALUES (?, ?, ?, ?)
    """, partes_data)
    


    conexion.commit()

except sqlite3.Error as error:
    print("Error al insertar los datos de prueba:", error)
    conexion.rollback()

    conexion.close()