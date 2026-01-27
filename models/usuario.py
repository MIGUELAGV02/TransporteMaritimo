from extensions import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class Usuario(db.Model):
    __tablename__ = 'usuarios'
    
    id_Usuarios = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    Nombre = db.Column(db.String(100), nullable=False)
    Apellido = db.Column(db.String(100), nullable=False)
    Contrasena = db.Column(db.String(255), unique=True, nullable=False)
    Rol = db.Column(db.Enum('superusuario', 'admin', 'usuario', 'tecnico'), default='usuario')
    Correo = db.Column(db.String(150), unique=True, nullable=False)
    Telefono = db.Column(db.String(20), nullable=True)
    Area = db.Column(db.String(100), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def set_password(self, password):
        self.Contrasena = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.Contrasena, password)
    
    def to_dict(self):
        return {
            'id_Usuarios': self.id_Usuarios,
            'Nombre': self.Nombre,
            'Apellido': self.Apellido,
            'Rol': self.Rol,
            'Correo': self.Correo,
            'Telefono': self.Telefono,
            'Area': self.Area,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
