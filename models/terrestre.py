from extensions import db
from datetime import datetime

class Terrestre(db.Model):
    __tablename__ = 'terrestre'
    
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    Nombre = db.Column(db.String(45), nullable=True)
    Cliente = db.Column(db.String(100), nullable=True)
    Tipo_envio_despacho = db.Column(db.String(45), nullable=True)
    Tipo_Mercancia = db.Column(db.String(45), nullable=True)
    Transporte_Estadias = db.Column(db.Integer, nullable=True)
    Link_naviera = db.Column(db.String(255), nullable=True)
    
    Factura = db.Column(db.String(255), nullable=True)
    Listamapaque = db.Column(db.String(255), nullable=True)
    
    Transporte = db.Column(db.String(45), nullable=True)
    Placas = db.Column(db.String(45), nullable=True)
    Cedula = db.Column(db.String(45), nullable=True)
    Num_economico = db.Column(db.Integer, nullable=True)
    Telefono = db.Column(db.String(20), nullable=True)
    
    Tipotransporte = db.Column(db.String(45), nullable=True)
    Origen = db.Column(db.String(45), nullable=True)
    Destino = db.Column(db.String(45), nullable=True)
    
    Fechacreacion = db.Column(db.Date, nullable=True, default=datetime.utcnow)
    Fechasalida = db.Column(db.Date, nullable=True)
    
    Ayudante = db.Column(db.String(45), nullable=True)
    
    CostoCotizacion = db.Column(db.Numeric(15, 2), nullable=True)
    CostoTotal = db.Column(db.Numeric(15, 2), nullable=True)
    
    Auditado = db.Column(db.Boolean, default=False)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'Nombre': self.Nombre,
            'Cliente': self.Cliente,
            'Tipo_envio_despacho': self.Tipo_envio_despacho,
            'Tipo_Mercancia': self.Tipo_Mercancia,
            'Transporte_Estadias': self.Transporte_Estadias,
            'Link_naviera': self.Link_naviera,
            'Factura': self.Factura,
            'Listamapaque': self.Listamapaque,
            'Transporte': self.Transporte,
            'Placas': self.Placas,
            'Cedula': self.Cedula,
            'Num_economico': self.Num_economico,
            'Telefono': self.Telefono,
            'Tipotransporte': self.Tipotransporte,
            'Origen': self.Origen,
            'Destino': self.Destino,
            'Fechacreacion': self.Fechacreacion.isoformat() if self.Fechacreacion else None,
            'Fechasalida': self.Fechasalida.isoformat() if self.Fechasalida else None,
            'Ayudante': self.Ayudante,
            'CostoCotizacion': float(self.CostoCotizacion) if self.CostoCotizacion else None,
            'CostoTotal': float(self.CostoTotal) if self.CostoTotal else None,
            'Auditado': self.Auditado,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
