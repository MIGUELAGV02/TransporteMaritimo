from extensions import db
from datetime import datetime

class Aereo(db.Model):
    __tablename__ = 'aereo'
    
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    Nombre = db.Column(db.String(45), nullable=True)
    Cliente = db.Column(db.String(100), nullable=True)
    Tipo_envio_despacho = db.Column(db.String(45), nullable=True)
    Tipo_Mercancia = db.Column(db.String(45), nullable=True)
    Transporte_Estadias = db.Column(db.Integer, nullable=True)
    Link_naviera = db.Column(db.String(255), nullable=True)
    
    Factura = db.Column(db.String(255), nullable=True)
    Listamapaque = db.Column(db.String(255), nullable=True)
    
    aduanacrigen = db.Column(db.String(45), nullable=True)
    aduanadestino = db.Column(db.String(45), nullable=True)
    transporteterrestre = db.Column(db.String(45), nullable=True)
    
    GuiaAerea = db.Column(db.String(100), nullable=True)
    Clave_de_Rastreo = db.Column(db.String(21), nullable=True)
    
    DiasAereos = db.Column(db.String(45), nullable=True)
    DiasAlmacenajes = db.Column(db.String(45), nullable=True)
    DiasTotales = db.Column(db.String(45), nullable=True)
    
    Fechasalida = db.Column(db.Date, nullable=True)
    Fechacreacion = db.Column(db.Date, nullable=True, default=datetime.utcnow)
    
    Paisorigen = db.Column(db.String(45), nullable=True)
    Paisdestino = db.Column(db.String(45), nullable=True)
    
    Fleteterrestre = db.Column(db.String(45), nullable=True)
    
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
            'aduanacrigen': self.aduanacrigen,
            'aduanadestino': self.aduanadestino,
            'transporteterrestre': self.transporteterrestre,
            'GuiaAerea': self.GuiaAerea,
            'Clave_de_Rastreo': self.Clave_de_Rastreo,
            'DiasAereos': self.DiasAereos,
            'DiasAlmacenajes': self.DiasAlmacenajes,
            'DiasTotales': self.DiasTotales,
            'Fechasalida': self.Fechasalida.isoformat() if self.Fechasalida else None,
            'Fechacreacion': self.Fechacreacion.isoformat() if self.Fechacreacion else None,
            'Paisorigen': self.Paisorigen,
            'Paisdestino': self.Paisdestino,
            'Fleteterrestre': self.Fleteterrestre,
            'CostoCotizacion': float(self.CostoCotizacion) if self.CostoCotizacion else None,
            'CostoTotal': float(self.CostoTotal) if self.CostoTotal else None,
            'Auditado': self.Auditado,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
