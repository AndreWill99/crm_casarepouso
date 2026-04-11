from flask import Blueprint, render_template, send_file
import pandas as pd
import io
from . import db
from .auth import login_required

admin_bp = Blueprint('admin', __name__)

# Associa o mock_login de forma que todo este arquivo admin.py seja bloqueado se não logado
@admin_bp.before_request
@login_required
def require_login():
    pass

@admin_bp.route('/')
def dashboard():
    """Painel principal com resumo."""
    contagem = {
        "leads": db.leads.count_documents({"status": "Novo"}),
        "residentes": db.residentes.count_documents({}),
        "funcionarios": db.funcionarios.count_documents({})
    }
    return render_template('admin/dashboard.html', resumo=contagem)

@admin_bp.route('/leads')
def leads():
    todos_leads = list(db.leads.find().sort("data_criacao", -1))
    return render_template('admin/leads.html', leads=todos_leads)

@admin_bp.route('/residentes')
def residentes():
    lista_residentes = list(db.residentes.find())
    return render_template('admin/residentes.html', residentes=lista_residentes)

@admin_bp.route('/funcionarios')
def funcionarios():
    todos_funcionarios = list(db.funcionarios.find())
    return render_template('admin/funcionarios.html', funcionarios=todos_funcionarios)

@admin_bp.route('/financeiro')
def financeiro():
    transacoes = list(db.financeiro.find().sort("data", -1))
    return render_template('admin/financeiro.html', transacoes=transacoes)

@admin_bp.route('/exportar-excel')
def exportar_excel():
    """Gera e faz o download direto do Excel pela memória Buffer."""
    dados = list(db.residentes.find({}, {'_id': 0}))
    if not dados:
        return "Nenhum dado para exportar", 404
        
    df = pd.DataFrame(dados)
    output = io.BytesIO()
    
    # Pandas + OpenPyxl para Buffer
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Residentes')
        
    output.seek(0)
    return send_file(output, download_name="relatorio_residentes.xlsx", as_attachment=True)
