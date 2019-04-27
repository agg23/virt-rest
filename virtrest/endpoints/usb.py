from flask import jsonify, request
from flask_restful import Resource, abort

import re
import subprocess

from virtrest.connection import getConnection
from virtrest.endpoints.domain import getDomainWithErrors

class USB(Resource):
    def get(self):
        # From https://stackoverflow.com/questions/8110310/simple-way-to-query-connected-usb-devices-info-in-python/8265634#8265634
        device_re = re.compile("Bus\s+(?P<bus>\d+)\s+Device\s+(?P<device>\d+).+ID\s(?P<idVendor>\w+):(?P<idProduct>\w+)\s(?P<tag>.+)$", re.I)
        df = subprocess.check_output("lsusb").decode("utf-8")
        print(df)
        devices = []
        for i in df.split("\n"):
            if i:
                info = device_re.match(i)
                if info:
                    dinfo = info.groupdict()
                    dinfo["device"] = "/dev/bus/usb/%s/%s" % (dinfo.pop("bus"), dinfo.pop("device"))
                    tag = dinfo["tag"]
                    if tag is not None:
                        tag = tag.strip()
                        dinfo["tag"] = tag
                    devices.append(dinfo)

        return jsonify(devices)

class USBState(Resource):
    def post(self, domainName=None):
        jsonData = request.get_json()

        if jsonData is None:
            abort(400, message="No payload provided")

        if "action" not in jsonData:
            abort(400, message="No action provided")

        if "id" not in jsonData:
            abort(400, message="No id provided")
        
        action = jsonData["action"]
        usbId = jsonData["id"]

        domain = getDomainWithErrors(domainName)

        if usbId is None:
            abort(400, message="No USB ID provided")

        ids = extractIds(usbId)
        if ids is None:
            abort(400, message="USB ID \"{0}\" is invalid".format(usbId))

        idVendor, idProduct = ids
        xml = buildUSBXML(idVendor, idProduct)

        if action == "attach":
            domain.attachDevice(xml)
        elif action == "detach":
            domain.detachDevice(xml)
        else:
            abort(400, message="Invalid action provided")

def extractIds(usbId):
    splitId = usbId.split(":")

    if len(splitId) != 2:
        return None

    return splitId

def buildUSBXML(idVendor, idProduct):
    return """
        <hostdev mode='subsystem' type='usb'>
            <source>
                <vendor id='0x{0}'/>
                <product id='0x{1}'/>
            </source>
        </hostdev>
    """.format(idVendor, idProduct)
