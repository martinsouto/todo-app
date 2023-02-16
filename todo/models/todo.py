from todo.db import get_db

class Todo(object):
    @classmethod
    def list_todos_for_user(cls, user_id):
        db, c = get_db()
        c.execute("select * from todo where user_id = %s", (user_id,))
        return c.fetchall()