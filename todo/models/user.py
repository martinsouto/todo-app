from todo.db import get_db

class User(object):
    @classmethod
    def find_by_username(cls, username):
        db, c = get_db()
        c.execute("select * from user where username = %s", (username,))
        return c.fetchone()
    
    @classmethod
    def create(cls, username, password):
        db, c = get_db()
        c.execute("insert into user (username, password) values (%s, %s)", (username, password))
        db.commit()
