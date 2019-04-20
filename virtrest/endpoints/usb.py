from flask import jsonify
from flask_restful import Resource

import re
import subprocess

from virtrest.connection import getConnection

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