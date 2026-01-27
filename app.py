import sys
import os

# Agregar el directorio actual al path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from config import Config
from extensions import db

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Inicializar extensiones
    CORS(app)
    db.init_app(app)
    jwt = JWTManager(app)
    
    # Manejadores de errores JWT
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return jsonify({
            'error': 'Token expirado',
            'message': 'El token de acceso ha expirado'
        }), 401
    
    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return jsonify({
            'error': 'Token inválido',
            'message': 'Verificación de firma fallida'
        }), 401
    
    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return jsonify({
            'error': 'Token requerido',
            'message': 'Token de autorización no encontrado'
        }), 401
    
    # Registrar blueprints
    from controllers import auth_bp, usuario_bp, maritimo_bp, aereo_bp, terrestre_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(usuario_bp)
    app.register_blueprint(maritimo_bp)
    app.register_blueprint(aereo_bp)
    app.register_blueprint(terrestre_bp)
    
    # Ruta de prueba
    @app.route('/')
    def index():
        return jsonify({
            'message': 'API de Logística',
            'version': '1.0.0',
            'endpoints': {
                'auth': '/api/auth',
                'usuarios': '/api/usuarios',
                'maritimo': '/api/maritimo',
                'aereo': '/api/aereo',
                'terrestre': '/api/terrestre'
            }
        })
    
    # Crear tablas
    with app.app_context():
        db.create_all()
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)
