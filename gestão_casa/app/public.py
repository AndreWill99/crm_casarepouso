from flask import Blueprint, render_template, request
from datetime import datetime
from . import db

public_bp = Blueprint('public', __name__)

def calcular_orcamento(grau):
    """Calcula o valor mensal com base na patologia."""
    base = 3000.00
    adicionais = {1: 0, 2: 800.00, 3: 1500.00}
    return base + adicionais.get(grau, 0)

@public_bp.route('/')
def index():
    """Página principal para o público."""
    return render_template('public/index.html')

@public_bp.route('/solicitar-orcamento', methods=['POST'])
def solicitar_orcamento():
    """Recebe o lead do site e salva no banco."""
    dados_lead = {
        "nome_responsavel": request.form.get('nome_responsavel'),
        "nome_idoso": request.form.get('nome_idoso'),
        "telefone": request.form.get('telefone'),
        "grau_patologia": int(request.form.get('grau', 1)),
        "data_criacao": datetime.now(),
        "status": "Novo"
    }
    
    # Adiciona a estimativa
    dados_lead['valor_estimado'] = calcular_orcamento(dados_lead['grau_patologia'])
    
    # Salva usando objeto db importado do app principal
    db.leads.insert_one(dados_lead)
    
    return render_template('public/sucesso.html', valor=dados_lead['valor_estimado'])
