#########################
#                       #
#     Configuration     #
#                       #
#########################
# LINE Access Token and Secret
line_access_token = 'oclPJrW8n+hqEQt5Jc9W+XOI3IZY/isIeVEAwWnhgNDvMRgkfuvRs1OLtdk9qA8GT6JAFMnV15R/rTskSqz+OzLbti6U3MqJif8zTnI6qi50bBrRnhkpFcS5O2bCpGzBA66/fBrG0dwCHuwM5DC/uQdB04t89/1O/w1cDnyilFU='

line_secret = '2f8e7100759b59a7fcfb96b2cd09afd1'

# Turn this off if you don't want to hot reload the pattern file
hotReloadPattern = True

####################################
#                                  #
#     Lorex's Testing LINE Bot     #
#                                  #
####################################
# Import Dependencies
import json, re, random
from flask import Flask, request
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

app = Flask(__name__)
inputFile = open('pattern.json', 'r')
matchList = json.load(inputFile)

@app.route('/')
def hello_world():
    return {'message': 'Line bot server up!'}

# Receive message from Line Webhook
@app.route('/', methods=['POST'])
def linebot():
  body = request.get_data(as_text=True)
  try:
    # Authenticate
    json_data = json.loads(body)
    line_bot_api = LineBotApi(line_access_token)
    handler = WebhookHandler(line_secret)
    signature = request.headers['X-Line-Signature']
    handler.handle(body, signature)

    # Get message
    getToken = json_data['events'][0]['replyToken']
    getMsgType = json_data['events'][0]['message']['type']
    if getMsgType == 'text':
      getMsg = json_data['events'][0]['message']['text']
      replyMsg = messageHandler(getMsg)
    else:
      replyMsg = 'WTF are you talking about?'

    # Reply message
    line_bot_api.reply_message(getToken, TextSendMessage(text=replyMsg))
  except:
    print(body)
  return 'OK'

def messageHandler(message):
  # Hot reload pattern.json
  if hotReloadPattern:
    inputFile = open('pattern.json', 'r')
    matchList = json.load(inputFile)

  # Iterate through matchRegexList and matchStringList
  for item in matchList:
    # Check if response is a string or a array
    if item['mode'] == 'regex':
      if re.search(item['pattern'], message):
        return responseHandler(item['response'])

    if item['mode'] == 'string':
      if item['pattern'] in message:
        return responseHandler(item['response'])

  return responseHandler('I don\'t understand what you are saying.')


def responseHandler(response):
  # Check if response is a string or a array
    if isinstance(response, str):
      # Response a string message
      return response
    else:
      # Response a random string message from array
      return response[random.randint(0, len(response) - 1)]

if __name__ == '__main__':
    app.run()