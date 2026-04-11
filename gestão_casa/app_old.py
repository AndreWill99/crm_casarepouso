from flask import Flask, render_template, request, redirect, url_for, jsonify
from pymongo import MongoClient
import pandas as pd
from datetime import datetime

app = Flask(__name__)

# --- CONFIGURAÇÃO DO BANCO DE DADOS ---
# Conecta ao MongoDB local (certifica-te que o MongoDB está a correr)
client = MongoClient("mongodb://localhost:27017/")
db = client['gestao_casa_repouso']

# --- LÓGICA DE NEGÓCIO ---
def calcular_orcamento(grau):
    """Calcula o valor mensal com base na patologia."""
    base = 3000.00
    adicionais = {1: 0, 2: 800.00, 3: 1500.00}
    return base + adicionais.get(grau, 0)

# --- ROTAS PÚBLICAS (CLIENTE) ---

@app.route('/')
def index():
    """Página principal para o público."""
    return render_template('public/index.html')

@app.route('/solicitar-orcamento', methods=['POST'])
def solicitar_orcamento():
    """Recebe o lead do site e salva no banco."""
    dados_lead = {
        "nome_responsavel": request.form.get('nome_responsavel'),
        "nome_idoso": request.form.get('nome_idoso'),
        "telefone": request.form.get('telefone'),
        "grau_patologia": int(request.form.get('grau')),
        "data_criacao": datetime.now(),
        "status": "Novo"
    }
    # Calcula o preço e adiciona ao dicionário
    dados_lead['valor_estimado'] = calcular_orcamento(dados_lead['grau_patologia'])
    
    # Salva na coleção de leads
    db.leads.insert_one(dados_lead)
    
    return render_template('public/sucesso.html', valor=dados_lead['valor_estimado'])

# --- ROTAS ADMINISTRATIVAS (GESTÃO) ---

@app.route('/admin')
def admin_dashboard():
    """Painel principal com resumo."""
    contagem = {
        "leads": db.leads.count_documents({"status": "Novo"}),
        "residentes": db.residentes.count_documents({}),
        "funcionarios": db.funcionarios.count_documents({})
    }
    return render_template('admin/dashboard.html', resumo=contagem)

@app.route('/admin/leads')
def admin_leads():
    """Lista todos os leads interessados."""
    todos_leads = list(db.leads.find().sort("data_criacao", -1))
    return render_template('admin/leads.html', leads=todos_leads)

@app.route('/admin/residentes')
def admin_residentes():
    """Lista os idosos que já moram na casa."""
    residentes = list(db.residentes.find())
    return render_template('admin/residentes.html', residentes=residentes)

@app.route('/admin/funcionarios')
def admin_funcionarios():
    """Lista a equipe de funcionários."""
    todos_funcionarios = list(db.funcionarios.find())
    return render_template('admin/funcionarios.html', funcionarios=todos_funcionarios)

@app.route('/admin/financeiro')
def admin_financeiro():
    """Mostra o fluxo de caixa."""
    transacoes = list(db.financeiro.find().sort("data", -1))
    return render_template('admin/financeiro.html', transacoes=transacoes)

@app.route('/admin/exportar-excel')
def exportar_excel():
    """Gera o arquivo Excel para o gestor."""
    # Busca dados de residentes para o exemplo
    dados = list(db.residentes.find({}, {'_id': 0}))
    if not dados:
        return "Nenhum dado para exportar", 404
        
    df = pd.DataFrame(dados)
    filename = "relatorio_residentes.xlsx"
    df.to_excel(filename, index=False)
    
    return f"Relatório {filename} gerado no servidor!"

if __name__ == '__main__':
    # Rodar em modo debug facilita o desenvolvimento
    app.run(debug=True)