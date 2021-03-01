# Run with "python server.py"
from bottle import run,get,static_file, post, request,route,jinja2_view,Bottle
import bottle
from bottle.ext import beaker
from peewee import *
from marshmallow import Schema, fields,ValidationError
from pprint import pprint
from datetime import datetime, timedelta
import jwt
from schemas import *
from models import Usuario,TipoUsuario,Notas
from functools import wraps


#FUNCION QUE SOLICITA EL TOKEN

SECRET_KEY='eltestedematiasjavierlucero'

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None        
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token'] #CABECERA QUE VALIDARA LA SESSION
        if not token:
            return ({"ERROR":"Token is missing"}),401
        try: 
            datatoken = jwt.decode(token, SECRET_KEY)
            userLogged=Usuario.select().where(Usuario.nombre==datatoken['nameUser'] and Usuario.password==datatoken['password']).first()
        except:
            return ({"ERROR":"Token is invalid or expired"}),401

        return f(userLogged, *args, **kwargs)

    return decorated


@post('/login')
def login_user():
    
    nombre = request.forms.get("usuario")  #Obtengo los datos del body
    password=request.forms.get("password")
    userLogged=Usuario.select().where(Usuario.nombre==nombre and Usuario.password==password).first()
    #Analizo usuario y contraseña que coincida con la base de datos
    if userLogged:
        token = jwt.encode({'idUser':userLogged.id,'nameUser': userLogged.nombre,'password':password, 'tipoUsuario': userLogged.tipo_id,'session':'Ok'}, SECRET_KEY)
        return ({'login':'True','username':userLogged.nombre,'tipoUsuario': userLogged.tipo_id,'token':token.decode("UTF-8"),'session':'Ok'})
    else:
        return ({"login":"Fale"})

@post('/register')
def register():
    nombre = request.forms.get("usuario")  #Obtengo los datos del body
    password=request.forms.get("password")
    tipo=request.forms.get("tipo")
    query=Usuario.select().where(Usuario.nombre==nombre).first()
    if query:
        return ({'register':'False'})
    else:
        user = Usuario(nombre=nombre,password=password,tipo=tipo)
        user.save()
        return ({'register':'True'})


@get('/mitablero')
@token_required
def mitablero(userLogged):
    nombre=userLogged.nombre
    return ({'Nombre':nombre,'Tipo':userLogged.tipo_id})

@get('/tablerodocente')
@token_required
def tablerodocente(userLogged):
    nombre=userLogged.nombre
    return ({'Nombre':nombre,'Tipo':userLogged.tipo_id})

   
@get('/misnotas')
@token_required
def misnotas(userLogged):
    query=Notas.select().where(Notas.usuarionota==userLogged.id)
    notas=nota_schema.dump(query,many=True)
    return ({'Notas': notas})


@get('/misnotasdocente')
@token_required
def misnotas(userLogged):
    query=Notas.select().where(Notas.usuariocarga==userLogged.id).order_by(Notas.usuarionota.asc())
    notas=nota_schema.dump(query,many=True)
    return ({'Notas': notas})

@get('/alumnos')
def users():
    Alumnos=Usuario.select().where(Usuario.tipo_id==1)
    Alumnos=user_schema.dump(Alumnos,many=True)
    return ({'Alumnos':Alumnos})

@post('/guardarnota')
@token_required
def guardarnota(userLogged):
    if userLogged.tipo_id != 2:
        return ({'Error','Es un alumno'},200)
    Alumno = request.forms.get("Alumno")  #Obtengo los datos del body
    Nota=request.forms.get("Nota")
    Profesor=userLogged.id
    user = Notas(nota=Nota,usuarionota_id=Alumno,usuariocarga_id=Profesor)
    user.save()
    return ({'Nota':'True'})

@post('/cargarnota/<id>')
@token_required
def cargarnota(userLogged,id):
    if userLogged.tipo_id !=2:
        return ({'Error':'Usted no es un profesor.No puede realizar carga'})
    nota=request.json['nota']
    alumno_id=id
    nuevanota = Notas(nota=nota, usuariocarga_id=userLogged.id,usuarionota_id=alumno_id)
    nuevanota.save() # bob is now stored in the database
    return {'Nota':nota,'Alumno':alumno_id,'Profesor':userLogged.id}






run(host='localhost', port=8000,reloader=True, debug=True)