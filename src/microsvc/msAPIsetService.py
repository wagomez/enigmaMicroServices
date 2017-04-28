import os, sys
import requests
#import json
from flask import Flask, request, g, json
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
app.config['JSON_SORT_KEYS'] = False
api = Api(app)
app.config.from_envvar('NEWAPP_SETTINGS', silent=True)


#app.config.from_envvar('FLASKR_SETTINGS', silent=True)
#Simply define the environment variable FLASKR_SETTINGS that points to a config file to be loaded.
#The silent switch just tells Flask to not complain if no such environment key is set.
#parser = reqparse.RequestParser()
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



def nsoSetService(data_string, serviceName, serviceInstanceName):


    print("*******nsoSetService")
    print(data_string)

    existe=nsoValidateServiceInstance(serviceName, serviceInstanceName)

    #return data


    if(existe):
        verb = "PATCH"
        data_string = '{"tailf-ncs:services": ' + data_string + '}'
        #data={"tailf-ncs:services" : data}


    else:
        verb = "POST"


    #data = json.loads(data_string)
    data = data_string
    print("*******nsoSetService****** data a enviar")
    print(data)



    url = "http://" + NOSip + ":" + NSOpto + "/api/running/services/"

    headers = {'Content-Type': 'application/vnd.yang.data+json'}

    s = Session()

    req = requests.Request(verb, url,
                           data=data,
                           headers=headers,auth = (NSOuser,NSOpasswd)
                           )
    prepped = s.prepare_request(req)
    resp = s.send(prepped)
    print("***********RESPUESTA****************")
    respuesta={"text":resp.text, "status_code": resp.status_code}
    print (resp.text)
    return respuesta




class setService(Resource):
    def post(self,serviceName,serviceInstanceName):
        texto=request.data
        print("******contenido en texto=   ")
        print(type(texto))
        print(texto)

        texto=texto.decode('utf-8')
        print("******contenido en texto=   ")
        print(type(texto))
        print(texto)

        content_string=texto

        ##content = request.json

        ##print("******contenido me llego en=   ")
        ##print(type(content))
        ##print(content)

        ##content_string=json.dumps(content)
        ##print("******contenido en string=   ")
        ##print(type(content_string))
        ##print(content_string)

        ##content = json.loads(content_string)
        ##print("******contenido en dict=   ")
        ##print(type(content))
        ##print(content)


        regreso = nsoSetService(content_string,serviceName,serviceInstanceName)

        return {'response': regreso}, 201
        #return {serviceName:serviceInstanceName }

api.add_resource(setService,'/setService/<string:serviceName>/<string:serviceInstanceName>')
#api.add_resource(ItemList,'/items')

if __name__ == '__main__':
    if my_debug == 0:
        if (sys.argv.__len__() > 1):
            app.run(host="0.0.0.0", port=sys.argv[1])
        else:
            app.run(host="0.0.0.0", port="5054")
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