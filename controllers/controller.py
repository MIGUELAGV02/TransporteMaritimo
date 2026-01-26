from flask import jsonify, request
from models import db, Usuario, Reporte, Maritimo, Aereo, TransporteTerrestre
import jwt
import datetime
from functools import wraps
from werkzeug.security import check_password_hash, generate_password_hash

# Configuración (debería estar en variables de entorno)
SECRET_KEY = 'dev-secret-key-change-in-production'

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            if auth_header.startswith('Bearer '):
                token = auth_header.split(' ')[1]
        
        if not token:
            return jsonify({'message': 'Token es requerido!'}), 401
        
        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            current_user = Usuario.query.get(data['user_id'])
            if not current_user:
                return jsonify({'message': 'Usuario no encontrado!'}), 401
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token expirado!'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Token inválido!'}), 401
        
        return f(current_user, *args, **kwargs)
    
    return decorated

class AuthController:
    @staticmethod
    def login():
        data = request.get_json()
        correo = data.get('correo')
        contraseña = data.get('contraseña')
        
        if not correo or not contraseña:
            return jsonify({'message': 'Correo y contraseña son requeridos'}), 400
        
        usuario = Usuario.query.filter_by(Correo=correo).first()
        
        if not usuario:
            return jsonify({'message': 'Credenciales inválidas'}), 401
        
        # Verificar contraseña hasheada
        if not check_password_hash(usuario.Contraseña, contraseña):
            return jsonify({'message': 'Credenciales incorrectas'}), 401
        
        # Crear token JWT
        token_data = {
            'user_id': usuario.ID,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
        }
        token = jwt.encode(token_data, SECRET_KEY, algorithm='HS256')
        
        return jsonify({
            'token': token,
            'user': usuario.to_dict()
        }), 200

class UsuarioController:
    @staticmethod
    @token_required
    def get_usuarios(current_user):
        usuarios = Usuario.query.all()
        return jsonify([usuario.to_dict() for usuario in usuarios]), 200
    
    @staticmethod
    @token_required
    def get_usuario(current_user, id):
        usuario = Usuario.query.get(id)
        if not usuario:
            return jsonify({'message': 'Usuario no encontrado'}), 404
        return jsonify(usuario.to_dict()), 200

class ReporteController:
    @staticmethod
    @token_required
    def get_reportes(current_user):
        reportes = Reporte.query.all()
        return jsonify([reporte.to_dict() for reporte in reportes]), 200
    
    @staticmethod
    @token_required
    def get_reporte(current_user, id):
        reporte = Reporte.query.get(id)
        if not reporte:
            return jsonify({'message': 'Reporte no encontrado'}), 404
        return jsonify(reporte.to_dict()), 200
    
    @staticmethod
    @token_required
    def create_reporte(current_user):
        data = request.get_json()
        
        reporte = Reporte(
            titulo=data.get('titulo'),
            descripcion=data.get('descripcion'),
            tipo=data.get('tipo'),
            estado=data.get('estado', 'Pendiente'),
            usuario_id=current_user.ID,
            contenedor_id=data.get('contenedor_id'),
            aereo_id=data.get('aereo_id'),
            transporteterrestre_id=data.get('transporteterrestre_id')
        )
        
        db.session.add(reporte)
        db.session.commit()
        
        return jsonify(reporte.to_dict()), 201

class MaritimoController:
    @staticmethod
    @token_required
    def get_maritimos(current_user):
        maritimos = Maritimo.query.all()
        return jsonify([maritimo.to_dict() for maritimo in maritimos]), 200
    
    @staticmethod
    @token_required
    def get_maritimo(current_user, id):
        maritimo = Maritimo.query.get(id)
        if not maritimo:
            return jsonify({'message': 'Registro marítimo no encontrado'}), 404
        return jsonify(maritimo.to_dict()), 200
    
    @staticmethod
    @token_required
    def create_maritimo(current_user):
        data = request.get_json()
        
        maritimo = Maritimo(
            Nombre=data.get('nombre'),
            Cliente=data.get('cliente'),
            Tipo_envio_despacio=data.get('tipo_envio_despacio'),
            Tipo_Mercancia=data.get('tipo_mercancia'),
            Transporte_Estadias=data.get('transporte_estadias'),
            Link_naviera=data.get('link_naviera'),
            aduanacofigen=data.get('aduanacofigen'),
            aduanadesino=data.get('aduanadesino'),
            transporteterrestre=data.get('transporte_terrestre'),
            BL=data.get('bl'),
            Disamaritinos=data.get('disamaritinos'),
            Dislomacensis=data.get('dislomacensis'),
            Diastotales=data.get('diastotales'),
            Barco=data.get('barco'),
            Fechasalida=data.get('fechasalida'),
            Fechacreacion=data.get('fechacreacion'),
            Paísdestino=data.get('pais_destino'),
            Paisorigen=data.get('pais_origen'),
            Guiaarea=data.get('guia_area'),
            Fleteterrestre=data.get('flete_terrestre'),
            CostoCotizacion=data.get('costo_cotizacion'),
            CostoTotal=data.get('costo_total')
        )
        
        db.session.add(maritimo)
        db.session.commit()
        
        return jsonify(maritimo.to_dict()), 201

