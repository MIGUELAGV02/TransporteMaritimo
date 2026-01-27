from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt
from werkzeug.security import generate_password_hash
from extensions import db
from models.usuario import Usuario

usuario_bp = Blueprint('usuarios', __name__, url_prefix='/api/usuarios')

def check_admin():
    """Verificar si el usuario actual es admin o superusuario"""
    claims = get_jwt()
    return claims.get('rol') in ['admin', 'superusuario']

@usuario_bp.route('/', methods=['GET'])
@jwt_required()
def get_usuarios():
    """Obtener todos los usuarios"""
    if not check_admin():
        return jsonify({'error': 'No autorizado'}), 403
    
    usuarios = Usuario.query.all()
    return jsonify({'usuarios': [u.to_dict() for u in usuarios]}), 200

@usuario_bp.route('/<int:id>', methods=['GET'])
@jwt_required()
def get_usuario(id):
    """Obtener un usuario por ID"""
    usuario = Usuario.query.get(id)
    
    if not usuario:
        return jsonify({'error': 'Usuario no encontrado'}), 404
    
    return jsonify({'usuario': usuario.to_dict()}), 200

@usuario_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update_usuario(id):
    """Actualizar un usuario"""
    if not check_admin():
        return jsonify({'error': 'No autorizado'}), 403
    
    usuario = Usuario.query.get(id)
    
    if not usuario:
        return jsonify({'error': 'Usuario no encontrado'}), 404
    
    data = request.get_json()
    
    if 'nombre' in data:
        usuario.Nombre = data['nombre']
    if 'apellido' in data:
        usuario.Apellido = data['apellido']
    if 'contrasena' in data:
        # Hashear la nueva contraseña
        usuario.Contrasena = generate_password_hash(data['contrasena'], method='pbkdf2:sha256')
    if 'correo' in data:
        existing = Usuario.query.filter_by(Correo=data['correo']).first()
        if existing and existing.id_Usuarios != id:
            return jsonify({'error': 'El correo ya está en uso'}), 400
        usuario.Correo = data['correo']
    if 'telefono' in data:
        usuario.Telefono = data['telefono']
    if 'area' in data:
        usuario.Area = data['area']
    if 'rol' in data:
        usuario.Rol = data['rol']
    
    db.session.commit()
    
    return jsonify({
        'message': 'Usuario actualizado',
        'usuario': usuario.to_dict()
    }), 200

@usuario_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_usuario(id):
    """Eliminar un usuario"""
    if not check_admin():
        return jsonify({'error': 'No autorizado'}), 403
    
    usuario = Usuario.query.get(id)
    
    if not usuario:
        return jsonify({'error': 'Usuario no encontrado'}), 404
    
    db.session.delete(usuario)
    db.session.commit()
    
    return jsonify({'message': 'Usuario eliminado'}), 200
