from flask import Flask

def create_app(config_name):
    app = Flask(__name__)
    #usuario: estudiante
    #contraseña: 12345
    #correrla en el puerto: 5432
    # crear db: tabla 
    # https://ocawthorne.medium.com/using-postgresql-on-a-windows-10-os-through-visual-studio-code-via-windows-subsystem-for-linux-d207a4708497
    #https://www.youtube.com/watch?v=BLH3s5eTL4Y
    #\q para salir
    app.config['SQLALCHEMY_DATABASE_URI']= 'postgresql://postgres:admin@127.0.0.1:5434/test'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    return app