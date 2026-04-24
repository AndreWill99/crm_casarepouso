from flask import Blueprint, render_template, send_file, request, jsonify
import pandas as pd
import io
from . import db
from .auth import login_required
from bson.objectid import ObjectId

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
    
    funnel = {
        "novo": 0,
        "em_contato": 0,
        "ag_visita": 0,
        "convertido": 0,
        "total_visitas_site": 1248 # Mock para demonstração
    }
    
    for l in todos_leads:
        st = l.get("status", "").lower()
        if "novo" in st: funnel["novo"] += 1
        elif "contato" in st: funnel["em_contato"] += 1
        elif "visita" in st: funnel["ag_visita"] += 1
        elif "convertido" in st or "matriculado" in st: funnel["convertido"] += 1
        
    funnel["total_leads"] = funnel["novo"] + funnel["em_contato"] + funnel["ag_visita"] + funnel["convertido"]
        
    return render_template('admin/leads.html', leads=todos_leads, funnel=funnel)

@admin_bp.route('/residentes')
def residentes():
    lista_residentes = list(db.residentes.find())
    return render_template('admin/residentes.html', residentes=lista_residentes)

@admin_bp.route('/funcionarios')
def funcionarios():
    todos_funcionarios = list(db.funcionarios.find())
    return render_template('admin/funcionarios.html', funcionarios=todos_funcionarios)

@admin_bp.route('/configuracoes')
def configuracoes():
    usuarios = list(db.users.find())
    config = db.config.find_one() or {
        "nome": "Casa de Repouso VivaBem",
        "cnpj": "12.345.678/0001-99",
        "telefone": "(11) 3456-7890",
        "endereco": "Rua das Flores, 245 — Jardim Primavera, São Paulo - SP",
        "email": "contato@vivabem.com.br",
        "site": "www.vivabem.com.br",
        "g1": "R$ 2.800,00",
        "g2": "R$ 4.200,00",
        "g3": "R$ 6.800,00"
    }
    return render_template('admin/configuracoes.html', usuarios=usuarios, config=config)

@admin_bp.route('/api/config', methods=['POST'])
def api_config():
    try:
        dados = request.get_json()
        if not dados:
            return jsonify({"status": "error", "message": "Nenhum dado recebido"}), 400
            
        db.config.replace_one({}, dados, upsert=True)
        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@admin_bp.route('/financeiro')
def financeiro():
    def tratar_moeda(val):
        if not val: return 0.0
        try:
            v = str(val).replace('R$', '').replace('.', '').replace(',', '.').strip()
            return float(v)
        except:
            return 0.0
            
    def formatar_brl(val):
        return f"R$ {val:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')

    transacoes = list(db.financeiro.find().sort("data", -1))
    
    entradas = 0.0
    despesas = 0.0
    
    import datetime
    agora = datetime.datetime.now()
    mes_atual_idx = agora.month - 1
    meses_nomes = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
    saldos_mes = {m: 0.0 for m in meses_nomes}
    
    for t in transacoes:
        v = tratar_moeda(t.get('valor', '0'))
        is_entrada = t.get('tipo', '').lower() == 'entrada'
        
        if is_entrada:
            entradas += v
        else:
            despesas += v
            
        data_str = t.get('data', '')
        if data_str:
            parts = data_str.replace('-', '/').split('/')
            if len(parts) >= 2:
                try:
                    mes_idx = int(parts[1]) - 1
                    if 0 <= mes_idx <= 11:
                        if is_entrada:
                            saldos_mes[meses_nomes[mes_idx]] += v
                        else:
                            saldos_mes[meses_nomes[mes_idx]] -= v
                except:
                    pass
            
    saldo = entradas - despesas
    cards = {
        "entradas": formatar_brl(entradas),
        "despesas": formatar_brl(despesas),
        "saldo": formatar_brl(saldo)
    }
    
    max_saldo = max([abs(val) for val in saldos_mes.values()] + [1.0])
    
    chart_data = []
    for i, m in enumerate(meses_nomes):
        val = saldos_mes[m]
        perc = int((abs(val) / max_saldo) * 100)
        if perc < 5 and val != 0: perc = 5
        if perc == 0 and val == 0: perc = 10
        chart_data.append({
            "mes": m,
            "valor": int(val),
            "perc": perc,
            "is_current": (i == mes_atual_idx),
            "is_zero": (val == 0)
        })
    
    return render_template('admin/financeiro.html', transacoes=transacoes, cards=cards, chart_data=chart_data)

@admin_bp.route('/agenda')
def agenda():
    return render_template('admin/agenda.html')

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

