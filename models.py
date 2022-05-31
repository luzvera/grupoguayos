from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Bache(db.Model):
    __tablename__ = 'baches'

    id = db.Column(db.Integer, primary_key=True)
    direccion = db.Column(db.String(50), nullable=False) 
    foto = db.Column(db.String(50), nullable=False, default='default.jpg')
    fecha = db.Column(db.DateTime(), nullable=False, default=db.func.current_timestamp())
    categoria = db.Column(db.String(50), nullable=False)
    latitud = db.Column(db.Float, nullable=False)
    longitud = db.Column(db.Float, nullable=False)
    nombre_bache = db.Column(db.String(50), nullable=False)
    nombre_usuario = db.Column(db.String(50), nullable=False)

    @classmethod
    def create(cls, nombre_bache, direccion, categoria, latitud, longitud, nombre_usuario):
            user = Bache(nombre_bache=nombre_bache, direccion=direccion, categoria=categoria, latitud=latitud, longitud=longitud, nombre_usuario=nombre_usuario)
            return user.save()

    def save(self):
            try:
                    db.session.add(self)
                    db.session.commit()

                    return self
            except Exception as e:
                    print(e)
                    return False

    def delete(self):
        try:
                db.session.delete(self)
                db.session.commit()

                return True
        except Exception as e:
                print(e)
                return False

    def json(self):
        return {
            'id': self.id,
            'direccion': self.direccion,
            'foto': self.foto,
            'fecha': self.fecha,
            'categoria': self.categoria,
            'latitud': self.latitud,
            'longitud': self.longitud,
            'nombre_bache': self.nombre_bache,
            'nombre_usuario': self.nombre_usuario
        }