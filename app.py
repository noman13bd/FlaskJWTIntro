from flask import Flask, jsonify, request
import jwt
import datetime
from functools import wraps
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask_sqlalchemy import SQLAlchemy
import uuid


app = Flask(__name__)
app.config['SECRET_KEY'] = 'MyJWTDemo'
#postgresql://USER:PASS@HOST:PORT/DB
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:postgres@localhost:5432/postgres"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80))
    name = db.Column(db.String(80))
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __init__(self, username, password, name, email):
        self.username = username
        self.password = generate_password_hash(password)
        self.name = name
        self.email = email
    
    def __repr__(self):
        return "<User {}>".format(self.username)

    def verify_password(self, pwd):
        return check_password_hash(self.password, pwd)

def check_if_authorized(func):
    ''' decorator to check if token is provided '''
    @wraps(func)
    def executor(*args, **kwargs):
        token = None
        if request.headers.has_key('Access-token'):
            token = request.headers['Access-Token']
        if not token:
            return jsonify({'message':'Missing Token'}), 403
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
        except:
            return jsonify({'message':'Invalid Token'}), 403
        return func(*args, **kwargs)
    return executor

@app.route('/')
def index():
    return 'Ok'

@app.route('/login', methods=['POST'])
def login():
    if request.is_json:
        data = request.get_json()
        print(data)
        if data['un'] and data['pwd'] == '123456':
            token = jwt.encode({
                'user': data['un'],
                'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60)
            }, app.config['SECRET_KEY'])
            return jsonify({'token': token.decode('utf-8')})
        else:
            return jsonify({'message':'error'})

@app.route('/public')
def public():
    return jsonify({'message':'Public'}), 200

@app.route('/auth')
@check_if_authorized
def authrized():
    return jsonify({'message':'Auth'}), 200

if __name__ == '__main__':
    app.run(debug=True)