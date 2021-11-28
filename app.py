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
        return json.load(response.text)
    raise ValueError("Response not 200")


def minjust_30102(regNum):
    params = {'regNum': regNum}
    url = 'https://apimgw.core.oais.by:8247/minjust-30102-directservice/v1/egr/info/num'
    response = request.get(url=url, headers=headers, params=params, verify=False, proxies=proxy)
    if response.status_code == 200:
        return json.load(response.text)
    raise ValueError("Response not 200")


def minjust_30105(regNum, dateFrom):
    params = {
        'regNum': regNum,
        'dateFrom': dateFrom
    }
    url = 'https://apimgw.core.oais.by:8247/minjust-30105-directservice/v1/osp/num'
    response = request.get(url=url, headers=headers, params=params, verify=False, proxies=proxy)
    if response.status_code == 200:
        return json.load(response.text)
    raise ValueError("Response not 200")


def minjust_30106(regNum, dateFrom, dateTo):
    params = {
        'regNum': regNum,
        'dateFrom': dateFrom,
        'dateTo': dateTo
    }
    url = 'https://apimgw.core.oais.by:8247/minjust-30106-directservice/v1/egr/info/period'
    response = request.get(url=url, headers=headers, params=params, verify=False, proxies=proxy)
    if response.status_code == 200:
        return json.load(response.text)
    raise ValueError("Response not 200")


@app.route('/api/v1.0/oaisegr', methods=['GET'])
def oaisegr():
    if 'regNum' in request.args:
        # 1 и 4 условие
        if 'dateFrom' not in request.args and 'dateTo' not in request.args:
            regNum = str(request.args['regNum'])
            dateFrom = ''
            data_30102 = minjust_30102(regNum)
            data_30105 = minjust_30105(regNum, dateFrom)

            unp = regNum
            vnaim = data_30102["EGRInfo"]["egr0332"]["VNAIM"]
            vnsostp = data_30102["EGRInfo"]["egr01"]["VNSOSTP"]
            if vnsostp == 'Действующий':
                vnsostp = '<font color = "green">Действующий</font>'
            elif vnsostp == 'Ликвидирован':
                vnsostp = '<font color = "red">Ликвидирован</font>'
            elif vnsostp == 'В процессе ликвидации':
                vnsostp = '<font color = "black">В процессе ликвидации</font>'
            # Данные для адреса
            if "VREGION" in data_30102["EGRInfo"]["egr0321"]:
                vregion = data_30102["EGRInfo"]["egr0321"]["VREGION"] + ' обл.,'
            else:
                vregion = ''
            vntnpp = data_30102["EGRInfo"]["egr0321"]["VNTNPP"][0] + '. '
            vnp = data_30102["EGRInfo"]["egr0321"]["VNP"] + ', '
            vntulp = data_30102["EGRInfo"]["egr0321"]["VNTULP"] + ' '
            vulitsa = data_30102["EGRInfo"]["egr0321"]["VULITSA"] + ', '
            vdom = 'д. ' + data_30102["EGRInfo"]["egr0321"]["VDOM"] + ', '
            if "VKORP" in data_30102["EGRInfo"]["egr0321"]:
                vkorp = "корп. " + data_30102["EGRInfo"]["egr0321"]["VKORP"] + ', '
            else:
                vkorp = ''
            vntpomp = data_30102["EGRInfo"]["egr0321"]["VNTPOMP"] + ' '
            vpom = data_30102["EGRInfo"]["egr0321"]["VPOM"]

            html_head_1 = '<table class="simple-little-table"cellspacing="0"><thead><tr>'\
                '<th>УНП</th>' \
                '<th>Название</th>' \
                '<th>Адрес</th>' \
                '<th>Руководитель</th>' \
                '<th>Статус</th>' \
                '<th class="hide_on_print"></th>' \
                '</tr></thead><tbody>'

            dropdown = '<div class="dropdown-content">' \
                '<a href="/auto/?unp_get=' + regNum + '" target="_blank" title="Автотранспорт на организации">ГАИ Авто</a>' \
                '<a href="/fsznrb/?unp_get=' + regNum + '" target="_blank" title="Работники">ФСЗН</a>' \
                '<a href="/mnscard-oais/?unp_get=' + regNum + '" target="_blank" title="Уастие в закупках">Закупки (уч-к)</a>' \
                '</div>'
                #    '<a href="/zakupki/?unp_get=' + regNum + '" target="_blank" title="Уастие в закупках">Закупки (уч-к)</a>' \

            address = vregion + vntnpp + vnp + vntulp + vulitsa + vdom + vkorp + vntpomp + vpom
            

            if "egr0332" in data_30102["EGRInfo"]:
                pass
                # Юр. лицо
                # link = 
            else:
                # Физ. лицо
                pass
                # Не нашел поле с номером паспорта в 30102 и 30105
                # num_pass = 
                # link = '<a href="/passport/?Pnum=' + regNum + '"'
            link = ''

            cod = '<tr class="table-data">' \
                '<td><div class="dropdown"><div class="dropbtn">' \
                + regNum + '</div>' + dropdown + '</div></td>' \
                '<td>' + vnaim + '</td>' \
                '<td>' + address + '</td>' \
                '<td>' + link + data_30102["EGRInfo"]["egr0302"]["VNAIM"] + '</td>' \
                '<td>' + vnsostp + '</td>' \
                '<td class="hide_on_print"><div  align="center"><a id="more" href="/mnscard-oais/?vunp=' + regNum + '" target="_blank">Подробнее</a></div></td></tr>'

            return html_head_1 + cod

        # 3 условие
        elif 'dateFrom' in request.args and 'dateTo' in request.args:
            regNum = str(request.args['regNum'])
            dateFrom = str(request.args['dateFrom'])
            dateTo = str(request.args['dateTo'])
            data_30106 = minjust_30106(regNum, dateFrom, dateTo)
    # 2 условие
    elif 'orgName' in request.args:
        orgName = str(request.args['orgName'])
        data_30101 = minjust_30101(orgName)


if __name__ == "__main__":
    app.run(debug=True)