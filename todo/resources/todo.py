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
    if request.method == 'POST':
        if request.form.get('create'):
            todo_desc = request.form['description']
            if not todo_desc:
                flash("ToDo description can't be empty")
            else:
                Todo.create(g.user['id'], todo_desc)
                return redirect(url_for('todo.index'))
        else:
            return redirect(url_for('todo.index'))

    return render_template('todo/create.html')

@bp.route('/update', methods=['POST','GET']) #/<int:id>/update
@login_required
def update():
    return render_template('todo/update.html')