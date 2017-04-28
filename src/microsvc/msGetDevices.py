import sys
import requests
from flask import Flask, url_for, request
import json
from requests import Request, Session
import os
from settings.base import *

app = Flask(__name__)


my_debug = 0


#NOSip="127.0.0.1"
#NSOpto="8080"
#NSOuser="admin"
#NSOpasswd="admin"


#print (NOS_CONF["NOSip"])
NOSip = NOS_CONF['NOSip']
NSOpto=NOS_CONF['NSOpto']
NSOuser=NOS_CONF['NSOuser']
NSOpasswd=NOS_CONF['NSOpasswd']

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


@app.route('/getDevicesGroup/<gpoOfDevices>/')
def api_getDevicesGroup(gpoOfDevices):

    devices = nsoGetDevices(gpoOfDevices)

    a=1

    #return devices
    return json.dumps(devices)

@app.route('/getDevices/')
def api_getDevices():
    allDevices = {}
    gpoCMTS="CMTS"
    gpoPE="PE"
    devices = nsoGetDevices(gpoCMTS)



    allDevices[gpoCMTS]=devices
    devices = nsoGetDevices(gpoPE)
    allDevices[gpoPE] = devices

    return json.dumps(allDevices)

if __name__ == '__main__':
    #app.run(port=sys.argv[1])
    if my_debug == 0:
        if (sys.argv.__len__()>1):
            app.run( host="0.0.0.0", port=sys.argv[1])
        else:
            app.run( host="0.0.0.0", port="5052")
    else:
        print ("debugeando")
        #infoInt=testGetSaturationIndex()
        #intSatIndex = api_getSatIndex(infoInt,"172.16.1.108")

        #intSatIndex= json.loads(intSatIndex)
        #final = api_getNoSatLc(intSatIndex,"172.16.1.108")

        #final = json.loads(final)

        respuesta=api_getDevicesGroup("CMTS")
        #api_getDevices()
        print(respuesta)

        print ("done")
