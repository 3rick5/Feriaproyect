import serial
import serial.tools.list_ports
import time
import sqlite3

# Crear la base de datos y la tabla si no existen
def crear_bd():
    conn = sqlite3.connect('datos_agua.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS lecturas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            dato TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

# Guardar un dato en la base de datos
def guardar_dato(dato):
    conn = sqlite3.connect('datos_agua.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO lecturas (dato) VALUES (?)', (dato,))
    conn.commit()
    conn.close()
 
 ######################################################################################
def conectar_arduino():
    puertos = [p.device for p in serial.tools.list_ports.comports()]
   
    if 'COM8' not in puertos:
        print("[ERROR] COM6 no está disponible. Verificá la conexión USB.")
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
 
def leer_datos(arduino):
    print("[INFO] Esperando datos desde el Arduino (Ctrl+C para salir)...")
    try:
        while True:
            if arduino.in_waiting > 0:
                linea = arduino.readline().decode('utf-8', errors='ignore').strip()
                if linea:
                    print(f"[DATOS] {linea}")
    except KeyboardInterrupt:
        print("\n[INFO] Lectura interrumpida por el usuario.")
    finally:
        arduino.close()
        print("[INFO] Puerto cerrado.")
 
# Programa principal
arduino = conectar_arduino()
 
if arduino:
    leer_datos(arduino)
else:
    print("[FINALIZADO] No se pudo establecer la conexión.")