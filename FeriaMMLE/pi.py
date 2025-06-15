import serial
import serial.tools.list_ports
import time
import mysql.connector
from mysql.connector import Error

######################################################################################
# Conectar a la base de datos MySQL
######################################################################################
def conectar_base_datos():
    try:
        conexion = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Yisus",
            database="patito"
        )
        if conexion.is_connected():
            print("[OK] Conectado a la base de datos 'patito'.")
            return conexion
    except Error as e:
        print(f"[ERROR] No se pudo conectar a la base de datos: {e}")
        return None

######################################################################################
# Conectar al Arduino y leer datos
######################################################################################
def conectar_arduino():
    puertos = [p.device for p in serial.tools.list_ports.comports()]
    
    if 'COM8' not in puertos:
        print("[ERROR] COM8 no está disponible. Verificá la conexión USB.")
        return None
 
    try:
        print("[INFO] Conectando a COM8...")
        arduino = serial.Serial('COM8', 9600, timeout=1)
        time.sleep(2)  # Espera para que el Arduino se reinicie correctamente
        print("[OK] Conectado a COM8.")
        return arduino
    except Exception as e:
        print(f"[ERROR] No se pudo abrir COM8: {e}")
        return None

######################################################################################
# Leer datos y guardarlos en la base de datos
######################################################################################
def leer_datos(arduino, conexion_db):
    print("[INFO] Esperando datos desde el Arduino (Ctrl+C para salir)...")
    cursor = conexion_db.cursor()

    try:
        while True:
            if arduino.in_waiting > 0:
                linea = arduino.readline().decode('utf-8', errors='ignore').strip()
                if linea:
                    print(f"[DATOS] {linea}")
                    try:
                        consulta = "INSERT INTO lecturas (valor) VALUES (%s)"
                        cursor.execute(consulta, (linea,))
                        conexion_db.commit()
                        print("[BD] Dato guardado en la tabla 'lecturas'.")
                    except Error as err:
                        print(f"[ERROR] No se pudo insertar el dato en 'lecturas': {err}")
    except KeyboardInterrupt:
        print("\n[INFO] Lectura interrumpida por el usuario.")
    finally:
        arduino.close()
        cursor.close()
        conexion_db.close()
        print("[INFO] Puerto cerrado y conexión a BD finalizada.")

######################################################################################
# Programa principal
######################################################################################
arduino = conectar_arduino()
conexion_db = conectar_base_datos()

if arduino and conexion_db:
    leer_datos(arduino, conexion_db)
else:
    print("[FINALIZADO] No se pudo establecer la conexión con Arduino o la base de datos.")
