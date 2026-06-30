import os
from flask import Flask
from pymongo import MongoClient
from flask_mail import Mail

# Configuração do MongoDB
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
client = MongoClient(MONGO_URI)
db = client['gestao_casa_repouso']

# Instância global do Mail
mail = Mail()

def create_app():
    # Inicializa o Flask apontando os folders para o diretório pai (raiz do projeto)
    app = Flask(__name__, template_folder='../templates', static_folder='../static')
    
    # Chave de segurança para as sessões do auth.py
    app.secret_key = "super_secret_key_mock"

    # Configurações do Flask-Mail (usando variáveis de ambiente ou valores de teste)
    app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
    app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT', 587))
    app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS', 'True') == 'True'
    app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME', 'teste@gmail.com')
    app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD', 'senha_teste')
    app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER', 'teste@gmail.com')
    
    mail.init_app(app)

    # Registrar os Blueprints (módulos)
    from .public import public_bp
    from .admin import admin_bp
    from .auth import auth_bp
    
    app.register_blueprint(public_bp)
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(auth_bp, url_prefix='/auth')

    return app
