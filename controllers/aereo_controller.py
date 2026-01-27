from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from extensions import db
from models.aereo import Aereo
from datetime import datetime

aereo_bp = Blueprint('aereo', __name__, url_prefix='/api/aereo')

@aereo_bp.route('/', methods=['GET'])
@jwt_required()
def get_all():
    """Obtener todos los registros aéreos"""
    registros = Aereo.query.all()
    return jsonify({'data': [r.to_dict() for r in registros]}), 200

@aereo_bp.route('/<int:id>', methods=['GET'])
@jwt_required()
def get_one(id):
    """Obtener un registro aéreo por ID"""
    registro = Aereo.query.get(id)
    
    if not registro:
        return jsonify({'error': 'Registro no encontrado'}), 404
    
    return jsonify({'data': registro.to_dict()}), 200

@aereo_bp.route('/', methods=['POST'])
@jwt_required()
def create():
    """Crear un nuevo registro aéreo"""
    data = request.get_json()
    
    nuevo_registro = Aereo(
        Nombre=data.get('Nombre'),
        Cliente=data.get('Cliente'),
        Tipo_envio_despacho=data.get('Tipo_envio_despacho'),
        Tipo_Mercancia=data.get('Tipo_Mercancia'),
        Transporte_Estadias=data.get('Transporte_Estadias'),
        Link_naviera=data.get('Link_naviera'),
        Factura=data.get('Factura'),
        Listamapaque=data.get('Listamapaque'),
        aduanacrigen=data.get('aduanacrigen'),
        aduanadestino=data.get('aduanadestino'),
        transporteterrestre=data.get('transporteterrestre'),
        GuiaAerea=data.get('GuiaAerea'),
        Clave_de_Rastreo=data.get('Clave_de_Rastreo'),
        DiasAereos=data.get('DiasAereos'),
        DiasAlmacenajes=data.get('DiasAlmacenajes'),
        DiasTotales=data.get('DiasTotales'),
        Fechasalida=datetime.strptime(data['Fechasalida'], '%Y-%m-%d').date() if data.get('Fechasalida') else None,
        Fechacreacion=datetime.strptime(data['Fechacreacion'], '%Y-%m-%d').date() if data.get('Fechacreacion') else datetime.utcnow().date(),
        Paisorigen=data.get('Paisorigen'),
        Paisdestino=data.get('Paisdestino'),
        Fleteterrestre=data.get('Fleteterrestre'),
        CostoCotizacion=data.get('CostoCotizacion'),
        CostoTotal=data.get('CostoTotal'),
        Auditado=data.get('Auditado', False)
    )
    
    db.session.add(nuevo_registro)
    db.session.commit()
    
    return jsonify({
        'message': 'Registro creado exitosamente',
        'data': nuevo_registro.to_dict()
    }), 201

@aereo_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update(id):
    """Actualizar un registro aéreo"""
    registro = Aereo.query.get(id)
    
    if not registro:
        return jsonify({'error': 'Registro no encontrado'}), 404
    
    data = request.get_json()
    
    campos = ['Nombre', 'Cliente', 'Tipo_envio_despacho', 'Tipo_Mercancia',
              'Transporte_Estadias', 'Link_naviera', 'Factura', 'Listamapaque',
              'aduanacrigen', 'aduanadestino', 'transporteterrestre', 'GuiaAerea',
              'Clave_de_Rastreo', 'DiasAereos', 'DiasAlmacenajes', 'DiasTotales',
              'Paisorigen', 'Paisdestino', 'Fleteterrestre', 'CostoCotizacion',
              'CostoTotal', 'Auditado']
    
    for campo in campos:
        if campo in data:
            setattr(registro, campo, data[campo])
    
    if 'Fechasalida' in data and data['Fechasalida']:
        registro.Fechasalida = datetime.strptime(data['Fechasalida'], '%Y-%m-%d').date()
    if 'Fechacreacion' in data and data['Fechacreacion']:
        registro.Fechacreacion = datetime.strptime(data['Fechacreacion'], '%Y-%m-%d').date()
    
    db.session.commit()
    
    return jsonify({
        'message': 'Registro actualizado',
        'data': registro.to_dict()
    }), 200

@aereo_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete(id):
    """Eliminar un registro aéreo"""
    registro = Aereo.query.get(id)
    
    if not registro:
        return jsonify({'error': 'Registro no encontrado'}), 404
    
    db.session.delete(registro)
    db.session.commit()
    
    return jsonify({'message': 'Registro eliminado'}), 200
