from sqlalchemy import create_engine
from sqlalchemy import Table
from sqlalchemy.sql import select
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash

db = SQLAlchemy()
connect='mysql+pymysql://sharon:TAhug0r3ng!@localhost:3333/operasional'
engine = create_engine(connect,pool_size=20, max_overflow=0)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))
    role = db.Column(db.String(50))

def create_users_table():
    User.metadata.create_all(engine)

create_users_table()
userTable = Table('user', User.metadata)

def add_user(username, password, email, admin):
    hashed_password = generate_password_hash(password, method='sha256')

    insert_stmt = userTable.insert().values(
        username=username, email=email, password=hashed_password, role=admin
    )
    conn = engine.connect()
    conn.execute(insert_stmt)

def update_password(username, password):
    hashed_password = generate_password_hash(password, method='sha256')
    update = userTable.update().\
        values(password=hashed_password).\
        where(userTable.c.username==username)
    conn = engine.connect()
    conn.execute(update)
    db.session.remove()
    conn.close()
    engine.dispose()

def update_role(username, role):
    update = userTable.update().\
        values(role=role).\
        where(userTable.c.username==username)

    conn = engine.connect()
    conn.execute(update)
    db.session.remove()
    conn.close()
    engine.dispose()

def delete_user(username):
    update = userTable.delete.where(userTable.c.username==username)

    conn = engine.connect()
    conn.execute(update)
    db.session.remove()
    conn.close()
    engine.dispose()

def show_role():
    select_stmt = select([userTable.c.username,userTable.c.role])
    conn=engine.connect()
    results = conn.execute(select_stmt)
    users=[]
    for result in results:
        users.append({
            'username':result[0],
            'role': result[1],
        })
    return users

def show_users():
    select_stmt = select([userTable.c.id,
                        userTable.c.username,
                        userTable.c.email,
                        userTable.c.role])

    conn = engine.connect()
    results = conn.execute(select_stmt)
    users = []

    for result in results:
        users.append({
            'username' : result[1],
            'email' : result[2],
            'role' : result[3]
        })
    return users