from flask import Flask, jsonify, request
from functools import wraps
import jwt
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'MyJWTDemo'

def check_if_authorized(func):
    ''' decorator to check if token is provided '''
    @wraps(func)
    def executor(*args, **kwargs):
        print(request.args)
        token = request.args.get('token')
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
                'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=60)
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