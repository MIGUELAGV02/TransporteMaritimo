from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from extensions import db
from models.maritimo import Maritimo
from datetime import datetime

maritimo_bp = Blueprint('maritimo', __name__, url_prefix='/api/maritimo')

@maritimo_bp.route('/', methods=['GET'])
@jwt_required()
def get_all():
    """Obtener todos los registros marítimos"""
    registros = Maritimo.query.all()
    return jsonify({'data': [r.to_dict() for r in registros]}), 200

@maritimo_bp.route('/<int:id>', methods=['GET'])
@jwt_required()
def get_one(id):
    """Obtener un registro marítimo por ID"""
    registro = Maritimo.query.get(id)
    
    if not registro:
        return jsonify({'error': 'Registro no encontrado'}), 404
    
    return jsonify({'data': registro.to_dict()}), 200

@maritimo_bp.route('/', methods=['POST'])
@jwt_required()
def create():
    """Crear un nuevo registro marítimo"""
    data = request.get_json()
    
    nuevo_registro = Maritimo(
        Nombre=data.get('Nombre'),
        Cliente=data.get('Cliente'),
        Tipo_envio_despacho=data.get('Tipo_envio_despacho'),
        Tipo_Mercancia=data.get('Tipo_Mercancia'),
        Transporte_Estadias=data.get('Transporte_Estadias'),
        Link_naviera=data.get('Link_naviera'),
        factura=data.get('factura'),
        listaempaque=data.get('listaempaque'),
        status=data.get('status'),
        BL=data.get('BL'),
        Aduanaorigen=data.get('Aduanaorigen'),
        Aduanadestino=data.get('Aduanadestino'),
        Pedimento=data.get('Pedimento'),
        Transporteterrestre=data.get('Transporteterrestre'),
        Barco=data.get('Barco'),
        Diasmaritimos=data.get('Diasmaritimos'),
        Diasalmacenajes=data.get('Diasalmacenajes'),
        Diastotales=data.get('Diastotales'),
        Fechasalida=datetime.strptime(data['Fechasalida'], '%Y-%m-%d').date() if data.get('Fechasalida') else None,
        Fechacreacion=datetime.strptime(data['Fechacreacion'], '%Y-%m-%d').date() if data.get('Fechacreacion') else datetime.utcnow().date(),
        Paisdestino=data.get('Paisdestino'),
        Paisorigen=data.get('Paisorigen'),
        Guiaarea=data.get('Guiaarea'),
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

@maritimo_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update(id):
    """Actualizar un registro marítimo"""
    registro = Maritimo.query.get(id)
    
    if not registro:
        return jsonify({'error': 'Registro no encontrado'}), 404
    
    data = request.get_json()
    
    campos = ['Nombre', 'Cliente', 'Tipo_envio_despacho', 'Tipo_Mercancia', 
              'Transporte_Estadias', 'Link_naviera', 'factura', 'listaempaque',
              'status', 'BL', 'Aduanaorigen', 'Aduanadestino', 'Pedimento',
              'Transporteterrestre', 'Barco', 'Diasmaritimos', 'Diasalmacenajes',
              'Diastotales', 'Paisdestino', 'Paisorigen', 'Guiaarea', 
              'Fleteterrestre', 'CostoCotizacion', 'CostoTotal', 'Auditado']
    
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

@maritimo_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete(id):
    """Eliminar un registro marítimo"""
    registro = Maritimo.query.get(id)
    
    if not registro:
        return jsonify({'error': 'Registro no encontrado'}), 404
    
    db.session.delete(registro)
    db.session.commit()
    
    return jsonify({'message': 'Registro eliminado'}), 200
