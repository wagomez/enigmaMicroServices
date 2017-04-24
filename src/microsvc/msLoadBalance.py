import sys
import requests
from flask import Flask, url_for, request
import json
from requests import Request, Session

app = Flask(__name__)

my_debug = 0


NOSip="127.0.0.1"
NSOpto="8080"
NSOuser="admin"
NSOpasswd="admin"



def nsoValidateLoadBalanceD3Service(loadBalanceD3serviceName):

    url = "http://" + NOSip + ":" + NSOpto + "/api/running/services/cableDocsis3LoadBalance/"+loadBalanceD3serviceName
    # return url
    headers = {'Accept': 'application/vnd.yang.data+json'}
    req = requests.get(url, headers=headers, auth=(NSOuser, NSOpasswd))
    if req.status_code == 404:
        return False
    else:
        return True

def nsoRemoveLoadBalanceD3(cmts, loadBalanceD3,loadBalanceD3serviceName):


    serviceValidate = nsoValidateLoadBalanceD3Service(loadBalanceD3serviceName)


    if serviceValidate == True:
        url = "http://" + NOSip + ":" + NSOpto + "/api/running/services/cableDocsis3LoadBalance:cableDocsis3LoadBalance/" + loadBalanceD3serviceName + "/_operations/un-deploy"
        # return url
        headers = ""
        new = ""
        s = Session()
        req = Request('POST', url,
                      data=new,
                      headers=headers,
                      auth=(NSOuser, NSOpasswd)
                      )
        prepped = s.prepare_request(req)

        # do something with prepped.body
        # do something with prepped.headers

        resp = s.send(prepped)
        statusCode = resp.status_code;


    return 1

def nsoLoadBalanceD3(cmts,loadbalanceD3,loadBalanceD3serviceName):


    serviceValidate=nsoValidateLoadBalanceD3Service(loadBalanceD3serviceName)

    if serviceValidate == False:

        url = "http://"+NOSip+":"+NSOpto+"/api/running/services"
        #return url
        headers = {'Content-Type': 'application/vnd.yang.data+json'}

        new = "{" \
              "\"cableDocsis3LoadBalance:cableDocsis3LoadBalance\""+": [" \
      "{" \
            "\"servicename\": \""+loadBalanceD3serviceName+"\"," \
            "\"device\": \""+cmts+"\"" \
      "}" \
      "]" \
      "}"

    else:


        url = "http://" + NOSip + ":" + NSOpto + "/api/running/services/cableDocsis3LoadBalance:cableDocsis3LoadBalance/"+loadBalanceD3serviceName+"/_operations/re-deploy"
        # return url
        headers = ""
        new = ""
    s = Session()
    req = Request('POST', url,
                  data=new,
                  headers=headers,
                  auth=(NSOuser, NSOpasswd)
                  )
    prepped = s.prepare_request(req)

    # do something with prepped.body
    # do something with prepped.headers

    resp = s.send(prepped)
    statusCode = resp.status_code;




    return 1


def nsoValidateLoadBalanceD2Service(loadBalanceD2serviceName):

    url = "http://" + NOSip + ":" + NSOpto + "/api/running/services/cableDocsisLoadBalance/"+loadBalanceD2serviceName

    headers = {'Accept': 'application/vnd.yang.data+json'}

    req = requests.get(url, headers=headers, auth=(NSOuser, NSOpasswd))

    #return url

    if req.status_code == 404:
        return False
    else:
        return True


def nsoRemoveLoadBalanceD2(cmts, loadBalanceD2,loadBalanceD2serviceName):
    serviceValidate = nsoValidateLoadBalanceD2Service(loadBalanceD2serviceName)


    if serviceValidate == True:
        url = "http://" + NOSip + ":" + NSOpto + "/api/running/services/cableDocsisLoadBalance:cableDocsisLoadBalance/" + loadBalanceD2serviceName + "/_operations/un-deploy"
        # return url
        headers = ""
        new = ""
        s = Session()
        req = Request('POST', url,
                      data=new,
                      headers=headers,
                      auth=(NSOuser, NSOpasswd)
                      )
        prepped = s.prepare_request(req)

        # do something with prepped.body
        # do something with prepped.headers

        resp = s.send(prepped)
        statusCode = resp.status_code;
        text = resp.text;

    return 1



def nsoLoadBalanceD2(cmts,loadbalanceD2,loadBalanceD2serviceName):

    #return cmts + "   " + loadBalanceD2serviceName
    serviceValidate=nsoValidateLoadBalanceD2Service(loadBalanceD2serviceName)

    #return serviceValidate + "   " + cmts + "   " + loadBalanceD2serviceName

    if serviceValidate == False:

        url = "http://"+NOSip+":"+NSOpto+"/api/running/services"
        #return url
        headers = {'Content-Type': 'application/vnd.yang.data+json'}

        new = "{" \
              "\"cableDocsisLoadBalance:cableDocsisLoadBalance\""+": [" \
      "{" \
            "\"servicename\": \""+loadBalanceD2serviceName+"\"," \
            "\"device\": \""+cmts+"\"" \
      "}" \
      "]" \
      "}"

    else:


        url = "http://" + NOSip + ":" + NSOpto + "/api/running/services/cableDocsisLoadBalance:cableDocsisLoadBalance/"+loadBalanceD2serviceName+"/_operations/re-deploy"
        # return url
        headers = ""
        new = ""
    s = Session()
    req = Request('POST', url,
                  data=new,
                  headers=headers,
                  auth=(NSOuser, NSOpasswd)
                  )
    prepped = s.prepare_request(req)

    # do something with prepped.body
    # do something with prepped.headers

    resp = s.send(prepped)
    statusCode = resp.status_code;

    return 1


@app.route('/setLoadBalance/<cmts>/<loadBalanceD2>/<loadBalanceD3>/')
def api_setLoadBalance(cmts,loadBalanceD2,loadBalanceD3):
    loadBalanceD2serviceName = "loadbalance" + cmts
    loadBalanceD3serviceName = "loadbalance3" + cmts
    #return cmts+ "   " + loadBalanceD2+ "   "+ loadBalanceD3 + "   " + loadBalanceD3serviceName
    if loadBalanceD2=="1":
        a=nsoLoadBalanceD2(cmts, loadBalanceD2,loadBalanceD2serviceName)
        b=a

    if loadBalanceD2=="0":
        nsoRemoveLoadBalanceD2(cmts, loadBalanceD2,loadBalanceD2serviceName)


    if loadBalanceD3=="1":
        nsoLoadBalanceD3(cmts, loadBalanceD3,loadBalanceD3serviceName)
    if loadBalanceD3=="0":
        nsoRemoveLoadBalanceD3(cmts, loadBalanceD3,loadBalanceD3serviceName)

    return "OK"

if __name__ == '__main__':
    #app.run(port=sys.argv[1])
    if my_debug == 0:
        if (sys.argv.__len__()>1):
            app.run( host="127.0.0.1", port=sys.argv[1])
        else:
            app.run( host="127.0.0.1", port="5051")
    else:
        print ("debugeando")
        #infoInt=testGetSaturationIndex()
        #intSatIndex = api_getSatIndex(infoInt,"172.16.1.108")

        #intSatIndex= json.loads(intSatIndex)
        #final = api_getNoSatLc(intSatIndex,"172.16.1.108")

        #final = json.loads(final)

        api_setLoadBalance("cbr8-1", "1", "1")

        print ("done")
