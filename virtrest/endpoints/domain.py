from flask import jsonify
from flask_restful import Resource

from virtrest.connection import getConnection

class Domain(Resource):
    def get(self):
        connection = getConnection()

        allDomains = {}

        for domain in connection.listAllDomains():
            domainId = domain.ID()

            domainDict = {}
            domainDict["name"] = domain.name()
            domainDict["osType"] = domain.OSType()
            info = parseInfo(domain.info())
            if info is not None:
                domainDict["info"] = info

            domainDict["running"] = domain.isActive() == 1

            allDomains[domainId] = domainDict

        return jsonify(allDomains)

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