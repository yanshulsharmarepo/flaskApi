from flask import Flask, redirect, url_for, request
from DbHelper import getUsers, createUsers, getUser, alterUser, deleteUser

app = Flask(__name__)


@app.route('/')
def hello_world():
    return "Hello World"


@app.route('/api/users', methods=['POST', 'GET'])
def CheckUsers():
    if request.method == 'GET':
        return getUsers(request)
    elif request.method == 'POST':
        return createUsers(request)
    else:
        return 'ELSE'


@app.route('/api/users/<id>', methods=['PUT', 'GET', 'DELETE'])
def users(id):
    if request.method == 'GET':
        return getUser(id)
    elif request.method == 'PUT':
        return alterUser(id, request)
    elif request.method == 'DELETE':
        return deleteUser(id)


if __name__ == '__main__':
    app.run(port='8087')
