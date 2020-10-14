from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('BOAa1Vsj+tSBhPc2IsnweMgQE52juXSCnLYRsYzsxHsxkznGZtFV6fy5vXe98NF03P5NlSNrQSvHL9dXSMH7wF9s26kIwPzp4JY7c/yt0mdA9on5hjXDwVtN5B4gHkcMplpfbMUIx3mm5Uok3ibf9wdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('247ad8a1c806de161dc12a4210e07ea5')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()