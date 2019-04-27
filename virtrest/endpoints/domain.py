from flask import jsonify, request
from flask_restful import Resource, abort

from virtrest.connection import getConnection
from virtrest.util import isInt

class Domains(Resource):
    def get(self):
        connection = getConnection()

        allDomains = [parseCommonDomain(domain) for domain in connection.listAllDomains()]

        return jsonify(allDomains)

class Domain(Resource):
    def get(self, name=None):
        domain = getDomainWithErrors(name)
        domainDict = parseCommonDomain(domain)

        return jsonify(domainDict)

class DomainState(Resource):
    def post(self, name=None):
        domain = getDomainWithErrors(name)

        jsonData = request.get_json()

        if jsonData is None:
            abort(400, message="No payload provided")

        if "action" not in jsonData:
            abort(400, message="No action provided")

        action = jsonData["action"]

        if action == "create":
            domain.create()
        elif action == "reboot":
            domain.reboot()
        elif action == "reset":
            domain.reset()
        elif action == "resume":
            domain.resume()
        elif action == "suspend":
            domain.suspend()
        elif action == "shutdown":
            domain.shutdown()
        else:
            abort(400, message="Invalid action provided")

def getDomainWithErrors(name):
    if name is None:
        abort(400, message="No domain provided")

    domain = lookupDomain(name)
    if domain is None:
        abort(404, message="Domain \"{0}\" could not be found".format(name))

    return domain

def lookupDomain(name):
    connection = getConnection()

    try:
        if isInt(name):
            domain = connection.lookupByID(int(name))
        else:
            domain = connection.lookupByName(name)
    except:
        return None

    return domain

def parseCommonDomain(domain):
    domainDict = {}
    domainId = domain.ID()
    if domainId == -1:
        # Inactive domain
        domainDict["id"] = None
    else:
        domainDict["id"] = domainId
    domainDict["name"] = domain.name()
    domainDict["osType"] = domain.OSType()
    info = parseInfo(domain.info())
    if info is not None:
        domainDict["info"] = info

    domainDict["running"] = domain.isActive() == 1

    return domainDict

def parseInfo(infoObject):
    infoDict = {}

    if len(infoObject) != 5:
        return infoDict

    infoDict["state"] = infoObject[0]
    infoDict["maxMemory"] = infoObject[1]
    infoDict["currentMemory"] = infoObject[2]
    infoDict["vcpus"] = infoObject[3]
    infoDict["cpuTime"] = infoObject[4]

    return infoDict