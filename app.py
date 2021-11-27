import json
import requests
from bs4 import BeautifulSoup as BS
from flask import Flask, render_template, Response, request


app = Flask(__name__, template_folder='templates')

headers = {"OAIS": "Bearer 996565bc-eedd-3696-9a87-3d19871f9638",
           "Authorization": "Bearer 996565bc-eedd-3696-9a87-3d19871f9638"}
proxy = {'https': 'https://xxx.x.xx.xxx:yyyy'}


def minjust_30101(orgName):
    params = {'name': orgName}
    url = 'https://apimgw.core.oais.by:10446/minjust-30101-directservice/v1/egr/short/name'
    response = requests.get(url=url, headers=headers, params=params, verify=False, proxies=proxy)
    if response.status_code == 200:
        return json.loads(response.text)
    raise ValueError("Response not 200")


def minjust_30102(regNum):
    pass


@app.route('/api/v1.0/oaismns/', methods=['GET'])
def oaisegr():
    if 'orgName' in request.args:
        orgname = str(request.args['orgName'])
    else:
        orgname = ''
    if 'regNum' in request.args:
        regnum = str(request.args['regNum'])
    else:
        regnum = ''
    if 'dateFrom' in request.args:
        datefrom = str(request.args['dateFrom'])
    else:
        datefrom = ''
    if 'dateTo' in request.args:
        dateto = str(request.args['dateTo'])
    else:
        dateto = ''


if __name__ == "__main__":
    app.run(debug=True)
