from flask import Blueprint, request, jsonify, send_from_directory, current_app
from flask_jwt_extended import jwt_required
from extensions import db
from models.maritimo import Maritimo
from datetime import datetime
import os
from werkzeug.utils import secure_filename
import uuid

maritimo_bp = Blueprint('maritimo', __name__, url_prefix='/api/maritimo')

def allowed_file(filename):
    """Verificar si el archivo es un PDF"""
    ALLOWED_EXTENSIONS = {'pdf'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_upload_folder():
    """Obtener la carpeta de uploads"""
    upload_folder = current_app.config.get('UPLOAD_FOLDER')
    if not upload_folder:
        upload_folder = os.path.join(os.path.dirname(__file__), '..', 'uploads')
        os.makedirs(upload_folder, exist_ok=True)
    return upload_folder

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
    """Crear un nuevo registro marítimo con archivos PDF"""
    try:
        # Inicializar datos
        data = {}
        
        # Obtener datos del formulario (form-data)
        if request.form:
            data = request.form.to_dict()
        
        # Obtener archivos
        files = request.files
        
        # Procesar archivos PDF
        upload_folder = get_upload_folder()
        
        for file_field in ['factura', 'listaempaque', 'pedimento']:
            if file_field in files:
                file = files[file_field]
                if file and file.filename and allowed_file(file.filename):
                    # Generar nombre único
                    original_filename = secure_filename(file.filename)
                    unique_filename = f"{uuid.uuid4().hex}_{original_filename}"
                    
                    # Guardar archivo
                    file_path = os.path.join(upload_folder, unique_filename)
                    file.save(file_path)
                    
                    # Guardar nombre en los datos
                    data[file_field] = unique_filename
        
        # Manejo de fechas
        fecha_salida_almacen = None
        fecha_salida_barco = None
        fecha_creacion = None
        
        if data.get('FechaSalidaAlmacen'):
            fecha_salida_almacen = datetime.strptime(data['FechaSalidaAlmacen'], '%Y-%m-%d').date()
        if data.get('FechaSalidaBarco'):
            fecha_salida_barco = datetime.strptime(data['FechaSalidaBarco'], '%Y-%m-%d').date()
        if data.get('Fechacreacion'):
            fecha_creacion = datetime.strptime(data['Fechacreacion'], '%Y-%m-%d').date()
        else:
            fecha_creacion = datetime.utcnow().date()
        
        # Convertir campos numéricos
        numeric_fields = ['Transporte_Estadias', 'Diasmaritimos', 'Diasalmacenajes', 'DiasLibres', 'CostoCotizacion', 'CostoTotal']
        for field in numeric_fields:
            if field in data and data[field]:
                try:
                    data[field] = float(data[field])
                except:
                    data[field] = None
        
        # Convertir campo booleano
        if 'Auditado' in data:
            data['Auditado'] = data['Auditado'].lower() in ['true', '1', 'yes']
        
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
            # Nuevos campos de transporte terrestre
            EmpresaTransporteTerrestre=data.get('EmpresaTransporteTerrestre'),
            OperadorTransporteTerrestre=data.get('OperadorTransporteTerrestre'),
            PlacasTransporteTerrestre=data.get('PlacasTransporteTerrestre'),
            NoEconomicoTransporteTerrestre=data.get('NoEconomicoTransporteTerrestre'),
            TipoDeTransporteTerrestre=data.get('TipoDeTransporteTerrestre'),
            Barco=data.get('Barco'),
            Diasmaritimos=data.get('Diasmaritimos'),
            Diasalmacenajes=data.get('Diasalmacenajes'),
            DiasLibres=data.get('DiasLibres'),  # Cambiado de Diastotales
            # Campos de fechas actualizados
            FechaSalidaAlmacen=fecha_salida_almacen,
            FechaSalidaBarco=fecha_salida_barco,
            Fechacreacion=fecha_creacion,
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
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@maritimo_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update(id):
    """Actualizar un registro marítimo con archivos"""
    try:
        registro = Maritimo.query.get(id)
        
        if not registro:
            return jsonify({'error': 'Registro no encontrado'}), 404
        
        # Inicializar datos
        data = {}
        
        # Obtener datos del formulario (form-data)
        if request.form:
            data = request.form.to_dict()
        
        # Obtener archivos
        files = request.files
        
        # Procesar archivos PDF
        upload_folder = get_upload_folder()
        
        for file_field in ['factura', 'listaempaque', 'pedimento']:
            if file_field in files:
                file = files[file_field]
                if file and file.filename and allowed_file(file.filename):
                    # Eliminar archivo anterior si existe
                    old_filename = getattr(registro, file_field, None)
                    if old_filename:
                        old_path = os.path.join(upload_folder, old_filename)
                        if os.path.exists(old_path):
                            os.remove(old_path)
                    
                    # Generar nombre único
                    original_filename = secure_filename(file.filename)
                    unique_filename = f"{uuid.uuid4().hex}_{original_filename}"
                    
                    # Guardar archivo
                    file_path = os.path.join(upload_folder, unique_filename)
                    file.save(file_path)
                    
                    # Actualizar campo
                    setattr(registro, file_field, unique_filename)
        
        # Lista de campos a actualizar
        campos = [
            'Nombre', 'Cliente', 'Tipo_envio_despacho', 'Tipo_Mercancia',
            'Transporte_Estadias', 'Link_naviera', 'status', 'BL',
            'Aduanaorigen', 'Aduanadestino',
            # Nuevos campos de transporte terrestre
            'EmpresaTransporteTerrestre', 'OperadorTransporteTerrestre',
            'PlacasTransporteTerrestre', 'NoEconomicoTransporteTerrestre',
            'TipoDeTransporteTerrestre',
            'Barco', 'Diasmaritimos', 'Diasalmacenajes',
            'DiasLibres',  # Cambiado de Diastotales
            'Paisdestino', 'Paisorigen', 'Guiaarea', 
            'Fleteterrestre', 'CostoCotizacion', 'CostoTotal', 'Auditado'
        ]
        
        # Actualizar campos regulares
        for campo in campos:
            if campo in data:
                # Convertir tipos de datos
                if campo in ['Transporte_Estadias', 'Diasmaritimos', 'Diasalmacenajes', 'DiasLibres', 'CostoCotizacion', 'CostoTotal']:
                    try:
                        setattr(registro, campo, float(data[campo]) if data[campo] else None)
                    except:
                        setattr(registro, campo, None)
                elif campo == 'Auditado':
                    setattr(registro, campo, data[campo].lower() in ['true', '1', 'yes'])
                else:
                    setattr(registro, campo, data[campo] if data[campo] else None)
        
        # Manejar campos de fecha especiales
        if 'FechaSalidaAlmacen' in data:
            if data['FechaSalidaAlmacen']:
                registro.FechaSalidaAlmacen = datetime.strptime(data['FechaSalidaAlmacen'], '%Y-%m-%d').date()
            else:
                registro.FechaSalidaAlmacen = None
                
        if 'FechaSalidaBarco' in data:
            if data['FechaSalidaBarco']:
                registro.FechaSalidaBarco = datetime.strptime(data['FechaSalidaBarco'], '%Y-%m-%d').date()
            else:
                registro.FechaSalidaBarco = None
                
        if 'Fechacreacion' in data and data['Fechacreacion']:
            registro.Fechacreacion = datetime.strptime(data['Fechacreacion'], '%Y-%m-%d').date()
        
        db.session.commit()
        
        return jsonify({
            'message': 'Registro actualizado',
            'data': registro.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@maritimo_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete(id):
    """Eliminar un registro marítimo y sus archivos"""
    try:
        registro = Maritimo.query.get(id)
        
        if not registro:
            return jsonify({'error': 'Registro no encontrado'}), 404
        
        # Eliminar archivos asociados
        upload_folder = get_upload_folder()
        
        for file_field in ['factura', 'listaempaque', 'Pedimento']:
            filename = getattr(registro, file_field, None)
            if filename:
                file_path = os.path.join(upload_folder, filename)
                if os.path.exists(file_path):
                    os.remove(file_path)
        
        db.session.delete(registro)
        db.session.commit()
        
        return jsonify({'message': 'Registro eliminado'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@maritimo_bp.route('/uploads/<filename>', methods=['GET'])
@jwt_required()
def serve_pdf(filename):
    """Servir archivos PDF"""
    try:
        upload_folder = get_upload_folder()
        file_path = os.path.join(upload_folder, filename)
        
        if not os.path.exists(file_path):
            return jsonify({'error': 'Archivo no encontrado'}), 404
        
        return send_from_directory(upload_folder, filename, as_attachment=False)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@maritimo_bp.route('/view-pdf/<int:id>/<document_type>', methods=['GET'])
@jwt_required()
def view_pdf(id, document_type):
    """Obtener información del PDF para visualización"""
    try:
        registro = Maritimo.query.get(id)
        
        if not registro:
            return jsonify({'error': 'Registro no encontrado'}), 404
        
        # Mapear tipos de documentos a campos
        doc_map = {
            'factura': 'factura',
            'listaempaque': 'listaempaque',
            'pedimento': 'Pedimento'
        }
        
        if document_type not in doc_map:
            return jsonify({'error': 'Tipo de documento inválido'}), 400
        
        field_name = doc_map[document_type]
        filename = getattr(registro, field_name)
        
        if not filename:
            return jsonify({'error': 'Documento no disponible'}), 404
        
        # Verificar que el archivo existe
        upload_folder = get_upload_folder()
        file_path = os.path.join(upload_folder, filename)
        
        if not os.path.exists(file_path):
            return jsonify({'error': 'Archivo físico no encontrado'}), 404
        
        return jsonify({
            'filename': filename,
            'original_filename': filename.split('_', 1)[1] if '_' in filename else filename,
            'download_url': f'/api/maritimo/uploads/{filename}?download=true',
            'view_url': f'/api/maritimo/uploads/{filename}',
            'file_size': os.path.getsize(file_path)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500