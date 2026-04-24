from flask import Blueprint, session, redirect, url_for, request, render_template
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from . import db

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
            session['user'] = user['username']
            session['role'] = user.get('role', 'staff')
            return redirect(request.args.get('next') or url_for('admin.dashboard'))
        else:
            error = "Usuário ou senha inválidos."
            
    return render_template('admin/login.html', error=error)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        name = request.form.get('name')
        username = request.form.get('username')
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
                "role": role,
                "password_hash": generate_password_hash(password)
            })
            session['user'] = username
            session['role'] = role
            return redirect(url_for('admin.dashboard'))
            
    return render_template('admin/register.html', error=error)

@auth_bp.route('/logout')
def logout():
    session.pop('user', None)
    session.pop('role', None)
    return redirect(url_for('public.index'))
