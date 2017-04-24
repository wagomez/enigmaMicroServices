import os, sys
import requests
import json
from flask import Flask, request, g
from flask_restful import reqparse, Resource, Api
from settings.base import *
from requests import Session



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
parser = reqparse.RequestParser()
#parser.add_argument('tailf-ncs:services')


def nsoValidateServiceInstance(serviceName, serviceInstanceName):

    url = "http://" + NOSip + ":" + NSOpto + "/api/running/services/" +serviceName +"/"+serviceInstanceName

    headers = {'Accept': 'application/vnd.yang.data+json'}

    req = requests.get(url, headers=headers, auth=(NSOuser, NSOpasswd))

    #return url

    if req.status_code == 404:
        return False
    else:
        return True



def nsoSetService(data, serviceName, serviceInstanceName):

    print("*******nsoSetService")
    print(data)

    existe=nsoValidateServiceInstance(serviceName, serviceInstanceName)
    #data = "{" + data + "}"
    #return data


    if(existe):
        verb = "PATCH"
        data = '{' \
               '"tailf-ncs:services": ' + data + '}'

    else:
        verb = "POST"

    print("*******nsoSetService****** data a enviar")
    print(data)

    data = json.loads(data)

    url = "http://" + NOSip + ":" + NSOpto + "/api/running/services/"

    headers = {'Content-Type': 'application/vnd.yang.data+json'}
    s = Session()

    req = requests.Request(verb, url,
                           data=data,
                           headers=headers,auth = (NSOuser,NSOpasswd)
                           )
    prepped = s.prepare_request(req)
    resp = s.send(prepped)
    print("***************************")
    print (resp.text)
    return resp




class setIntCableCont(Resource):
    def post(self,serviceName,serviceInstanceName):
        content = request.json

        content = json.dumps(content)

        regreso = nsoSetService(content,serviceName,serviceInstanceName)

        return {'item': regreso}, 201
        #return {serviceName:serviceInstanceName }

api.add_resource(setIntCableCont,'/setIntCableCont/<string:serviceName>/<string:serviceInstanceName>')
#api.add_resource(ItemList,'/items')

if __name__ == '__main__':
    if my_debug == 0:
        if (sys.argv.__len__() > 1):
            app.run(host="127.0.0.1", port=sys.argv[1])
        else:
            app.run(host="127.0.0.1", port="5053")
    else:

        datos = '{' \
                '"controllerIntegratedCable:controllerIntegratedCable": [' \
                '{' \
                '"servicename": "cbr8-1_3-0-0_contIntegratedCable",' \
                '"device": "cbr8-1",' \
                '"card": "3",' \
                '"numDS": "8",' \
                '"freqIni": "591000000",' \
                '"endDS": "7"' \
                '}' \
                ']' \
                '}'

        regreso = nsoSetService(datos,"controllerIntegratedCable","cbr8-1_3-0-0_contIntegratedCable")
        # api_getDevices()
        print(regreso)
        print("done")

    #if __name__ == '__main__':
    #    app.run(debug=True)