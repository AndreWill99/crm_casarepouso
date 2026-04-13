from flask import Blueprint, session, redirect, url_for, request, render_template
from functools import wraps

auth_bp = Blueprint('auth', __name__)

# Mock Decorador para proteger rotas da gestão
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Checa se o usuário atual está na sessão
        if 'user' not in session:
            # Caso contrário, força o redirecionamento par a página de login
            return redirect(url_for('auth.login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Mocking: Qualquer formulário preenchido loga como 'Admin'
        session['user'] = request.form.get('username', 'Admin')
        return redirect(request.args.get('next') or url_for('admin.dashboard'))
    
    # Renderiza o template que criamos
    return render_template('admin/login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Mocking: Cadastro concluído com sucesso loga como 'Admin'
        session['user'] = request.form.get('username', 'Admin')
        return redirect(url_for('admin.dashboard'))
    
    # Renderiza o template de cadastro
    return render_template('admin/register.html')

@auth_bp.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('public.index'))
