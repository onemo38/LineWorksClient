import sys
import time
import jwt
import requests
import urllib
import json

class LineWorksClient:
    # constructor
    def __init__(self, api_id = "", server_id = "", private_key = "", consumer_key="", bot_no="", exp_min = 20):
        self.api_id = api_id
        self.server_id = server_id
        self.private_key = private_key
        self.exp_min = exp_min
        self.bot_no = bot_no
        self.consumer_key = consumer_key
        self.token = ""
    
    #get_server_token
    def get_server_token(self):
        #generate JWT token.
        #see https://developers.worksmobile.com/jp/document/1002002?lang=ja
        iss = self.server_id       #ServerId
        iat = int(time.time())     #JWT generated at
        exp = iat + (60 * self.exp_min)      #JWT expire at（after 20 minutes）
        #シークレットトークンの設定
        jwttoken = jwt.encode({'iss': iss, 'iat': iat, 'exp': exp}, self.private_key, algorithm='RS256')

        #get serverToken using JWT token
        url = 'https://authapi.worksmobile.com/b/' + self.api_id + '/server/token'
        headers = {"Content-Type": 'application/x-www-form-urlencoded; charset=UTF-8'}
        form = {
            "grant_type" : urllib.parse.quote("urn:ietf:params:oauth:grant-type:jwt-bearer"),
            "assertion" : jwttoken
        }
        try:
            res = requests.post(url=url, data=form, headers=headers)
            res_json = res.json()
            self.token = res_json['access_token']
            return self.token
        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise

    #send text message to specified room
    def send_text_message(self, roomId="", body=""):
        url = "https://apis.worksmobile.com/" + self.api_id + "/message/sendMessage/v2"
        data = {
            "botNo": int(self.bot_no),
            "roomId": roomId,
            "content": {
                "type": "text",
                "text": body
            }
        }
        json_data = json.dumps(data)
        headers = {
            'Content-Type': 'application/json;charset=UTF-8',
            'consumerKey': self.consumer_key,
            'Authorization': "Bearer " + self.token
        }
        print(self.token)
        try:
            res = requests.post(url=url, data=json_data, headers=headers)
            return res.text
        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise

