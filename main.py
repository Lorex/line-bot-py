#########################
#                       #
#     Configuration     #
#                       #
#########################
# LINE Access Token and Secret
line_access_token = ''

line_secret = ''

# Turn this off if you don't want to hot reload the pattern file
hotReloadPattern = True

####################################
#                                  #
#     Lorex's Testing LINE Bot     #
#                                  #
####################################
# Import Dependencies
import json, re
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
    if item['mode'] == 'regex':
      if re.search(item['pattern'], message):
        return item['response']

    if item['mode'] == 'string':
      if item['pattern'] in message:
        return item['response']

  return 'I don\'t understand what you are saying.'

if __name__ == '__main__':
    app.run()