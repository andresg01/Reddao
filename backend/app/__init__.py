from flask import Flask
from uuid import uuid4
from .blockchain import Blockchain
from .models import db
from flask_cors import CORS

# Instanciar la Blockchain y otros elementos globales
blockchain = Blockchain()
node_identifier = str(uuid4()).replace('-', '')

def create_app():
    """Crea y configura una instancia de la aplicación Flask."""
    app = Flask(__name__)
    
    # Habilitar CORS para permitir que el frontend se comunique con el backend
    CORS(app)

    with app.app_context():
        # Importar las rutas para que se registren en la aplicación
        from . import routes

    return app
