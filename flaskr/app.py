from flaskr import create_app
from markupsafe import escape
from .modelos import db, Cancion, Album, Usuario, Medio
from .modelos import AlbumSchema, CancionSchema, UsuarioSchema
from flask_restful import Api
from .vistas import VistaCanciones, VistaCancion, VistaLogIn, VistaSignIn1, VistaSignIn2, VistaAlbum, VistaAlbumsUsuario, VistaCancionesAlbum
from flask_jwt_extended import JWTManager
from flask_cors import CORS


app = create_app('default')
app_context = app.app_context()
app_context.push()

db.init_app(app)
db.create_all()

cors = CORS(app)


api = Api(app)
api.add_resource(VistaCanciones, '/canciones')
api.add_resource(VistaCancion, '/cancion/<int:id_cancion>')
api.add_resource(VistaSignIn2, '/signin')
api.add_resource(VistaSignIn1, '/signin/<int:id_usuario>')
api.add_resource(VistaLogIn, '/login')
api.add_resource(VistaAlbumsUsuario, '/usuario/<int:id_usuario>/albumes')
api.add_resource(VistaAlbum, '/album/<int:id_album>')
api.add_resource(VistaCancionesAlbum, '/album/<int:id_album>/canciones')


jwt = JWTManager(app)


#PRUEBA

with app.app_context():
    '''
    c = Cancion(titulo='Prueba', minutos=2, segundos=25, interprete='Juanse')
    c2 = Cancion(titulo='Prueba2', minutos=2, segundos=25, interprete='Juanse')
    db.session.add(c)
    db.session.add(c2)
    db.session.commit()
    print(Cancion.query.all())
    '''
    '''
    u = Usuario(nombre_usuario='Juanse', contrasena='1234')
    a = Album(titulo='Prueba', anio=2020, descripcion='Prueba-', medio=Medio.CD)
    c = Cancion(titulo='Prueba', minutos=2, segundos=25, interprete='Juanse')
    u.albumes.append(a)
    a.canciones.append(c)
    db.session.add(u)
    db.session.add(c)
    db.session.commit()
    '''
    '''
    print(Usuario.query.all())
    print(Usuario.query.all()[0].albumes)
    db.session.delete(u)
    print(Usuario.query.all())
    print(Album.query.all())
    '''
    '''
    print(Album.query.all())
    print(Album.query.all()[0].canciones)
    print(Cancion.query.all())
    db.session.delete(a)
    print(Album.query.all())
    print(Cancion.query.all())
    '''

    '''
    print('ALBUMES')
    album_schema = AlbumSchema()
    A = Album(titulo='Prueba', anio=2020, descripcion='Prueba-', medio=Medio.CD)
    db.session.add(A)
    db.session.commit()
    print([album_schema.dumps(album) for album in Album.query.all()])

    print('CANCIONES')
    cancion_schema = CancionSchema()
    C = Cancion(titulo='Prueba', minutos=2, segundos=25, interprete='Juanse')
    db.session.add(C)
    db.session.commit()
    print([cancion_schema.dumps(cancion) for cancion in Cancion.query.all()])

    print('USUARIOS')
    usuario_schema = UsuarioSchema()
    U = Usuario(nombre_usuario='Juanse', contrasena='1234')
    db.session.add(U)
    db.session.commit()
    print([usuario_schema.dumps(usuario) for usuario in Usuario.query.all()])
    '''