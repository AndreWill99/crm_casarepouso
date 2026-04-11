from flask import Blueprint, session, redirect, url_for, request
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
    
    # Renderiza um login inline básico para mock
    return '''
        <div style="font-family: sans-serif; display: flex; justify-content: center; align-items: center; height: 100vh; background: #FFEED5;">
            <form method="post" style="background: white; padding: 40px; border-radius: 8px; box-shadow: 0 4px 10px rgba(0,0,0,0.1); width: 300px; text-align: center;">
                <h2 style="color: #7A1515; margin-bottom: 20px;">Login Gestão</h2>
                <input type="text" name="username" placeholder="Login" style="width: 100%; padding: 10px; margin-bottom: 15px; border: 1px solid #ddd; border-radius: 4px;" required>
                <input type="password" name="password" placeholder="Senha" style="width: 100%; padding: 10px; margin-bottom: 15px; border: 1px solid #ddd; border-radius: 4px;" required>
                <button type="submit" style="width: 100%; padding: 10px; background: #7A1515; color: white; border: none; border-radius: 4px; font-weight: bold; cursor: pointer;">Entrar</button>
            </form>
        </div>
    '''

@auth_bp.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('public.index'))
