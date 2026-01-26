from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Usuario(db.Model):
    __tablename__ = 'unitarios'
    
    ID = db.Column(db.Integer, primary_key=True)
    Nombre = db.Column(db.String(45))
    Apellido = db.Column(db.String(45))
    Contraseña = db.Column(db.String(255))  # Ampliado para soportar hashes
    R01 = db.Column(db.String(45))
    Correo = db.Column(db.String(45))
    Telefono = db.Column(db.Integer)
    Área = db.Column(db.String(45))
    
    def to_dict(self):
        return {
            'id': self.ID,
            'nombre': self.Nombre,
            'apellido': self.Apellido,
            'correo': self.Correo,
            'telefono': self.Telefono,
            'area': self.Área,
            'r01': self.R01
        }

class Reporte(db.Model):
    __tablename__ = 'reportes'
    
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100))
    descripcion = db.Column(db.Text)
    tipo = db.Column(db.String(45))
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_modificacion = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    estado = db.Column(db.String(45))
    archivo = db.Column(db.LargeBinary)  # BLOB
    usuario_id = db.Column(db.Integer, db.ForeignKey('unitarios.ID'))
    contenedor_id = db.Column(db.Integer)
    aereo_id = db.Column(db.Integer)
    transporteterrestre_id = db.Column(db.Integer)
    
    usuario = db.relationship('Usuario', backref='reportes')
    
    def to_dict(self):
        return {
            'id': self.id,
            'titulo': self.titulo,
            'descripcion': self.descripcion,
            'tipo': self.tipo,
            'fecha_creacion': self.fecha_creacion.isoformat() if self.fecha_creacion else None,
            'fecha_modificacion': self.fecha_modificacion.isoformat() if self.fecha_modificacion else None,
            'estado': self.estado,
            'usuario_id': self.usuario_id,
            'contenedor_id': self.contenedor_id,
            'aereo_id': self.aereo_id,
            'transporteterrestre_id': self.transporteterrestre_id
        }

class Maritimo(db.Model):
    __tablename__ = 'maritimos'
    
    Id = db.Column(db.Integer, primary_key=True)
    Nombre = db.Column(db.String(45))
    Cliente = db.Column(db.String(100))
    Tipo_envio_despacio = db.Column(db.String(45))
    Tipo_Mercancia = db.Column(db.String(45))
    Transporte_Estadias = db.Column(db.Integer)
    Link_naviera = db.Column(db.String(255))
    Factura = db.Column(db.LargeBinary)  # BLOB
    Listamapaque = db.Column(db.LargeBinary)  # BLOB
    aduanacofigen = db.Column(db.String(45))
    aduanadesino = db.Column(db.String(45))
    transporteterrestre = db.Column(db.String(45))
    BL = db.Column(db.Integer)
    Disamaritinos = db.Column(db.Integer)
    Dislomacensis = db.Column(db.Integer)
    Diastotales = db.Column(db.Integer)
    Barco = db.Column(db.String(45))
    Fechasalida = db.Column(db.Date)
    Fechacreacion = db.Column(db.Date)
    Paísdestino = db.Column(db.String(45))
    Paisorigen = db.Column(db.String(45))
    Guiaarea = db.Column(db.String(45))
    Fleteterrestre = db.Column(db.String(45))
    CostoCotizacion = db.Column(db.Integer)
    CostoTotal = db.Column(db.Integer)
    
    def to_dict(self):
        return {
            'id': self.Id,
            'nombre': self.Nombre,
            'cliente': self.Cliente,
            'tipo_envio_despacio': self.Tipo_envio_despacio,
            'tipo_mercancia': self.Tipo_Mercancia,
            'transporte_estadias': self.Transporte_Estadias,
            'link_naviera': self.Link_naviera,
            'aduanacofigen': self.aduanacofigen,
            'aduanadesino': self.aduanadesino,
            'transporte_terrestre': self.transporteterrestre,
            'bl': self.BL,
            'disamaritinos': self.Disamaritinos,
            'dislomacensis': self.Dislomacensis,
            'diastotales': self.Diastotales,
            'barco': self.Barco,
            'fechasalida': self.Fechasalida.isoformat() if self.Fechasalida else None,
            'fechacreacion': self.Fechacreacion.isoformat() if self.Fechacreacion else None,
            'pais_destino': self.Paísdestino,
            'pais_origen': self.Paisorigen,
            'guia_area': self.Guiaarea,
            'flete_terrestre': self.Fleteterrestre,
            'costo_cotizacion': self.CostoCotizacion,
            'costo_total': self.CostoTotal
        }

