from flask import Flask, jsonify, request
from config import config
from models import db, Bache

def create_app(enviroment):
    app = Flask(__name__)

    app.config.from_object(enviroment)

    with app.app_context():
        db.init_app(app)
        db.create_all()

    return app

enviroment = config['development']

app = create_app(enviroment)

# Traer todos los baches
@app.route('/api/v1/baches', methods=['GET'])
def get_baches():
    baches = [ bache.json() for bache in Bache.query.all() ]
    return jsonify({'baches': baches })


# Traer un bache
@app.route('/api/v1/baches/<id>', methods=['GET'])
def get_bache(id):
    bache = Bache.query.filter_by(id=id).first()
    if bache is None:
        return jsonify({'message': 'El bache existe más :\'D'}), 404

    return jsonify({'bache': bache.json() })

# Crear un bache
@app.route('/api/v1/baches/', methods=['POST'])
def create_bache():
    body_diccionario = request.get_json(force=True)

    bache = Bache.create(direccion=body_diccionario['direccion'], categoria=body_diccionario['categoria'], latitud=body_diccionario['latitud'], longitud=body_diccionario['longitud'], nombre_bache=body_diccionario['nombre_bache'], nombre_usuario=body_diccionario['nombre_usuario'])

    return jsonify({'bache': bache.json()})

# Borrar un bache
@app.route('/api/v1/baches/<id>', methods=['DELETE'])
def delete_bache(id):
    bache = Bache.query.filter_by(id=id).first()
    if bache is None:
        return jsonify({'message': 'El bache no existe más :\'D'}), 404

    bache.delete()

    return jsonify({'bache': bache.json() })

if __name__ == '__main__':
    app.run(debug=True)