@admin_bp.route('/configuracoes')
def configuracoes():
    return render_template('admin/configuracoes.html')

@admin_bp.route('/api/residentes', methods=['POST'])
def api_residentes():
    try:
        dados = request.get_json()
        
        # Validar dados básicos
        if not dados or not dados.get('nome'):
            return jsonify({"status": "error", "message": "Nome é obrigatório"}), 400
            
        # Inserção do residente novo (simplificada)
        resultado = db.residentes.insert_one({
            "nome": dados.get('nome'),
            "data_nascimento": dados.get('nascimento'),
            "data_entrada": dados.get('entrada'),
            "quarto": dados.get('quarto'),
            "status": dados.get('status'),
            "responsavel": dados.get('responsavel'),
            "telefone_responsavel": dados.get('telefone'),
            "grau_dependencia": dados.get('grau')
        })
        
        return jsonify({"status": "success", "id": str(resultado.inserted_id)})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@admin_bp.route('/api/financeiro', methods=['POST'])
def api_financeiro():
    try:
        dados = request.get_json()
        
        if not dados or not dados.get('categoria') or not dados.get('valor'):
            return jsonify({"status": "error", "message": "Preencha a categoria e valor."}), 400
            
        doc = {
            "tipo": dados.get('tipo'),
            "categoria": dados.get('categoria'),
            "valor": dados.get('valor'),
            "data": dados.get('data'),
            "descricao": dados.get('descricao')
        }
        
        obj_id = dados.get('id')
        if obj_id:
            db.financeiro.update_one({'_id': ObjectId(obj_id)}, {'$set': doc})
            return jsonify({"status": "success", "id": str(obj_id)})
        else:
            resultado = db.financeiro.insert_one(doc)
            return jsonify({"status": "success", "id": str(resultado.inserted_id)})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@admin_bp.route('/api/funcionarios', methods=['POST'])
def api_funcionarios():
    try:
        dados = request.get_json()
        
        if not dados or not dados.get('nome'):
            return jsonify({"status": "error", "message": "Nome é obrigatório"}), 400
            
        resultado = db.funcionarios.insert_one({
            "nome": dados.get('nome'),
            "data_nascimento": dados.get('nascimento'),
            "data_admissao": dados.get('admissao'),
            "cpf": dados.get('cpf'),
            "status": dados.get('status'),
            "email": dados.get('email'),
            "telefone": dados.get('telefone'),
            "turno": dados.get('turno'),
            "salario_base": dados.get('salario_base'),
            "cargo": dados.get('cargo'),
            "escala": dados.get('escala')
        })
        
        return jsonify({"status": "success", "id": str(resultado.inserted_id)})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@admin_bp.route('/api/leads', methods=['POST'])
def api_leads():
    try:
        dados = request.get_json()
        
        if not dados or not dados.get('nome'):
            return jsonify({"status": "error", "message": "O nome do interessado é obrigatório."}), 400
            
        doc = {
            "nome": dados.get('nome'),
            "telefone": dados.get('telefone'),
            "email": dados.get('email'),
            "nome_idoso": dados.get('nome_idoso'),
            "idade_gen": dados.get('idade_gen'),
            "grau": dados.get('grau'),
            "obs": dados.get('obs'),
            "status": dados.get('status')
        }
        
        obj_id = dados.get('id')
        if obj_id:
            db.leads.update_one({'_id': ObjectId(obj_id)}, {'$set': doc})
            return jsonify({"status": "success", "id": str(obj_id)})
        else:
            import datetime
            doc["data_criacao"] = datetime.datetime.now().strftime("%d-%m-%Y")
            resultado = db.leads.insert_one(doc)
            return jsonify({"status": "success", "id": str(resultado.inserted_id)})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@admin_bp.route('/export/<modulo>')
def exportar_modulo(modulo):
    colecoes = {
        'leads': db.leads,
        'residentes': db.residentes,
        'funcionarios': db.funcionarios,
        'financeiro': db.financeiro
    }
    
    if modulo not in colecoes:
        return "Módulo não encontrado", 404
        
    dados = list(colecoes[modulo].find())
    
    if not dados:
        return "Nenhum dado para exportar", 404
        
    for doc in dados:
        doc['_id'] = str(doc['_id'])
        
    df = pd.DataFrame(dados)
    output = io.BytesIO()
    
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name=modulo.capitalize())
        
    output.seek(0)
    return send_file(
        output,
        as_attachment=True,
        download_name=f'export_{modulo}.xlsx',
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
