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

                if text == "我的名字":
                    payload["messages"] = [getNameEmojiMessage()]
                elif text == "出去玩囉":
                    payload["messages"] = [getPlayStickerMessage()]
                elif text == "台北101":
                    payload["messages"] = [getTaipei101ImageMessage(),
                                           getTaipei101LocationMessage(),
                                           getMRTVideoMessage()]
                elif text == "養一隻貓吧":
                    payload["messages"] = [getTaipei101ImageMessage()]
                elif text == "簡介":
#                     payload["messages"] = 
                    reply_text = "Hello"
                elif text == "quoda":
                    payload["messages"] = [
                            {
                                "type": "text",
                                "text": getTotalSentMessageCount()
                            }
                        ]
                elif text == "今日確診人數":
                    payload["messages"] = [
                            {
                                "type": "text",
                                "text": getTodayCovid19Message()
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
                                  "text": "我們的功能",
                                  "actions": [
                                      {
                                        "type": "message",
                                        "label": "簡介",
                                        "text": "簡介"
                                      },
#                                       {
#                                         "type": "message",
#                                         "label": "品種",
#                                         "text": "1.Criollo－產量約是總可可豆產量的3%，主要是分佈在南美洲的委內瑞拉。由於Criollo很怕蟲害，因此在栽種上相當不容易。但是不會過於酸、苦的風味，還帶有獨特的細緻香氣，是最頂級的可可豆品種。"
#                                           "2.Forastero－是市面上最常見，生產也最大量的可可豆品種，佔總可可豆產量80%以上。主要分布在西非及東南亞。無論是在澀味、苦味及酸味上都相較濃厚，巧克力味也較淡，但因為產量多的關係，因此常使用於平價巧克力。"
#                                           "3.Trintario－集合了上述口味及產量的優點。由Criollo、Forastero所混種的Trintario，原產地在加勒比海的千里達群島，口味比較濃郁厚實，帶一點果香味。由Criollo品種混搭Forastero的Trintario，在產量上也較容易栽培。"
#                                       },
                                      {
                                        "type": "uri",
                                        "label": "聯絡我",
                                        "uri": f"tel:{my_phone}"
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


def getNameEmojiMessage():
    lookUpStr = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    productId = "5ac21a8c040ab15980c9b43f"
    name = "Jason"
    message = dict()
    message["type"] = "text"
    message["text"] = "".join("$" for r in range(len(name)))
    emojis_list = list()
    for i, nChar in enumerate(name):
        emojis_list.append(
            {
              "index": i,
              "productId": productId,
              "emojiId": f"{lookUpStr.index(nChar) + 1 :03}"
            }
        )
    message["emojis"] = emojis_list
    return message


def getCarouselMessage(data):
    message = dict()
    return message


def getLocationConfirmMessage(title, latitude, longitude):
    message = dict()
    return message


def getCallCarMessage(data):
    message = dict()
    return message

# def getdata():
#     message = TextSendMessage(text='可可樹每個果實中大約可得到20-25粒可可豆，外層是白色微甜帶酸的果肉。可可豆可經加工處理，成為可可餅、可可粉、可可脂等重要食物原料。可可豆曾被作為貨幣使用，比如瑪雅人和阿茲特克人')
#     line_bot_api.reply_message(event.reply_token, message)


def getPlayStickerMessage():
    message = dict()
    message["type"] = "sticker"
    message["packageId"] = "446"
    message["stickerId"] = "1988"
    return message


def getTaipei101LocationMessage():
    message = dict()
    return message


def getMRTVideoMessage():
    message = dict()
    return message


def getMRTSoundMessage():
    message = dict()
    message["type"] = "audio"
    message["originalContentUrl"] = F"{end_point}/static/mrt_sound.m4a"
    import audioread
    with audioread.audio_open('static/mrt_sound.m4a') as f:
        # totalsec contains the length in float
        totalsec = f.duration
    message["duration"] = totalsec * 1000
    return message


def getTaipei101ImageMessage(originalContentUrl=F"{end_point}/static/112.jpg"):
    return getImageMessage(originalContentUrl)


def getImageMessage(originalContentUrl):
    message = dict()
    message["type"] = "image"
    message["originalContentUrl"] = originalContentUrl
    message["previewImageUrl"] = originalContentUrl
    return message


def replyMessage(payload):
    response = requests.post("https://api.line.me/v2/bot/message/reply",headers=HEADER,data=json.dumps(payload))
    return 'OK'


def pushMessage(payload):
    response = requests.post("https://api.line.me/v2/bot/message/push",headers=HEADER,data=json.dumps(payload))
    return 'OK'


def getTotalSentMessageCount():
    response = requests.get("https://api.line.me/v2/bot/message/quota/consumption",headers=HEADER)
    return response.json()["totalUsage"]


def getTodayCovid19Message():
    response = requests.get("https://covid-19.nchc.org.tw/api/covid19?CK=covid-19@nchc.org.tw&querydata=4001&limited=TWN")
    date = response.json()[0]["a04"]
    total_count = response.json()[0]["a05"]
    count = response.json()[0]["a06"]
    return F"日期：{date}, 人數：{count}, 確診總人數：{total_count}"


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/upload_file', methods=['POST'])
def upload_file():
    payload = dict()
    if request.method == 'POST':
        file = request.files['file']
        print("json:", request.json)
        form = request.form
        age = form['age']
        gender = ("男" if form['gender'] == "M" else "女") + "性"
        if file:
            filename = file.filename
            img_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(img_path)
            print(img_path)
            payload["to"] = my_line_id
            payload["messages"] = [getImageMessage(F"{end_point}/{img_path}"),
                {
                    "type": "text",
                    "text": F"年紀：{age}\n性別：{gender}"
                }
            ]
            pushMessage(payload)
    return 'OK'


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
