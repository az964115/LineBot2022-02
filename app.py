from __future__ import unicode_literals
from flask import Flask, request, abort, render_template
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import requests
import json
import configparser
import os
from urllib import parse
app = Flask(__name__, static_url_path='/static')
UPLOAD_FOLDER = 'static'
ALLOWED_EXTENSIONS = set(['pdf', 'png', 'jpg', 'jpeg', 'gif'])


config = configparser.ConfigParser()
config.read('config.ini')

line_bot_api = LineBotApi(config.get('line-bot', 'channel_access_token'))
handler = WebhookHandler(config.get('line-bot', 'channel_secret'))
my_line_id = config.get('line-bot', 'my_line_id')
end_point = config.get('line-bot', 'end_point')
line_login_id = config.get('line-bot', 'line_login_id')
line_login_secret = config.get('line-bot', 'line_login_secret')
my_phone = config.get('line-bot', 'my_phone')
# link1 = "https://zh.wikipedia.org/wiki/%E5%8F%AF%E5%8F%AF%E8%B1%86"
# link2 = "https://heho.com.tw/archives/78396"
HEADER = {
    'Content-type': 'application/json',
    'Authorization': F'Bearer {config.get("line-bot", "channel_access_token")}'
}


@app.route("/", methods=['POST', 'GET'])
def index():
    if request.method == 'GET':
        return 'ok'
    body = request.json
    events = body["events"]
    print(body)
    if "replyToken" in events[0]:
        payload = dict()
        replyToken = events[0]["replyToken"]
        payload["replyToken"] = replyToken
        if events[0]["type"] == "message":
            if events[0]["message"]["type"] == "text":
                text = events[0]["message"]["text"]
                if text == "TC-綜合巧克力禮盒(小盒/12片)":
                    payload["messages"] = [get1(),
                                          {"type": "text",
                                "text": "NT$ 550"}]
                elif text == "TC-柴燒黑糖巧克力":
                    payload["messages"] = [get2(),
                                          {"type": "text",
                                "text": "NT$ 300"}]
                elif text == "TC-100%無糖巧克力磚":
                    payload["messages"] = [get3(),
                                          {"type": "text",
                                "text": "NT$ 300"}]
                elif text == "TC-95%巧克力磚":
                    payload["messages"] = [get3(),
                                          {"type": "text",
                                "text": "NT$ 300"}]
                elif text == "TC-85%巧克力磚":
                    payload["messages"] = [get3(),
                                          {"type": "text",
                                "text": "NT$ 300"}]
                elif text == "TC-75%巧克力磚":
                    payload["messages"] = [get3(),
                                          {"type": "text",
                                "text": "NT$ 300"}]
                elif text == "TC 95%巧克力禮盒":
                    payload["messages"] = [get4(),
                                          {"type": "text",
                                "text": "NT$ 999"}]
                elif text == "TC-綜合巧克力禮盒":
                    payload["messages"] = [get5(),
                                          {"type": "text",
                                "text": "NT$ 900"}]
                elif text == "TC 85%巧克力禮盒":
                    payload["messages"] = [get6(),
                                          {"type": "text",
                                "text": "NT$ 899"}]
                elif text == "TC-紅藜巧克力BAR":
                    payload["messages"] = [get7(),
                                          {"type": "text",
                                "text": "NT$ 300"}]
                elif text == "TC-牛奶巧克力BAR":
                    payload["messages"] = [get7(),
                                          {"type": "text",
                                "text": "NT$ 300"}]
                elif text == "TC-海鹽巧克力BAR":
                    payload["messages"] = [get7(),
                                          {"type": "text",
                                "text": "NT$ 300"}]
                elif text == "TC-花生巧克力BAR":
                    payload["messages"] = [get7(),
                                          {"type": "text",
                                "text": "NT$ 300"}]
                elif text == "TC-95%黑巧克力冰淇淋":
                    payload["messages"] = [get8(),
                                          {"type": "text",
                                "text": "NT$ 100"}]
                elif text == "TC-抹茶拿鐵生巧克力":
                    payload["messages"] = [get9(),
                                          {"type": "text",
                                "text": "NT$ 380"}]
                elif text == "TC-經典生巧克力":
                    payload["messages"] = [get10(),
                                          {"type": "text",
                                "text": "NT$ 380"}]
                elif text == "禮盒":
                    payload["messages"] = [
                            {
                                "type": "template",
                                "altText": "This is a buttons template",
                                "template": {
                                  "type": "buttons",
                                  "title": "巧克力禮盒",
                                  "text": "熱門商品",
                                  "actions": [
                                      {
                                        "type": "message",
                                        "label": "TC-綜合巧克力禮盒",
                                        "text": "TC-綜合巧克力禮盒"
                                      },
                                      {
                                        "type": "message",
                                        "label": "TC-綜合巧克力禮盒(小盒/12片)",
                                        "text": "TC-綜合巧克力禮盒"
                                      },
                                      {
                                        "type": "message",
                                        "label": "TC 95%巧克力禮盒",
                                        "text": "TC 95%巧克力禮盒"
                                      },
                                      {
                                        "type": "message",
                                        "label": "TC 85%巧克力禮盒",
                                        "text": "TC 85%巧克力禮盒"
                                      }
                                  ]
                               }
                            }
                        ]
                elif text == "巧克力磚":
                    payload["messages"] = [
                            {
                                "type": "template",
                                "altText": "This is a buttons template",
                                "template": {
                                  "type": "buttons",
                                  "title": "巧克力磚",
                                  "text": "熱門商品",
                                  "actions": [
                                      {
                                        "type": "message",
                                        "label": "TC-100%無糖巧克力磚",
                                        "text": "TC-100%無糖巧克力磚"
                                      },
                                      {
                                        "type": "message",
                                        "label": "TC-95%巧克力磚",
                                        "text": "TC-95%巧克力磚"
                                      },
                                      {
                                        "type": "message",
                                        "label": "TC-85%巧克力磚",
                                        "text": "TC-85%巧克力磚"
                                      },
                                      {
                                        "type": "message",
                                        "label": "TC-75%巧克力磚",
                                        "text": "TC-75%巧克力磚"
                                      }
                                  ]
                               }
                            }
                        ]
                elif text == "巧克力BAR":
                    payload["messages"] = [
                            {
                                "type": "template",
                                "altText": "This is a buttons template",
                                "template": {
                                  "type": "buttons",
                                  "title": "巧克力BAR",
                                  "text": "熱門商品",
                                  "actions": [
                                      {
                                        "type": "message",
                                        "label": "TC-紅藜巧克力BAR",
                                        "text": "TC-紅藜巧克力BAR"
                                      },
                                      {
                                        "type": "message",
                                        "label": "TC-牛奶巧克力BAR",
                                        "text": "TC-牛奶巧克力BAR"
                                      },
                                      {
                                        "type": "message",
                                        "label": "TC-海鹽巧克力BAR",
                                        "text": "TC-海鹽巧克力BAR"
                                      },
                                      {
                                        "type": "message",
                                        "label": "TC-花生巧克力BAR",
                                        "text": "TC-花生巧克力BAR"
                                      }
                                  ]
                               }
                            }
                        ]
                elif text == "其他系列":
                    payload["messages"] = [
                            {
                                "type": "template",
                                "altText": "This is a buttons template",
                                "template": {
                                  "type": "buttons",
                                  "title": "其他系列",
                                  "text": "商品清單",
                                  "actions": [
                                      {
                                        "type": "message",
                                        "label": "TC-柴燒黑糖巧克力",
                                        "text": "TC-柴燒黑糖巧克力"
                                      },
                                      {
                                        "type": "message",
                                        "label": "TC-95%黑巧克力冰淇淋",
                                        "text": "TC-95%黑巧克力冰淇淋"
                                      },
                                      {
                                        "type": "message",
                                        "label": "TC-抹茶拿鐵生巧克力",
                                        "text": "TC-抹茶拿鐵生巧克力"
                                      },
                                      {
                                        "type": "message",
                                        "label": "TC-經典生巧克力",
                                        "text": "TC-經典生巧克力"
                                      }
                                  ]
                               }
                            }
                        ]
                elif text == "主選單":
                    payload["messages"] = [
                            {
                                "type": "template",
                                "altText": "This is a buttons template",
                                "template": {
                                  "type": "buttons",
                                  "title": "tc巧鋪歡迎您",
                                  "text": "商品價格查詢",
                                  "actions": [
                                      {
                                        "type": "message",
                                        "label": "禮盒",
                                        "text": "禮盒"
                                      },
                                      {
                                        "type": "message",
                                        "label": "巧克力BAR",
                                        "text": "巧克力BAR"
                                      },
                                      {
                                        "type": "message",
                                        "label": "巧克力磚",
                                        "text": "巧克力磚"
                                      },
                                      {
                                        "type": "message",
                                        "label": "其他系列",
                                        "text": "其他系列"
                                      }
                                  ]
                               }
                           }
                        ]
                else:
                    payload["messages"] = [
                            {
                                "type": "text",
                                "text": text
                            }
                        ]
                replyMessage(payload)
            elif events[0]["message"]["type"] == "location":
                title = events[0]["message"]["title"]
                latitude = events[0]["message"]["latitude"]
                longitude = events[0]["message"]["longitude"]
                payload["messages"] = [getLocationConfirmMessage(title, latitude, longitude)]
                replyMessage(payload)
        elif events[0]["type"] == "postback":
            if "params" in events[0]["postback"]:
                reservedTime = events[0]["postback"]["params"]["datetime"].replace("T", " ")
                payload["messages"] = [
                        {
                            "type": "text",
                            "text": F"已完成預約於{reservedTime}的叫車服務"
                        }
                    ]
                replyMessage(payload)
            else:
                data = json.loads(events[0]["postback"]["data"])
                action = data["action"]
                if action == "get_near":
                    data["action"] = "get_detail"
                    payload["messages"] = [getCarouselMessage(data)]
                elif action == "get_detail":
                    del data["action"]
                    payload["messages"] = [getTaipei101ImageMessage(),
                                           getTaipei101LocationMessage(),
                                           getMRTVideoMessage(),
                                           getCallCarMessage(data)]
                replyMessage(payload)

    return 'OK'


