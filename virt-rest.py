import sys

from flask import Flask
from flask_restful import Api

from virtrest.endpoints.domain import Domains, Domain
from virtrest.endpoints.usb import USB

app = Flask(__name__)
api = Api(app)

api.add_resource(Domains, '/domains/')
api.add_resource(Domain, '/domain/<name>')
api.add_resource(USB, '/usb/')

if __name__ == '__main__':
    app.run(host= '0.0.0.0', debug=True)