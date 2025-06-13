from flask import Flask, render_template
import mysql.connector

app = Flask(__name__)

# ✅ Configuración de la conexión a la base de datos
conexion = mysql.connector.connect(
    host="localhost",
    user="root",           # Ej: root
    password="estudiante",    # Ej: 1234
    database="patito"           # Ej: recolector
)

@app.route("/")
def index():
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("SELECT * FROM datos_lluvia ORDER BY fecha DESC LIMIT 10")
    datos = cursor.fetchall()
    return render_template("pagina.html", datos=datos)

if __name__ == "__main__":
    app.run(debug=True)