@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    try:
        handler.handle(body, signature)

    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def pretty_echo(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text)
        )


@app.route("/sendTextMessageToMe", methods=['POST'])
def sendTextMessageToMe():
    pushMessage({})
    return 'OK'

def getCarouselMessage(data):
    message = dict()
    return message

def get1(originalContentUrl=F"https://github.com/az964115/LineBot2022-02/blob/main/static/1.jpg?raw=true"): #{end_point}/static/378.jp
    return getImageMessage(originalContentUrl)

def getImageMessage(originalContentUrl):
    message = dict()
    message["type"] = "image"
    message["originalContentUrl"] = "https://github.com/az964115/LineBot2022-02/blob/main/static/1.jpg?raw=true" #originalContentUrl
    message["previewImageUrl"] = "https://github.com/az964115/LineBot2022-02/blob/main/static/1.jpg?raw=true" #originalContentUrl
    return message

def get2(originalContentUrl=F"https://github.com/az964115/LineBot2022-02/blob/main/static/1.jpg?raw=true"): #{end_point}/static/378.jp
    return getImageMessage2(originalContentUrl)

def getImageMessage2(originalContentUrl):
    message = dict()
    message["type"] = "image"
    message["originalContentUrl"] = "https://raw.githubusercontent.com/az964115/LineBot2022-02/main/static/2.jpg" #originalContentUrl
    message["previewImageUrl"] = "https://raw.githubusercontent.com/az964115/LineBot2022-02/main/static/2.jpg" #originalContentUrl
    return message

