import base64
from flask import Flask, jsonify, request,  render_template, send_file
from sqlalchemy import true
from config import config
from models import db, Bache
import folium
from folium import IFrame
from folium.plugins import MarkerCluster
import pandas as pd

def create_app(enviroment):
    app = Flask(__name__)

    app.config.from_object(enviroment)

    with app.app_context():
        db.init_app(app)
        db.create_all()

    return app

enviroment = config['development']

app = create_app(enviroment)



@app.route('/')
def index():
    return render_template('index.html')

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
    body_diccionario = request.form

    bache = Bache.create(
        direccion=body_diccionario['direccion'], 
        foto=request.files['foto'].filename,
        categoria=body_diccionario['categoria'], 
        latitud=body_diccionario['latitud'], 
        longitud=body_diccionario['longitud'], 
        nombre_bache=body_diccionario['nombre_bache'], 
        nombre_usuario=body_diccionario['nombre_usuario'],
    )
    file = request.files['foto']
    file.save(f"static/baches/{file.filename}")

    return render_template('index.html', bache= bache)

# Borrar un bache
@app.route('/api/v1/baches/<id>', methods=['DELETE'])
def delete_bache(id):
    bache = Bache.query.filter_by(id=id).first()
    if bache is None:
        return jsonify({'message': 'El bache no existe más :\'D'}), 404

    bache.delete()

    return jsonify({'bache': bache.json() })

@app.route('/mapa')
def mapa():
    #Inicializamos el mapa 
    map= folium.Map(
        location=[-25.302058396540463, -57.58112871603071],
        zoom_start=9,
        )
    cluster= MarkerCluster().add_to(map)
    lista_baches =Bache.query.all()
    extraccion = []
    for datos in lista_baches:
        extraccion.append([datos.latitud, datos.longitud, datos.nombre_bache, datos.foto, datos.categoria])

    for point in extraccion:
        mark= point[0],point[1]
        #print(point)
        # # point(i)
        foto= f"static/baches/{point[3]}"
        html = '<img width="360px" src="data:image/jpeg;base64,{}">'.format
        encoded = base64.b64encode(open(foto, 'rb').read())
        #print(foto)
        #print(foto)
        iframe= IFrame(html(encoded.decode()),width=360,height=240)
        categoria= point[4]
        print(categoria)
        validacion_agua= categoria=="Aquabache" or categoria =="Bachemar" or categoria== "Aquabache" or categoria== "Bachelor" or categoria =="Bacheton" 
        validacion_tierra= categoria== "Bachardo" or categoria== "Bacheto" or categoria=="Bacheinfierno" or categoria== "Bachenato" or categoria== "Bachero"
        if validacion_agua:
            folium.Marker(
            location=mark,
            popup=folium.Popup(iframe),
            icon=folium.Icon(color="blue"),
            tooltip=point[2]).add_to(cluster)
        elif validacion_tierra:
            folium.Marker(
            location=mark,
            popup=folium.Popup(iframe),
            icon=folium.Icon(color="red"),
            tooltip=point[2]
            ).add_to(cluster)
    return map._repr_html_()

def to_dict(row):
    if row is None:
        return None

    rtn_dict = dict()
    keys = row.__table__.columns.keys()
    for key in keys:
        rtn_dict[key] = getattr(row, key)
    return rtn_dict

@app.route('/excel', methods=['GET', 'POST'])
def exportexcel():
    data = Bache.query.all()
    data_list = [to_dict(item) for item in data]
    df = pd.DataFrame(data_list)
    filename = "extraccion.xlsx"
    print("Archivo: "+filename)

    writer = pd.ExcelWriter(filename)
    df.to_excel(writer, sheet_name='PalaEssap')
    writer.save()

    return send_file(filename)

if __name__== '__main__':
    app.run(debug= true)