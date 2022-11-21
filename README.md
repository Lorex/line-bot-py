# Lorex's Testing LINE Bot

This is a testing LINE bot using LINE Messaging API and Python 3 with Flask framework.

## Installation
Install Dependencies
```bash
$ pip3 install -r requirements.txt
```

Run the app
```bash
$ python3 main.py
```


## Configuration
You need to set the following variables at the head of main.py
```python:
# LINE Access Token and Secret
line_access_token = 'YOUR_LINE_CHANNEL_ACCESS_TOKEN'

line_secret = 'YOUR_LINE_CHANNEL_SECRET'

# If you turn this on, the bot will reload pattern file when it receives a message.
# For performance consideration, you should turn this off in production or when you have a lot of patterns.
hotReloadPattern = True
```

## Pattern File
The pattern file is a JSON file that contains the patterns and the responses. The pattern file is loaded when the app starts. If you turn on hotReloadPattern, the pattern file will be reloaded everytime when the app receives a message.

The pattern config is a JSON array, each element is a pattern object. The pattern object has the following properties:
```json:
{
    "mode": "regex | string",
    "pattern": "pattern string",
    "response": "response string",
}
```

You can also set the "response" property to a string array, the bot will randomly choose the response from array, here is the example:
```json:
{
    "mode": "regex | string",
    "pattern": "pattern string",
    "response": ["response A", "response B", "response C"],
}
```

Modes:
- `regex`: The pattern string will be treated as a regular expression. If the message matches the pattern, the response will be sent.
- `string`: The pattern string will be treated as a string. If the message contains the pattern, the response will be sent. Please notice that the pattern is case sensitive.