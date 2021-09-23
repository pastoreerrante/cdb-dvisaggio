from flask import Flask, request
from webexteamssdk import WebexTeamsAPI, Webhook
from cardcontent import *
import smartsheet

app = Flask(__name__)
api = WebexTeamsAPI(access_token="YmQ1MTM1MTUtNmE4Ni00YmY4LTg2ZGQtYWFmZmFkODlhMDM5ODdiM2IxMjQtNzNm_PF84_0198f08a-3880-4871-b55e-4863ccf723d5")

@app.route('/', methods=['POST', 'GET'])
def home():
    return 'OK', 200

@app.route('/webhookreq', methods=['POST', 'GET'])
def webhookreq():
    if request.method == 'POST':
        req = request.get_json()
        data_personId = req['data']['personId']
        data_roomId = req['data']['roomId']
        #Loop prevention VERY IMPORTNAT!
        me = api.people.me()
        if data_personId == me.id:
            return 'OK', 200
        else:
            if api.messages.create(roomId=data_roomId, text='Hello Dawg!!!', attachments=[{"contentType": "application/vnd.microsoft.card.adaptive", "content":
cardcontent}]):
                return "OK"

    elif request.method == 'GET':
        return "Yes, this is working."
    
    return 'OK', 200

@app.route('/cardsubmitted', methods=['POST'])
def cardsubmitted():
    if request.method == 'POST':
        req = request.get_json()
        data_id = req['data']['id']
        attachment_actions = api.attachment_actions.get(data_id)
        inputs = attachment_actions.inputs
        myName = inputs['myName']
        myEmail = inputs['myEmail']
        myTel = inputs['myTel']
        print(myName)
        print(myEmail)
        print(myTel)
        smart = smartsheet.Smartsheet('qQjWXjxpPlVCcwsKs7Kb8thI4RL5drVxEDcB0') #Smartsheet Access Token
        smart.errors_as_exceptions(True)
        # Specify cell values for the added row
        newRow = smartsheet.models.Row()
        newRow.to_top = True
        # The above variables are the incoming JSON
        newRow.cells.append({ 'column_id': 2301578106431364, 'value': myName })
        #
        newRow.cells.append({ 'column_id': 1175678199588740, 'value': myEmail, 'strict': False })
        newRow.cells.append({ 'column_id': 3427478013273988, 'value': myTel, 'strict': False })
        response = smart.Sheets.add_rows(502961223821188, newRow) # The -- xxxxxxxxxxxxxx -- on this line is the sheet ID.
    return 'OK', 200

if __name__=='__main__':
    app.debug = True
    app.run(host="0.0.0.0")