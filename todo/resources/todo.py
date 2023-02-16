import functools
from flask import Blueprint, flash, g, render_template, url_for, request, session, redirect
from werkzeug.exceptions import abort
from todo.models.todo import Todo
from todo.resources.auth import login_required

bp = Blueprint('todo', __name__)

@bp.route('/', methods=['POST','GET'])
@login_required
def index():
    todos = sorted(sorted(Todo.list_todos_for_user(g.user['id']), key= lambda x: x['created_at'], reverse=True), key= lambda x: x['completed'])
    return render_template('todo/index.html', todos=todos)

@bp.route('/create', methods=['POST','GET'])
@login_required
def create():
    return ''

@bp.route('/update', methods=['POST','GET'])
@login_required
def update():
    return ''