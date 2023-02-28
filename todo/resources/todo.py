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

def todo_checks(todo):
    if todo is None:
        abort(404, 'The ToDo you are looking for does not exist')
    elif g.user['id'] != todo['user_id']:
        abort(403, 'You do not have access to this ToDo')

@bp.route('/<int:id>/update', methods=['POST','GET'])
@login_required
def update(id):
    todo = Todo.find_by_id(id)
    todo_checks(todo)
    
    if request.method == 'POST':
        print(request.form)
        if request.form.get('update'):
            todo_desc = request.form['description']
            if not todo_desc:
                flash("ToDo description can't be empty")
            else:
                todo_comp = True if request.form.get('completed') else False
                Todo.update(id, todo_desc, todo_comp)
                return redirect(url_for('todo.index'))
        else:
            return redirect(url_for('todo.index'))
    return render_template('todo/update.html', todo=todo)

@bp.route('/<int:id>/delete', methods=['POST'])
@login_required
def delete(id):
    todo = Todo.find_by_id(id)
    todo_checks(todo)
    Todo.delete(id)
    return redirect(url_for('todo.index'))