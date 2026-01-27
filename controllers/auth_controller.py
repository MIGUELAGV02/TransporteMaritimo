from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
import bcrypt
from extensions import db
from models.usuario import Usuario

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

def verify_password(stored_password, provided_password):
    """
    Verifica la contraseña soportando múltiples formatos:
    - Texto plano
    - Hash de werkzeug (pbkdf2:sha256)
    - Hash de bcrypt (Laravel)
    """
    # Si la contraseña almacenada parece ser un hash de werkzeug
    if stored_password.startswith('pbkdf2:') or stored_password.startswith('scrypt:'):
        try:
            return check_password_hash(stored_password, provided_password)
        except ValueError:
            return False
    
    # Si la contraseña almacenada parece ser un hash de bcrypt (Laravel usa $2y$)
    if stored_password.startswith('$2y$') or stored_password.startswith('$2b$') or stored_password.startswith('$2a$'):
        try:
            # Convertir $2y$ a $2b$ para compatibilidad con Python bcrypt
            stored_password_fixed = stored_password.replace('$2y$', '$2b$')
            return bcrypt.checkpw(
                provided_password.encode('utf-8'),
                stored_password_fixed.encode('utf-8')
            )
        except Exception:
            return False
    
    # Si no es un hash reconocido, comparar como texto plano
    return stored_password == provided_password

@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Login usando solo la contraseña (soporta contraseñas hasheadas)
    Body: { "contrasena": "password123" }
    """
    data = request.get_json()
    
    if not data or 'contrasena' not in data:
        return jsonify({'error': 'Contraseña requerida'}), 400
    
    contrasena = data.get('contrasena')
    
    # Buscar usuario verificando contraseña
    usuarios = Usuario.query.all()
    usuario = None
    
    for u in usuarios:
        # Verificar si la contraseña coincide
        if verify_password(u.Contrasena, contrasena):
            usuario = u
            break
    
    if not usuario:
        return jsonify({'error': 'Contraseña incorrecta'}), 401
    
    # Crear token JWT
    access_token = create_access_token(
        identity=str(usuario.id_Usuarios),
        additional_claims={
            'rol': usuario.Rol,
            'nombre': usuario.Nombre,
            'apellido': usuario.Apellido
        }
    )
    
    return jsonify({
        'message': 'Login exitoso',
        'access_token': access_token,
        'usuario': usuario.to_dict()
    }), 200

@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    """
    Obtener información del usuario actual
    """
    current_user_id = get_jwt_identity()
    usuario = Usuario.query.get(current_user_id)
    
    if not usuario:
        return jsonify({'error': 'Usuario no encontrado'}), 404
    
    return jsonify({'usuario': usuario.to_dict()}), 200

@auth_bp.route('/register', methods=['POST'])
def register():
    """
    Registrar un nuevo usuario
    Body: { "nombre": "", "apellido": "", "contrasena": "", "correo": "", "telefono": "", "area": "", "rol": "" }
    """
    data = request.get_json()
    
    required_fields = ['nombre', 'apellido', 'contrasena', 'correo']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Campo {field} es requerido'}), 400
    
    # Verificar si ya existe un usuario con ese correo
    existing_email = Usuario.query.filter_by(Correo=data['correo']).first()
    if existing_email:
        return jsonify({'error': 'El correo ya está registrado'}), 400
    
    # Hashear la contraseña antes de guardar
    hashed_password = generate_password_hash(data['contrasena'], method='pbkdf2:sha256')
    
    nuevo_usuario = Usuario(
        Nombre=data['nombre'],
        Apellido=data['apellido'],
        Contrasena=hashed_password,
        Correo=data['correo'],
        Telefono=data.get('telefono'),
        Area=data.get('area'),
        Rol=data.get('rol', 'usuario')
    )
    
    db.session.add(nuevo_usuario)
    db.session.commit()
    
    return jsonify({
        'message': 'Usuario registrado exitosamente',
        'usuario': nuevo_usuario.to_dict()
    }), 201
