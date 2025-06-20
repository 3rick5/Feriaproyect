from flask import Flask, render_template
import serial.tools.list_ports
import serial
import time
import mysql.connector
from mysql.connector import Error
import threading

app = Flask(__name__, template_folder='.')

# --- Función para conectar a la base de datos ---
def conectar_base_datos():
    try:
        conexion = mysql.connector.connect(
            host="localhost",
            user="root",
            password="estudiante",
            database="patito"
        )
        if conexion.is_connected():
            print("[OK] Conectado a la base de datos 'patito'.")
            return conexion
    except Error as e:
        print(f"[ERROR] No se pudo conectar a la base de datos: {e}")
        return None

# --- Función para conectar al Arduino ---
def conectar_arduino():
    puertos = [p.device for p in serial.tools.list_ports.comports()]
    if 'COM4' not in puertos:
        print("[ERROR] COM4 no está disponible. Verificá la conexión USB.")
        return None
    try:
        print("[INFO] Conectando a COM4...")
        arduino = serial.Serial('COM4', 9600, timeout=1)
        time.sleep(2)  # Espera para que Arduino se reinicie
        print("[OK] Conectado a COM4.")
        return arduino
    except Exception as e:
        print(f"[ERROR] No se pudo abrir COM4: {e}")
        return None

# --- Función que corre en hilo separado para leer datos y guardar en BD ---
def leer_datos_loop():
    arduino = conectar_arduino()
    if not arduino:
        print("[ERROR] No se pudo conectar al Arduino. Terminando hilo de lectura.")
        return

    conexion_db = conectar_base_datos()
    if not conexion_db:
        print("[ERROR] No se pudo conectar a la base de datos. Terminando hilo de lectura.")
        arduino.close()
        return

    cursor = conexion_db.cursor()
    print("[INFO] Iniciando lectura de datos desde Arduino (Ctrl+C para detener)...")

    try:
        while True:
            if arduino.in_waiting > 0:
                linea = arduino.readline().decode('utf-8', errors='ignore').strip()
                if linea:
                    print(f"[DATOS]  {linea}")
                    try:
                        consulta = "INSERT INTO lecturas (valor) VALUES (%s)"
                        cursor.execute(consulta, (linea,))
                        conexion_db.commit()
                        print("[BD] Dato guardado en la tabla 'lecturas'.")
                    except Error as err:
                        print(f"[ERROR] No se pudo insertar el dato: {err}")
            time.sleep(0.1)  # Evita usar CPU al 100%
    except KeyboardInterrupt:
        print("\n[INFO] Lectura interrumpida por el usuario.")
    finally:
        cursor.close()
        conexion_db.close()
        arduino.close()
        print("[INFO] Hilo de lectura finalizado.")

# --- Función para obtener datos y mostrar en la web ---
def obtener_datos():
    try:
        conexion = mysql.connector.connect(
            host="localhost",
            user="root",
            password="estudiante",
            database="patito"
        )
        if conexion.is_connected():
            cursor = conexion.cursor()
            cursor.execute("SELECT valor, fecha FROM lecturas ORDER BY id DESC LIMIT 20")
            datos = cursor.fetchall()
            cursor.close()
            return datos
    except Error as e:
        print(f"[ERROR] No se pudo obtener datos: {e}")
        return []
    finally:
        if 'conexion' in locals() and conexion.is_connected():
            conexion.close()

@app.route("/")
def pagina_principal():
    return render_template("index.html")
@app.route("/datos")
def index():
    datos = obtener_datos()
    print(datos)  # Para debug en consola
    return render_template("pagina.html", datos=datos)
@app.route("/calc")
def calculos():
    return render_template("calculo.html")

if __name__ == "__main__":
    # Crear y arrancar hilo para lectura Arduino
    hilo_lectura = threading.Thread(target=leer_datos_loop, daemon=True)
    hilo_lectura.start()

    # Arrancar servidor Flask
    app.run(debug=True)