class AereoController:
    @staticmethod
    @token_required
    def get_aereos(current_user):
        aereos = Aereo.query.all()
        return jsonify([aereo.to_dict() for aereo in aereos]), 200
    
    @staticmethod
    @token_required
    def get_aereo(current_user, id):
        aereo = Aereo.query.get(id)
        if not aereo:
            return jsonify({'message': 'Registro aéreo no encontrado'}), 404
        return jsonify(aereo.to_dict()), 200
    
    @staticmethod
    @token_required
    def create_aereo(current_user):
        data = request.get_json()
        
        aereo = Aereo(
            Nombre=data.get('nombre'),
            Cliente=data.get('cliente'),
            Tipo_envio_despacio=data.get('tipo_envio_despacio'),
            Tipo_Mercancia=data.get('tipo_mercancia'),
            Transporte_Estadias=data.get('transporte_estadias'),
            Link_naviera=data.get('link_naviera'),
            aduanacofigen=data.get('aduanacofigen'),
            aduanadesino=data.get('aduanadesino'),
            transporteterrestre=data.get('transporte_terrestre'),
            GuiaAerea=data.get('guia_aerea'),
            Clave_de_Rastreo=data.get('clave_rastreo'),
            Disamaritinos=data.get('disamaritinos'),
            Dislomacensis=data.get('dislomacensis'),
            Diastotales=data.get('diastotales'),
            Fechasalida=data.get('fechasalida'),
            Fechacreacion=data.get('fechacreacion'),
            Paísdestino=data.get('pais_destino'),
            Paisorigen=data.get('pais_origen'),
            Fleteterrestre=data.get('flete_terrestre'),
            CostoCotizacion=data.get('costo_cotizacion'),
            CostoTotal=data.get('costo_total'),
            Auditado=data.get('auditado', False)
        )
        
        db.session.add(aereo)
        db.session.commit()
        
        return jsonify(aereo.to_dict()), 201

class TransporteTerrestreController:
    @staticmethod
    @token_required
    def get_transportes(current_user):
        transportes = TransporteTerrestre.query.all()
        return jsonify([transporte.to_dict() for transporte in transportes]), 200
    
    @staticmethod
    @token_required
    def get_transporte(current_user, id):
        transporte = TransporteTerrestre.query.get(id)
        if not transporte:
            return jsonify({'message': 'Registro de transporte terrestre no encontrado'}), 404
        return jsonify(transporte.to_dict()), 200
    
    @staticmethod
    @token_required
    def create_transporte(current_user):
        data = request.get_json()
        
        transporte = TransporteTerrestre(
            Nombre=data.get('nombre'),
            Cliente=data.get('cliente'),
            Tipo_envio_despacio=data.get('tipo_envio_despacio'),
            Tipo_Mercancia=data.get('tipo_mercancia'),
            Transporte_Estadias=data.get('transporte_estadias'),
            Link_naviera=data.get('link_naviera'),
            Transporte=data.get('transporte'),
            Placas=data.get('placas'),
            Chofer=data.get('chofer'),
            Num_económico=data.get('num_economico'),
            Telefono=data.get('telefono'),
            Tipotransporte=data.get('tipo_transporte'),
            Origen=data.get('origen'),
            Destino=data.get('destino'),
            Fechacreacion=data.get('fechacreacion'),
            Fechasalida=data.get('fechasalida'),
            Ayudante=data.get('ayudante'),
            CostoCotizacion=data.get('costo_cotizacion'),
            CostoTotal=data.get('costo_total'),
            Auditado=data.get('auditado', False)
        )
        
        db.session.add(transporte)
        db.session.commit()
        
        return jsonify(transporte.to_dict()), 201