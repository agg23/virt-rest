import signal
import sys

from flask import Flask, jsonify
from flask_restful import Api
from werkzeug.exceptions import HTTPException

from virtrest.connection import getConnection
from virtrest.endpoints.domain import Domains, Domain, DomainState
from virtrest.endpoints.usb import USB, USBState

app = Flask(__name__)
api = Api(app)

api.add_resource(Domains, '/domains/')
api.add_resource(Domain, '/domain/<name>')
api.add_resource(DomainState, '/domain/<name>/status')
api.add_resource(USB, '/usb/')
api.add_resource(USBState, '/usb/state/<domainName>')

def signal_handler(sig, frame):
    print("SIGINT recieved")
    connection = getConnection()
    connection.close()
    sys.exit(0)

if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)

    app.run(host= '0.0.0.0', debug=True)
