from extensions import db
from datetime import datetime

class Maritimo(db.Model):
    __tablename__ = 'maritimo'
    
    idContenedores = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    Nombre = db.Column(db.String(255), nullable=True)
    Cliente = db.Column(db.String(255), nullable=True)
    Tipo_envio_despacho = db.Column(db.String(45), nullable=True)
    Tipo_Mercancia = db.Column(db.String(45), nullable=True)
    Transporte_Estadias = db.Column(db.Integer, nullable=True)
    Link_naviera = db.Column(db.String(255), nullable=True)
    
    factura = db.Column(db.String(255), nullable=True)
    listaempaque = db.Column(db.String(255), nullable=True)
    
    status = db.Column(db.String(250), nullable=True)
    BL = db.Column(db.String(100), nullable=True)
    Aduanaorigen = db.Column(db.String(45), nullable=True)
    Aduanadestino = db.Column(db.String(45), nullable=True)
    Pedimento = db.Column(db.String(100), nullable=True)
    Transporteterrestre = db.Column(db.String(45), nullable=True)
    
    Barco = db.Column(db.String(45), nullable=True)
    Diasmaritimos = db.Column(db.Integer, nullable=True)
    Diasalmacenajes = db.Column(db.Integer, nullable=True)
    Diastotales = db.Column(db.Integer, nullable=True)
    
    Fechasalida = db.Column(db.Date, nullable=True)
    Fechacreacion = db.Column(db.Date, nullable=True, default=datetime.utcnow)
    Paisdestino = db.Column(db.String(45), nullable=True)
    Paisorigen = db.Column(db.String(45), nullable=True)
    Guiaarea = db.Column(db.String(45), nullable=True)
    Fleteterrestre = db.Column(db.String(45), nullable=True)
    
    CostoCotizacion = db.Column(db.Numeric(15, 2), nullable=True)
    CostoTotal = db.Column(db.Numeric(15, 2), nullable=True)
    
    Auditado = db.Column(db.Boolean, default=False)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'idContenedores': self.idContenedores,
            'Nombre': self.Nombre,
            'Cliente': self.Cliente,
            'Tipo_envio_despacho': self.Tipo_envio_despacho,
            'Tipo_Mercancia': self.Tipo_Mercancia,
            'Transporte_Estadias': self.Transporte_Estadias,
            'Link_naviera': self.Link_naviera,
            'factura': self.factura,
            'listaempaque': self.listaempaque,
            'status': self.status,
            'BL': self.BL,
            'Aduanaorigen': self.Aduanaorigen,
            'Aduanadestino': self.Aduanadestino,
            'Pedimento': self.Pedimento,
            'Transporteterrestre': self.Transporteterrestre,
            'Barco': self.Barco,
            'Diasmaritimos': self.Diasmaritimos,
            'Diasalmacenajes': self.Diasalmacenajes,
            'Diastotales': self.Diastotales,
            'Fechasalida': self.Fechasalida.isoformat() if self.Fechasalida else None,
            'Fechacreacion': self.Fechacreacion.isoformat() if self.Fechacreacion else None,
            'Paisdestino': self.Paisdestino,
            'Paisorigen': self.Paisorigen,
            'Guiaarea': self.Guiaarea,
            'Fleteterrestre': self.Fleteterrestre,
            'CostoCotizacion': float(self.CostoCotizacion) if self.CostoCotizacion else None,
            'CostoTotal': float(self.CostoTotal) if self.CostoTotal else None,
            'Auditado': self.Auditado,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
