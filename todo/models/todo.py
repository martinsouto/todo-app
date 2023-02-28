from todo.db import get_db

class Todo(object):
    @classmethod
    def list_todos_for_user(cls, user_id):
        db, c = get_db()
        c.execute("select * from todo where user_id = %s", (user_id,))
        return c.fetchall()
    
    @classmethod
    def create(cls, user_id, description):
        db, c = get_db()
        c.execute("insert into todo (user_id, description, completed) values (%s, %s, %s)", (user_id, description, False))
        db.commit()
        
    @classmethod
    def find_by_id(cls, id):
        db, c = get_db()
        c.execute("select * from todo where id = %s", (id, ))
        return c.fetchone()
    
    @classmethod
    def update(cls, id, description, completed):
        db, c = get_db()
        c.execute("update todo set description = %s, completed = %s where id = %s", (description, completed, id))
        db.commit()

    @classmethod
    def delete(cls, id):
        db, c = get_db()
        c.execute("delete from todo where id = %s", (id, ))
        db.commit()