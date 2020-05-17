from flask import Flask
from flask_restful import Api

# from security import authenticate, identity
from route import Route

app = Flask(__name__)
app.secret_key = 'embarc'
api = Api(app)

# jwt = JWT(app, authenticate, identity)

api.add_resource(Route, '/route')

if __name__ == '__main__':
    app.run(debug=True)  # important to mention debug=True
