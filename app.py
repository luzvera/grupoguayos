# crear rutas para denuncia, ubicaciones, estadisticas, conocenos
from flask import Flask, redirect, render_template, url_for, request
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField
from wtforms.validators import InputRequired 
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
Bootstrap(app)

@app.route('/')
def index():
    return render_template('index.html')



# @app.route('/Denuncias', methods=['GET','POST'] )
# def denuncias():
#     form = registerForm()
#     if form.validate_on_submit():
#         return 'form.html'

# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/database.sqlite3'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# db= SQLAlchemy(app)
# class basecita(db.Model):
#     id = db.Column(db.Integer, primary_key = True)
#     title = db.Column(db.String(80))
#     completed = db.Column(db.Boolean)


#     def __init__(self,title,completed):
#         self.title = title
#         self.completed = completed 

#     def __repr__(self):
#         return f'<Tarea con nombre: {self.title}'



# @app.route('/about')
# def about():
#     tareas = basecita.query.all()
#     return render_template('form.html', tareas=tareas)

# @app.route('/creartarea',methods=['POST'])
# def create():
#     titulo = request.form['tarea']
#     tarea = basecita(title=titulo,completed=False)
#     db.session.add(tarea)
#     db.session.commit()
#     return redirect(url_for('about'))


if __name__ == '__main__':
    #db.create_all()
    app.run(debug=True)