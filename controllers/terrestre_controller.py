from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from extensions import db
from models.terrestre import Terrestre
from datetime import datetime

terrestre_bp = Blueprint('terrestre', __name__, url_prefix='/api/terrestre')

@terrestre_bp.route('/', methods=['GET'])
@jwt_required()
def get_all():
    """Obtener todos los registros terrestres"""
    registros = Terrestre.query.all()
    return jsonify({'data': [r.to_dict() for r in registros]}), 200

@terrestre_bp.route('/<int:id>', methods=['GET'])
@jwt_required()
def get_one(id):
    """Obtener un registro terrestre por ID"""
    registro = Terrestre.query.get(id)
    
    if not registro:
        return jsonify({'error': 'Registro no encontrado'}), 404
    
    return jsonify({'data': registro.to_dict()}), 200

@terrestre_bp.route('/', methods=['POST'])
@jwt_required()
def create():
    """Crear un nuevo registro terrestre"""
    data = request.get_json()
    
    nuevo_registro = Terrestre(
        Nombre=data.get('Nombre'),
        Cliente=data.get('Cliente'),
        Tipo_envio_despacho=data.get('Tipo_envio_despacho'),
        Tipo_Mercancia=data.get('Tipo_Mercancia'),
        Transporte_Estadias=data.get('Transporte_Estadias'),
        Link_naviera=data.get('Link_naviera'),
        Factura=data.get('Factura'),
        Listamapaque=data.get('Listamapaque'),
        Transporte=data.get('Transporte'),
        Placas=data.get('Placas'),
        Cedula=data.get('Cedula'),
        Num_economico=data.get('Num_economico'),
        Telefono=data.get('Telefono'),
        Tipotransporte=data.get('Tipotransporte'),
        Origen=data.get('Origen'),
        Destino=data.get('Destino'),
        Fechacreacion=datetime.strptime(data['Fechacreacion'], '%Y-%m-%d').date() if data.get('Fechacreacion') else datetime.utcnow().date(),
        Fechasalida=datetime.strptime(data['Fechasalida'], '%Y-%m-%d').date() if data.get('Fechasalida') else None,
        Ayudante=data.get('Ayudante'),
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

@terrestre_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update(id):
    """Actualizar un registro terrestre"""
    registro = Terrestre.query.get(id)
    
    if not registro:
        return jsonify({'error': 'Registro no encontrado'}), 404
    
    data = request.get_json()
    
    campos = ['Nombre', 'Cliente', 'Tipo_envio_despacho', 'Tipo_Mercancia',
              'Transporte_Estadias', 'Link_naviera', 'Factura', 'Listamapaque',
              'Transporte', 'Placas', 'Cedula', 'Num_economico', 'Telefono',
              'Tipotransporte', 'Origen', 'Destino', 'Ayudante',
              'CostoCotizacion', 'CostoTotal', 'Auditado']
    
    for campo in campos:
        if campo in data:
            setattr(registro, campo, data[campo])
    
    if 'Fechacreacion' in data and data['Fechacreacion']:
        registro.Fechacreacion = datetime.strptime(data['Fechacreacion'], '%Y-%m-%d').date()
    if 'Fechasalida' in data and data['Fechasalida']:
        registro.Fechasalida = datetime.strptime(data['Fechasalida'], '%Y-%m-%d').date()
    
    db.session.commit()
    
    return jsonify({
        'message': 'Registro actualizado',
        'data': registro.to_dict()
    }), 200

@terrestre_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete(id):
    """Eliminar un registro terrestre"""
    registro = Terrestre.query.get(id)
    
    if not registro:
        return jsonify({'error': 'Registro no encontrado'}), 404
    
    db.session.delete(registro)
    db.session.commit()
    
    return jsonify({'message': 'Registro eliminado'}), 200
