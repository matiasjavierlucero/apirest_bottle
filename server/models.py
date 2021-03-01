from marshmallow import fields,Schema
from peewee import *

#Models
db = SqliteDatabase('aimo.db')

class BaseModel(Model):
    class Meta:
        database = db

class TipoUsuario(BaseModel):
    nombre = CharField(unique=True)
    
class Usuario(BaseModel):
    nombre = CharField(unique=True)
    password = CharField()
    tipo=ForeignKeyField(TipoUsuario)

class Notas(BaseModel):
    nota = IntegerField()
    usuarionota = ForeignKeyField(Usuario,related_name='relationships')
    usuariocarga= ForeignKeyField(Usuario,related_name='related_to')



db.connect()
try:
    db.create_tables([TipoUsuario,Usuario,Notas])
except :
    pass