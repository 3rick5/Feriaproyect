from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData

# Configuración personalizada para evitar errores de collation
metadata = MetaData()

# Crear la app Flask
app = Flask(__name__)

# URI de conexión (ajusta tu usuario, contraseña, host, y base de datos)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://usuario:contraseña@localhost/tu_base_de_datos?charset=utf8mb4'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Crear la instancia de SQLAlchemy con metadata personalizada
db = SQLAlchemy(app, metadata=metadata)

# Modelo de ejemplo
class Usuario(db.Model):
    __tablename__ = 'usuarios'
    __table_args__ = {
        'mysql_charset': 'utf8mb4',
        'mysql_collate': 'utf8mb4_unicode_ci'
    }

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    correo = db.Column(db.String(120), nullable=False)

# Crear las tablas en la base de datos (si no existen)
with app.app_context():
    db.create_all()
