from flask import Flask
from pymongo import MongoClient

# Instância global do BD local
client = MongoClient("mongodb://localhost:27017/")
db = client['gestao_casa_repouso']

def create_app():
    # Inicializa o Flask apontando os folders para o diretório pai (raiz do projeto)
    app = Flask(__name__, template_folder='../templates', static_folder='../static')
    
    # Chave de segurança para as sessões do auth.py
    app.secret_key = "super_secret_key_mock"

    # Registrar os Blueprints (módulos)
    from .public import public_bp
    from .admin import admin_bp
    from .auth import auth_bp
    
    app.register_blueprint(public_bp)
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(auth_bp, url_prefix='/auth')

    return app
