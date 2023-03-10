import functools
from flask import Blueprint, flash, g, render_template, url_for, request, session, redirect
from werkzeug.security import check_password_hash, generate_password_hash
from todo.models.user import User

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=['POST','GET'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None
        if not username:
            error = 'Username is required'
        elif not password:
            error = 'Password is required'
        elif User.find_by_username(username) is not None:
            error = "User {} already exists, try a different username".format(username)
        else:
            User.create(username,generate_password_hash(password))
            return redirect(url_for('auth.login')) 
        flash(error)
    
    return render_template('auth/register.html')

@bp.route('/login', methods=['POST','GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None
        if not username:
            error = 'Username is required'
        elif not password:
            error = 'Password is required'
        else:
            user = User.find_by_username(username)
            if (user is None) or (not check_password_hash(pwhash=user['password'], password=password)):
                error = "Incorrect username and/or password"
            else:
                session.clear()
                session['user_id'] = user['id']
                return redirect(url_for('todo.index'))

        flash(error)

    return render_template('auth/login.html')

@bp.route('/logout', methods=['POST','GET'])
def logout():
    session.clear()
    return redirect(url_for('todo.index'))

@bp.before_app_request
def load_logged_in_user():
    if session.get('user_id') is None:
        g.user = None
    else:
        g.user = User.find_by_id(session.get('user_id'))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    
    return wrapped_view