from flask import Flask
from flask_cors import CORS
from models import db
from controllers import (
    AuthController, 
    UsuarioController, 
    ReporteController,
    MaritimoController,
    AereoController,
    TransporteTerrestreController
)
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

app = Flask(__name__)
CORS(app)

# Configuración de la base de datos (MySQL local)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'mysql+pymysql://root@localhost:3306/system')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')

# Inicializar la base de datos
db.init_app(app)

# Crear tablas si no existen
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return "API de Gestión de Reportes de Transporte"

# Rutas de autenticación
@app.route('/api/login', methods=['POST'])
def login():
    return AuthController.login()

# Rutas de usuarios (protegidas)
@app.route('/api/usuarios', methods=['GET'])
def get_usuarios():
    return UsuarioController.get_usuarios()

@app.route('/api/usuarios/<int:id>', methods=['GET'])
def get_usuario(id):
    return UsuarioController.get_usuario(id)

# Rutas de reportes (protegidas)
@app.route('/api/reportes', methods=['GET'])
def get_reportes():
    return ReporteController.get_reportes()

@app.route('/api/reportes/<int:id>', methods=['GET'])
def get_reporte(id):
    return ReporteController.get_reporte(id)

@app.route('/api/reportes', methods=['POST'])
def create_reporte():
    return ReporteController.create_reporte()

# Rutas de marítimos (protegidas)
@app.route('/api/maritimos', methods=['GET'])
def get_maritimos():
    return MaritimoController.get_maritimos()

@app.route('/api/maritimos/<int:id>', methods=['GET'])
def get_maritimo(id):
    return MaritimoController.get_maritimo(id)

@app.route('/api/maritimos', methods=['POST'])
def create_maritimo():
    return MaritimoController.create_maritimo()

# Rutas de aéreos (protegidas)
@app.route('/api/aereos', methods=['GET'])
def get_aereos():
    return AereoController.get_aereos()

@app.route('/api/aereos/<int:id>', methods=['GET'])
def get_aereo(id):
    return AereoController.get_aereo(id)

@app.route('/api/aereos', methods=['POST'])
def create_aereo():
    return AereoController.create_aereo()

# Rutas de transporte terrestre (protegidas)
@app.route('/api/transportes-terrestres', methods=['GET'])
def get_transportes():
    return TransporteTerrestreController.get_transportes()

@app.route('/api/transportes-terrestres/<int:id>', methods=['GET'])
def get_transporte(id):
    return TransporteTerrestreController.get_transporte(id)

@app.route('/api/transportes-terrestres', methods=['POST'])
def create_transporte():
    return TransporteTerrestreController.create_transporte()

# Ruta de verificación
@app.route('/api/health', methods=['GET'])
def health_check():
    return {'status': 'API funcionando correctamente'}, 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)