class Aereo(db.Model):
    __tablename__ = 'aereo'
    
    id = db.Column(db.Integer, primary_key=True)
    Nombre = db.Column(db.String(45))
    Cliente = db.Column(db.String(100))
    Tipo_envio_despacio = db.Column(db.String(45))
    Tipo_Mercancia = db.Column(db.String(45))
    Transporte_Estadias = db.Column(db.Integer)
    Link_naviera = db.Column(db.String(255))
    Factura = db.Column(db.LargeBinary)  # BLOB
    Listamapaque = db.Column(db.LargeBinary)  # BLOB
    aduanacofigen = db.Column(db.String(45))
    aduanadesino = db.Column(db.String(45))
    transporteterrestre = db.Column(db.String(45))
    GuiaAerea = db.Column(db.Integer)
    Clave_de_Rastreo = db.Column(db.String(21))
    Disamaritinos = db.Column(db.Integer)
    Dislomacensis = db.Column(db.Integer)
    Diastotales = db.Column(db.Integer)
    Fechasalida = db.Column(db.Date)
    Fechacreacion = db.Column(db.Date)
    Paísdestino = db.Column(db.String(45))
    Paisorigen = db.Column(db.String(45))
    Fleteterrestre = db.Column(db.String(45))
    CostoCotizacion = db.Column(db.Integer)
    CostoTotal = db.Column(db.Integer)
    Auditado = db.Column(db.Boolean, default=False)
    
    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.Nombre,
            'cliente': self.Cliente,
            'tipo_envio_despacio': self.Tipo_envio_despacio,
            'tipo_mercancia': self.Tipo_Mercancia,
            'transporte_estadias': self.Transporte_Estadias,
            'link_naviera': self.Link_naviera,
            'aduanacofigen': self.aduanacofigen,
            'aduanadesino': self.aduanadesino,
            'transporte_terrestre': self.transporteterrestre,
            'guia_aerea': self.GuiaAerea,
            'clave_rastreo': self.Clave_de_Rastreo,
            'disamaritinos': self.Disamaritinos,
            'dislomacensis': self.Dislomacensis,
            'diastotales': self.Diastotales,
            'fechasalida': self.Fechasalida.isoformat() if self.Fechasalida else None,
            'fechacreacion': self.Fechacreacion.isoformat() if self.Fechacreacion else None,
            'pais_destino': self.Paísdestino,
            'pais_origen': self.Paisorigen,
            'flete_terrestre': self.Fleteterrestre,
            'costo_cotizacion': self.CostoCotizacion,
            'costo_total': self.CostoTotal,
            'auditado': self.Auditado
        }

class TransporteTerrestre(db.Model):
    __tablename__ = 'transporteterrestre'
    
    id = db.Column(db.Integer, primary_key=True)
    Nombre = db.Column(db.String(45))
    Cliente = db.Column(db.String(100))
    Tipo_envio_despacio = db.Column(db.String(45))
    Tipo_Mercancia = db.Column(db.String(45))
    Transporte_Estadias = db.Column(db.Integer)
    Link_naviera = db.Column(db.String(255))
    Factura = db.Column(db.LargeBinary)  # BLOB
    Listamapaque = db.Column(db.LargeBinary)  # BLOB
    Transporte = db.Column(db.String(45))
    Placas = db.Column(db.String(45))
    Chofer = db.Column(db.String(45))
    Num_económico = db.Column(db.Integer)
    Telefono = db.Column(db.Integer)
    Tipotransporte = db.Column(db.String(45))
    Origen = db.Column(db.String(45))
    Destino = db.Column(db.String(45))
    Fechacreacion = db.Column(db.Date)
    Fechasalida = db.Column(db.Date)
    Ayudante = db.Column(db.String(45))
    CostoCotizacion = db.Column(db.Integer)
    CostoTotal = db.Column(db.Integer)
    Auditado = db.Column(db.Boolean, default=False)
    
    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.Nombre,
            'cliente': self.Cliente,
            'tipo_envio_despacio': self.Tipo_envio_despacio,
            'tipo_mercancia': self.Tipo_Mercancia,
            'transporte_estadias': self.Transporte_Estadias,
            'link_naviera': self.Link_naviera,
            'transporte': self.Transporte,
            'placas': self.Placas,
            'chofer': self.Chofer,
            'num_economico': self.Num_económico,
            'telefono': self.Telefono,
            'tipo_transporte': self.Tipotransporte,
            'origen': self.Origen,
            'destino': self.Destino,
            'fechacreacion': self.Fechacreacion.isoformat() if self.Fechacreacion else None,
            'fechasalida': self.Fechasalida.isoformat() if self.Fechasalida else None,
            'ayudante': self.Ayudante,
            'costo_cotizacion': self.CostoCotizacion,
            'costo_total': self.CostoTotal,
            'auditado': self.Auditado
        }