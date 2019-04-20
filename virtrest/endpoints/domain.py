from flask import jsonify
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
        connection = getConnection()

        if name is None:
            abort(400)

        try:
            if isInt(name):
                domain = connection.lookupByID(int(name))
            else:
                domain = connection.lookupByName(name)
        except:
            abort(404)

        domainDict = parseCommonDomain(domain)

        return jsonify(domainDict)

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