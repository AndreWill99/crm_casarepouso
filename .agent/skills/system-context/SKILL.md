---
name: system-context
description: Use sempre para manter o contexto do desenvolvimento do sistema.O sistema tem como objetivo profissionalizar o atendimento e a gestão de uma casa de repouso de pequeno porte. Atualmente, a empresa opera via WhatsApp e planilhas manuais. A solução automatiza a captação de clientes (Leads) e centraliza a gestão administrativa. 
---


1. Visão Geral do Projeto
O sistema tem como objetivo profissionalizar o atendimento e a gestão de uma casa de repouso de pequeno porte. Atualmente, a empresa opera via WhatsApp e planilhas manuais. A solução automatiza a captação de clientes (Leads) e centraliza a gestão administrativa.

2. Stack Tecnológica
Linguagem: Python 3.x

Framework Web: Flask (Abordagem Monolítica com Jinja2 templates)

Banco de Dados: MongoDB (NoSQL)

Bibliotecas Chave:

pymongo: Conexão com banco de dados.

pandas e openpyxl: Geração de relatórios Excel.

datetime: Gestão de datas e fluxos financeiros.

3. Arquitetura e Site Map
O sistema é dividido em duas frentes principais:

A. Área Pública (Landing Page)
Objetivo: Conversão de visitantes em Leads.

Seções: Home, Sobre, Serviços (Graus de dependência), Simulador de Orçamento.

Fluxo: Preenchimento do formulário -> Cálculo Automático -> Cadastro na coleção leads.

B. Área Administrativa (Painel de Gestão)
Dashboard: Visão geral (KPIs de residentes, leads e financeiro).

Gestão de Leads: Triagem e conversão de interessados em residentes.

Gestão de Residentes: Cadastro completo e prontuário básico.

Gestão de Funcionários: Cadastro de staff e controle salarial.

Financeiro: Fluxo de caixa (Entradas de mensalidades e saídas de funcionários/custos fixos).

4. Regras de Negócio (Core Logic)
Cálculo de Orçamento Mensal:

Grau 1 (Base): R$ 3.000,00

Grau 2: Base + R$ 800,00

Grau 3: Base + R$ 1.500,00

Conversão: Um Lead torna-se um Residente mantendo o histórico de contato inicial.

Fluxo de Caixa: Toda saída (salário) deve ser vinculada a um id_funcionario ou categoria de despesa.

5. Estrutura de Dados (MongoDB Collections)
leads: {nome_responsavel, nome_idoso, telefone, grau, valor_estimado, status, data}

residentes: {nome, data_admissao, grau, status_saude, responsavel_contato, id_lead_origem}

funcionarios: {nome, cargo, salario_base, data_admissao, status}

financeiro: {tipo: "Receita/Despesa", valor, categoria, data, referencia_id}

6. Estrutura de Pastas
Instruções para a IA:
Ao gerar código para este projeto, mantenha a simplicidade. Priorize o uso de Python para manipulação de dados e evite complexidades desnecessárias de JavaScript. Toda exportação de dados deve seguir o formato .xlsx usando Pandas.

## 7. Segurança e Modularidade (Blueprints)
- **Estrutura:** O projeto utiliza Flask Blueprints para separar a área pública da administrativa.
- **Isolamento:** - `public_bp`: Gerencia rotas acessíveis ao mundo (Landing Page, Orçamentos).
    - `admin_bp`: Gerencia rotas sensíveis (CRM, Financeiro, Residentes).
- **Segurança Futura:** Esta separação permite aplicar decoradores de `@login_required` apenas no bloco `admin_bp`, sem afetar a performance ou o acesso ao site público.
- **Manutenção:** Erros de lógica no código administrativo não derrubam a renderização da página pública e vice-versa.

## 8. Módulo de Calendário e Agenda
- **Objetivo:** Organizar o fluxo de pessoas externas e eventos internos.
- **Categorias de Eventos:** - **Visitas Familiares:** Vinculadas a um Residente específico.
    - **Ações Sociais:** Visitas de Igrejas, ONGs ou grupos filantrópicos.
    - **Datas Comemorativas:** Aniversários de residentes/staff e feriados.
- **Dados (Coleção `agenda`):** `{titulo, tipo, data, hora, descricao, id_residente (opcional)}`

## 9. Padrões de Interface (UI Patterns)
- **Master-Detail:** Utilização de Side Panels (Drawers) para visualização e edição rápida de Residentes e Leads, mantendo o contexto da lista principal.
- **Micro-interações:** Uso de cores semânticas (Verde/Laranja/Vermelho) para representar estados críticos de saúde ou financeiro.

## 10. Entidade: Funcionários (Staff)
- **Campos:** {nome, cargo, turno, salario_base, status, data_admissao}.
- **Regra de Negócio:** O campo `salario_base` deve alimentar automaticamente as sugestões de lançamentos de saída no módulo Financeiro.

## 11. Inteligência Financeira
- **Cruzamento de Dados:** O sistema deve permitir filtrar despesas por funcionário e receitas por residente.
- **Exportação:** O botão "Exportar" na tela financeira deve gerar o Excel consolidado com o saldo final calculado via Python (Pandas).