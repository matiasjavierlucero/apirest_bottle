from marshmallow import fields,Schema,ValidationError

#Validaciones
def validar_nota(n):
    if not 1<n< 10:
        raise ValidationError("Debe ingresar una nota entre 1 y 10")
    
#Schemas  
class TUserSchema(Schema):
    id = fields.Integer(dump_only=True)
    nombre=fields.String()
    
tuser_schema = TUserSchema()

class UserSchema(Schema):
    id = fields.Integer(dump_only=True)
    nombre=fields.String()
    password=fields.String()
    tipo=fields.Nested(TUserSchema())

user_schema = UserSchema()

class NotasSchema(Schema):
    id = fields.Integer(dump_only=True)
    nota=fields.Integer(validate=validar_nota)
    usuarionota=fields.Nested(UserSchema())
    usuariocarga=fields.Nested(UserSchema())

nota_schema=NotasSchema()



#class ChildSchema(Schema):
#    id = fields.Str()
#    name = fields.Str()
#    # Use lambda functions when you need two-way nesting or self-nesting
#    parent = fields.Nested(lambda: ParentSchema(only=("id",)), dump_only=True)
#    siblings = fields.List(fields.Nested(lambda: ChildSchema(only=("id", "name"))))
#
#class ParentSchema(Schema):
#    id = fields.Str()
#    children = fields.List(
#        fields.Nested(ChildSchema(only=("id", "parent", "siblings")))
#    )
#    spouse = fields.Nested(lambda: ParentSchema(only=("id",)))