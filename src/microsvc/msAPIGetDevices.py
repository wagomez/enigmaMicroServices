import os, sys
import requests
import json
from flask import Flask, request, g
from flask_restful import Resource, Api
from microsvc.settings.base import *

NOSip = NOS_CONF['NOSip']
NSOpto=NOS_CONF['NSOpto']
NSOuser=NOS_CONF['NSOuser']
NSOpasswd=NOS_CONF['NSOpasswd']

my_debug = 0

etiqueta = "estoy dentro de newApp"

app = Flask(__name__)
app.config.from_object(__name__)
api = Api(app)
app.config.from_envvar('NEWAPP_SETTINGS', silent=True)
#app.config.from_envvar('FLASKR_SETTINGS', silent=True)
#Simply define the environment variable FLASKR_SETTINGS that points to a config file to be loaded.
#The silent switch just tells Flask to not complain if no such environment key is set.


def nsoGetDevices(gpoDevices):
    url = "http://" + NOSip + ":" + NSOpto + "/api/running/devices/device-group/" + gpoDevices
    # return url
    headers = {'Accept': 'application/vnd.yang.data+json'}
    req = requests.get(url, headers=headers, auth=(NSOuser, NSOpasswd))

    #groupOfDevices = req.json()
    groupOfDevices = json.loads(req.text)
    a=1
    groupOfDevices=groupOfDevices['tailf-ncs:device-group']['device-name']
    return groupOfDevices



def api_getDevicesGroup(gpoOfDevices):

    devices = nsoGetDevices(gpoOfDevices)

    a=1

    #return devices
    return json.dumps(devices)


class getDevicesGroup(Resource):
    def get(self,gpoOfDevices):
        devices=nsoGetDevices(gpoOfDevices)
        if(devices):
            return devices
        return {'item': None}, 404


api.add_resource(getDevicesGroup,'/getDevicesGroup/<string:gpoOfDevices>')
#api.add_resource(ItemList,'/items')

if __name__ == '__main__':
    if my_debug == 0:
        if (sys.argv.__len__() > 1):
            app.run(host="127.0.0.1", port=sys.argv[1])
        else:
            app.run(host="127.0.0.1", port="5052")
    else:
        respuesta = api_getDevicesGroup("PE")
        # api_getDevices()
        print(respuesta)
        print("done")

    #if __name__ == '__main__':
    #    app.run(debug=True)