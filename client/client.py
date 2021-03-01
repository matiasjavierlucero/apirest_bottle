# Run with "python client.py"
from bottle import get, run, static_file, post, request,route,jinja2_view,Bottle    
from bottle.ext import beaker
import requests
import jwt


SECRET_KEY='eltestedematiasjavierlucero'

#El token la almacenare en una variable global, ya que no quiero usar Flask

Token=''
@get('/')
@jinja2_view('templates/index.html')
def index():
    return {}

@get('/register')
@jinja2_view('templates/register.html')
def register():
    return {}

@get('/login')
@jinja2_view('templates/login.html')
def login():
    return {}

@post('/login')
@jinja2_view('templates/register.html')
def login_post():
    usuario=request.forms['usuario']
    password=request.forms['password']
    auth_data = {'usuario': usuario, 'password': password}    
    url = "http://127.0.0.1:8000/login"
    headers = {
    'content-type': "application/json",
    'cache-control': "no-cache"
    }
    response= requests.request("POST", url, data=auth_data, headers=headers)
    response=response.json()
    global Token
    if response['tipoUsuario']==1:
        Token=response['token']
        return mitablero()
    else:
        Token=response['token']
        return tablerodocente()


@post('/register')
@jinja2_view('templates/register.html')
def register_post():
    usuario=request.forms['usuario']
    password=request.forms['password']

    register_data = {'usuario': usuario, 'password': password}    
    url = "http://127.0.0.1:8000/register"
    headers = {
    'content-type': "application/json",
    'cache-control': "no-cache"
    }
    response= requests.request("POST", url, data=register_data, headers=headers)
    response=response.json()
    if response['register']=='False':
        return {'mensaje':'Seleccione otro nombre'}
    else:
        return index()

@get('/mitablero')
@jinja2_view('templates/mitablero.html')
def mitablero():
    global Token
    url = "http://127.0.0.1:8000/mitablero"
    headers = {
    'content-type': "application/json",
    'cache-control': "no-cache",
    'x-access-token':Token
    }
    response_usuario= requests.request("GET", url, headers=headers)
    response_usuario= response_usuario.json()
   
    url = "http://127.0.0.1:8000/misnotas"
    headers = {
    'content-type': "application/json",
    'cache-control': "no-cache",
    'x-access-token':Token
    }
    response_notas= requests.request("GET", url, headers=headers)
    response_notas=response_notas.json()
    response_notas=response_notas['Notas'][0]
    
    return ({'data':response_usuario,'notas':response_notas,'session':'ok'})

@get('/tablerodocente')
@jinja2_view('templates/tablerodocente.html')
def tablerodocente():
    global Token
    url = "http://127.0.0.1:8000/alumnos"
    headers = {
    'content-type': "application/json",
    'cache-control': "no-cache",
    'x-access-token':Token
    }
    response_alumnos= requests.request("GET", url, headers=headers)
    response_alumnos=response_alumnos.json()
    return ({'Alumnos':response_alumnos,'session':'ok'})


@post('/guardarnota')
def guardarnota():
    global Token
    Alumno=request.forms['Alumno']
    Nota=request.forms['Nota']
    Nota_data = {'Alumno': Alumno, 'Nota': Nota}    
    url = "http://127.0.0.1:8000/guardarnota"
    headers = {
    'content-type': "application/json",
    'cache-control': "no-cache",
    'x-access-token':Token
    }
    response= requests.request("POST", url, data=Nota_data, headers=headers)
    response_notas=response.json()
    if response_notas['Nota']=='True':
        return misnotasdocente()
    
@get('/misnotasdocente')
@jinja2_view('templates/listanotas.html')
def misnotasdocente():
    global Token
    url = "http://127.0.0.1:8000/misnotasdocente"
    headers = {
    'content-type': "application/json",
    'cache-control': "no-cache",
    'x-access-token':Token
    }   
    response_notas= requests.request("GET", url,headers=headers)
    response_notas=response_notas.json()
    response_notas=response_notas['Notas'][0]
    return ({'Notas':response_notas,'session':'ok'})




@get('/logout')
@jinja2_view('templates/login.html')
def logout():
    Token=''
    return {}

run(host='localhost',port=5000,reloader=True,debug=True)
