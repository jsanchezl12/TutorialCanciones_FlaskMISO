from flask_restful import Resource
from  ..modelos import db, Cancion, CancionSchema, Album, AlbumSchema, Usuario, UsuarioSchema
from flask import request
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import jwt_required, create_access_token

from datetime import datetime
from celery import Celery

celery_app = Celery(__name__, broker='redis://localhost:6379/0')

@celery_app.task(name="registrar_log")
def registrar_log(*args):
    pass

cancion_schema = CancionSchema()
usuario_schema = UsuarioSchema()
album_schema = AlbumSchema()

class VistaLogIn(Resource):
    #Iniciar sesión
    def post(self):
            u_nombre = request.json["nombre"]
            u_contrasena = request.json["contrasena"]
            usuario = Usuario.query.filter_by(nombre=u_nombre, contrasena = u_contrasena).all()
            if usuario:
                args = (u_nombre, datetime.utcnow())
                #registrar_log.delay(u_nombre, datetime.utcnow())
                registrar_log.apply_async(args=args,queue='logs')
                return {'mensaje':'Inicio de sesión exitoso'}, 200
            else:
                return {'mensaje':'Nombre de usuario o contraseña incorrectos'}, 401


class VistaSignIn2(Resource):
    #Crear un usuario
    def post(self):
        nuevo_usuario = Usuario(nombre=request.json["nombre"], contrasena=request.json["contrasena"])
        token_de_acceso = create_access_token(identity=request.json["nombre"])
        db.session.add(nuevo_usuario)
        db.session.commit()
        #return 'Usuario creado exitosamente', 201
        return {'mensaje':'Usuario creado exitosamente', 'token_de_acceso':token_de_acceso}, 201

class VistaSignIn1(Resource):

    #Get Usuario
    @jwt_required()
    def get(self, id_usuario):
        print(id_usuario)
        usuario = Usuario.query.get_or_404(id_usuario)
        return usuario_schema.dump(usuario)

    #Actualizar Usuario
    def put(self, id_usuario):
        usuario = Usuario.query.get_or_404(id_usuario)
        usuario.contrasena = request.json.get("contrasena",usuario.contrasena)
        db.session.commit()
        return usuario_schema.dump(usuario)

    #Eliminar Usuario
    def delete(self, id_usuario):
        usuario = Usuario.query.get_or_404(id_usuario)
        db.session.delete(usuario)
        db.session.commit()
        return {'mensaje':'Usuario borrado exitosamente'}, 204          

class VistaCanciones(Resource):
    #Obtener Canciones
    def get(self):
        return [cancion_schema.dump(cancion) for cancion in Cancion.query.all()]

    #Crear Cancion
    def post(self):
        nueva_cancion = Cancion(titulo=request.json['titulo'],\
                                minutos=request.json['minutos'],\
                                segundos=request.json['segundos'],\
                                interprete=request.json['interprete'])
        db.session.add(nueva_cancion)
        db.session.commit()
        return cancion_schema.dump(nueva_cancion)

class VistaCancion(Resource):
    #Obtener Cancion por id
    def get(self, id_cancion):
        return cancion_schema.dump(Cancion.query.get_or_404(id_cancion))

    #Actualizar Cancion por id
    def put(self, id_cancion):
        cancion = Cancion.query.get_or_404(id_cancion)
        cancion.titulo = request.json.get('titulo',cancion.titulo)
        cancion.minutos = request.json.get('minutos',cancion.minutos)
        cancion.segundos = request.json.get('segundos',cancion.segundos)
        cancion.interprete = request.json.get('interprete',cancion.interprete)
        db.session.commit()
        return cancion_schema.dump(cancion)

    #Eliminar Cancion por id
    def delete(self, id_cancion):
        cancion = Cancion.query.get_or_404(id_cancion)
        db.session.delete(cancion)
        db.session.commit()
        return {'mensaje':'Cancion borrada exitosamente'}, 204        

class VistaAlbumsUsuario(Resource):

    #Obtener Albums de un usuario
    @jwt_required()
    def post(self, id_usuario):
        nuevo_album = Album(titulo=request.json["titulo"], anio=request.json["anio"], descripcion=request.json["descripcion"], medio=request.json["medio"])
        usuario = Usuario.query.get_or_404(id_usuario)
        usuario.albumes.append(nuevo_album)

        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return 'El usuario ya tiene un album con dicho nombre',409

        return album_schema.dump(nuevo_album)
    
    #Crear Album de un usuario
    @jwt_required()
    def get(self, id_usuario):
        usuario = Usuario.query.get_or_404(id_usuario)
        return [album_schema.dump(al) for al in usuario.albumes]

class VistaCancionesAlbum(Resource):

    #Crear Cancion de un album
    @jwt_required()
    def post(self, id_album):
        album = Album.query.get_or_404(id_album)
        
        if "id_cancion" in request.json.keys():
            
            nueva_cancion = Cancion.query.get(request.json["id_cancion"])
            if nueva_cancion is not None:
                album.canciones.append(nueva_cancion)
                db.session.commit()
            else:
                return 'Canción errónea',404
        else: 
            nueva_cancion = Cancion(titulo=request.json["titulo"], minutos=request.json["minutos"], segundos=request.json["segundos"], interprete=request.json["interprete"])
            album.canciones.append(nueva_cancion)
        db.session.commit()
        return cancion_schema.dump(nueva_cancion)

    #Obtener Canciones de un album
    @jwt_required()        
    def get(self, id_album):
        album = Album.query.get_or_404(id_album)
        return [cancion_schema.dump(ca) for ca in album.canciones]

class VistaAlbum(Resource):

    #Obtener Album por id
    def get(self, id_album):
        return album_schema.dump(Album.query.get_or_404(id_album))

    #Actualizar Album por id
    def put(self, id_album):
        album = Album.query.get_or_404(id_album)
        album.titulo = request.json.get("titulo",album.titulo)
        album.anio = request.json.get("anio", album.anio)
        album.descripcion = request.json.get("descripcion", album.descripcion)
        album.medio = request.json.get("medio", album.medio)
        db.session.commit()
        return album_schema.dump(album)

    #Eliminar Album por id
    def delete(self, id_album):
        album = Album.query.get_or_404(id_album)
        db.session.delete(album)
        db.session.commit()
        return '',204