def get3(originalContentUrl=F"{end_point}/static/378.jp"):
    return getImageMessage3(originalContentUrl)

def getImageMessage3(originalContentUrl):
    message = dict()
    message["type"] = "image"
    message["originalContentUrl"] = "https://github.com/az964115/LineBot2022-02/blob/main/static/3.jpg?raw=true" #originalContentUrl
    message["previewImageUrl"] = "https://github.com/az964115/LineBot2022-02/blob/main/static/3.jpg?raw=true" #originalContentUrl
    return message

def get4(originalContentUrl=F"{end_point}/static/378.jp"):
    return getImageMessage4(originalContentUrl)

def getImageMessage4(originalContentUrl):
    message = dict()
    message["type"] = "image"
    message["originalContentUrl"] = "https://raw.githubusercontent.com/az964115/LineBot2022-02/main/static/4.jpg" #originalContentUrl
    message["previewImageUrl"] = "https://raw.githubusercontent.com/az964115/LineBot2022-02/main/static/4.jpg" #originalContentUrl
    return message

def get5(originalContentUrl=F"{end_point}/static/378.jp"):
    return getImageMessage5(originalContentUrl)

def getImageMessage5(originalContentUrl):
    message = dict()
    message["type"] = "image"
    message["originalContentUrl"] = "https://cdn.store-assets.com/s/632442/i/20113307.jpg?width=1024&format=webp" #originalContentUrl
    message["previewImageUrl"] = "https://cdn.store-assets.com/s/632442/i/20113307.jpg?width=1024&format=webp" #originalContentUrl
    return message

def get6(originalContentUrl=F"{end_point}/static/378.jp"):
    return getImageMessage6(originalContentUrl)

def getImageMessage6(originalContentUrl):
    message = dict()
    message["type"] = "image"
    message["originalContentUrl"] = "https://cdn.store-assets.com/s/632442/i/20058553.jpg?width=480&format=webp" #originalContentUrl
    message["previewImageUrl"] = "https://cdn.store-assets.com/s/632442/i/20058553.jpg?width=480&format=webp" #originalContentUrl
    return message

