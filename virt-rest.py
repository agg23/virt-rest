import sys

from flask import Flask
from flask_restful import Api

from virtrest.endpoints.domain import Domain

app = Flask(__name__)
api = Api(app)

api.add_resource(Domain, '/')

if __name__ == '__main__':
    app.run(host= '0.0.0.0', debug=True)