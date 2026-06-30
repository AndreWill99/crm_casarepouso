from flask import Blueprint, session, redirect, url_for, request, render_template
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from . import db, mail
from flask_mail import Message
import random
import string

auth_bp = Blueprint('auth', __name__)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('auth.login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = db.users.find_one({"username": username})
        
        if user and check_password_hash(user['password_hash'], password):
            # Salva dados temporários na sessão para o processo de 2FA
            session['temp_user'] = user['username']
            session['temp_role'] = user.get('role', 'staff')
            session['temp_email'] = user.get('email', '')
            # Guarda também o next_url se houver
            session['next_url'] = request.args.get('next')
            return redirect(url_for('auth.verify_pin'))
        else:
            error = "Usuário ou senha inválidos."
            
    return render_template('admin/login.html', error=error)

@auth_bp.route('/verify-pin', methods=['GET', 'POST'])
def verify_pin():
    if 'temp_user' not in session:
        return redirect(url_for('auth.login'))
        
    error = None
    # Verifica/Cria PIN padrão se não existir
    settings = db.settings.find_one({"type": "security"})
    if not settings:
        db.settings.insert_one({"type": "security", "master_pin": "1234"})
        master_pin = "1234"
    else:
        master_pin = settings.get("master_pin", "1234")
        
    if request.method == 'POST':
        pin = request.form.get('pin')
        if pin == master_pin:
            # PIN correto, gera OTP e envia por e-mail
            otp = ''.join(random.choices(string.digits, k=6))
            session['otp'] = otp
            
            # Enviar e-mail (usar try-except para evitar quebra se o email falhar localmente)
            try:
                msg = Message("Seu código de verificação",
                              recipients=[session.get('temp_email')])
                msg.body = f"Seu código de verificação é: {otp}"
                mail.send(msg)
            except Exception as e:
                print(f"Erro ao enviar email: {e}")
                # Para desenvolvimento, você pode logar o OTP no console
                print(f"OTP gerado: {otp}")
                
            return redirect(url_for('auth.verify_email'))
        else:
            error = "PIN incorreto."
            
    return render_template('admin/verify_pin.html', error=error)

@auth_bp.route('/verify-email', methods=['GET', 'POST'])
def verify_email():
    if 'temp_user' not in session or 'otp' not in session:
        return redirect(url_for('auth.login'))
        
    error = None
    if request.method == 'POST':
        user_otp = request.form.get('otp')
        if user_otp == session['otp']:
            # Autenticação completa
            session['user'] = session.pop('temp_user')
            session['role'] = session.pop('temp_role')
            session.pop('temp_email', None)
            session.pop('otp', None)
            
            next_url = session.pop('next_url', None)
            return redirect(next_url or url_for('admin.dashboard'))
        else:
            error = "Código de verificação incorreto."
            
    return render_template('admin/verify_email.html', error=error)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        name = request.form.get('name')
        username = request.form.get('username')
        email = request.form.get('email')
        role = request.form.get('role')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        if password != confirm_password:
            error = "As senhas não coincidem."
        elif db.users.find_one({"username": username}):
            error = "Este nome de usuário já está em uso."
        else:
            db.users.insert_one({
                "name": name,
                "username": username,
                "email": email,
                "role": role,
                "password_hash": generate_password_hash(password)
            })
            # Salva na sessão e envia para o Dashboard sem 2FA (ou pode forçar relogar)
            # Para manter segurança, vamos apenas redirecionar para login
            return redirect(url_for('auth.login'))
            
    return render_template('admin/register.html', error=error)

@auth_bp.route('/logout')
def logout():
    session.pop('user', None)
    session.pop('role', None)
    return redirect(url_for('public.index'))