def get7(originalContentUrl=F"{end_point}/static/378.jp"):
    return getImageMessage7(originalContentUrl)

def getImageMessage7(originalContentUrl):
    message = dict()
    message["type"] = "image"
    message["originalContentUrl"] = "https://cdn.store-assets.com/s/632442/i/20280325.png?width=480&format=webp" #originalContentUrl
    message["previewImageUrl"] = "https://cdn.store-assets.com/s/632442/i/20280325.png?width=480&format=webp" #originalContentUrl
    return message

def get8(originalContentUrl=F"{end_point}/static/378.jp"):
    return getImageMessage8(originalContentUrl)

def getImageMessage8(originalContentUrl):
    message = dict()
    message["type"] = "image"
    message["originalContentUrl"] = "https://cdn.store-assets.com/s/632442/i/20212428.jpg?width=480&format=webp" #originalContentUrl
    message["previewImageUrl"] = "https://cdn.store-assets.com/s/632442/i/20212428.jpg?width=480&format=webp" #originalContentUrl
    return message

def get9(originalContentUrl=F"{end_point}/static/378.jp"):
    return getImageMessage9(originalContentUrl)

def getImageMessage9(originalContentUrl):
    message = dict()
    message["type"] = "image"
    message["originalContentUrl"] = "https://cdn.store-assets.com/s/632442/i/20123932.jpg?width=480&format=webp" #originalContentUrl
    message["previewImageUrl"] = "https://cdn.store-assets.com/s/632442/i/20123932.jpg?width=480&format=webp" #originalContentUrl
    return message

def get10(originalContentUrl=F"{end_point}/static/378.jp"):
    return getImageMessage10(originalContentUrl)

def getImageMessage10(originalContentUrl):
    message = dict()
    message["type"] = "image"
    message["originalContentUrl"] = "https://cdn.store-assets.com/s/632442/i/20280445.jpg?width=480&format=webp" #originalContentUrl
    message["previewImageUrl"] = "https://cdn.store-assets.com/s/632442/i/20280445.jpg?width=480&format=webp" #originalContentUrl
    return message


def replyMessage(payload):
    response = requests.post("https://api.line.me/v2/bot/message/reply",headers=HEADER,data=json.dumps(payload))
    return 'OK'


def pushMessage(payload):
    response = requests.post("https://api.line.me/v2/bot/message/push",headers=HEADER,data=json.dumps(payload))
    return 'OK'

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


# @app.route('/upload_file', methods=['POST'])
# def upload_file():
#     payload = dict()
#     if request.method == 'POST':
#         file = request.files['file']
#         print("json:", request.json)
#         form = request.form
#         age = form['age']
#         gender = ("男" if form['gender'] == "M" else "女") + "性"
#         if file:
#             filename = file.filename
#             img_path = os.path.join(UPLOAD_FOLDER, filename)
#             file.save(img_path)
#             print(img_path)
#             payload["to"] = my_line_id
#             payload["messages"] = [getImageMessage(F"{end_point}/{img_path}"),
#                 {
#                     "type": "text",
#                     "text": F"年紀：{age}\n性別：{gender}"
#                 }
#             ]
#             pushMessage(payload)
#     return 'OK'


@app.route('/line_login', methods=['GET'])
def line_login():
    if request.method == 'GET':
        code = request.args.get("code", None)
        state = request.args.get("state", None)

        if code and state:
            HEADERS = {'Content-Type': 'application/x-www-form-urlencoded'}
            url = "https://api.line.me/oauth2/v2.1/token"
            FormData = {"grant_type": 'authorization_code', "code": code, "redirect_uri": F"{end_point}/line_login", "client_id": line_login_id, "client_secret":line_login_secret}
            data = parse.urlencode(FormData)
            content = requests.post(url=url, headers=HEADERS, data=data).text
            content = json.loads(content)
            url = "https://api.line.me/v2/profile"
            HEADERS = {'Authorization': content["token_type"]+" "+content["access_token"]}
            content = requests.get(url=url, headers=HEADERS).text
            content = json.loads(content)
            name = content["displayName"]
            userID = content["userId"]
            pictureURL = content["pictureUrl"]
            statusMessage = content["statusMessage"]
            print(content)
            return render_template('profile.html', name=name, pictureURL=
                                   pictureURL, userID=userID, statusMessage=
                                   statusMessage)
        else:
            return render_template('login.html', client_id=line_login_id,
                                   end_point=end_point)


if __name__ == "__main__":
    app.debug = True
    app.run()
