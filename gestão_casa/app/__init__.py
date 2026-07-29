import os
# pyrefly: ignore [missing-import]
from flask import Flask
# pyrefly: ignore [missing-import]
from pymongo import MongoClient
from pymongo.server_api import ServerApi
# pyrefly: ignore [missing-import]
from flask_mail import Mail

# Configuração do MongoDB (Tenta ler de MONGO_URI, se não existir usa a string do Atlas)
MONGO_URI = os.getenv(
    "MONGO_URI", 
    "mongodb://localhost:27017/"
)
# Cria o cliente usando a API Server recomendada pela Atlas
client = MongoClient(MONGO_URI, server_api=ServerApi('1'))
db = client['gestao_casa_repouso']
# Envia um ping para confirmar se a conexão com o banco remoto foi estabelecida com sucesso
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(f"Erro de conexão com o MongoDB: {e}")

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
