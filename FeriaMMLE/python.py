from flask import Flask, render_template
import os
import mysql.connector
from mysql.connector import Error

app = Flask(__name__, template_folder='.')

def obtener_datos():
    try:
        conexion = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Yisus",
            database="patito"
        )
        if conexion.is_connected():
            cursor = conexion.cursor()
            cursor.execute("SELECT valor, fecha FROM lecturas ORDER BY id DESC LIMIT 10")
            datos = cursor.fetchall()
            return datos
    except Error as e:
        print(f"[ERROR] No se pudo obtener datos: {e}")
        return []
    finally:
        if conexion.is_connected():
            conexion.close()

@app.route("/")
def pagina_principal():
    datos = obtener_datos()
    print(datos)  # Para debug en consola
    return render_template("pagina.html", datos=datos)

if __name__ == "__main__":
    app.run(debug=True)
