from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,StickerSendMessage
)

app = Flask(__name__)

line_bot_api = LineBotApi('C1+5ZnxbL5JzSPsKXBPDlu5eWrcTa2S7u73KsikLuexmk/AcyihO0ClnbeH9NKy9zkX7oN9hZO7Mc8cHc7+aEL126lqg8NsgeTahugyYL/thzkWWFUWWJ8f4LFfpnE7lLG3+2lE4M5ow6O2aW8zdzwdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('a5cbefd1b6b4d35c7b248b0a14c94180')


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
    msg = event.message.text
    r = '很抱歉您說什麼'

    if '給我貼圖' in msg:
        sticker_message = StickerSendMessage(
            package_id='2',
            sticker_id='23'
        )

        line_bot_api.reply_message(
            event.reply_token,
            sticker_message)

        return

    if msg in ['hi','Hi']:
        r = '嗨'
    elif msg == '你吃飯了嗎':
        r = '還沒'
    elif msg == '你是誰':
        r = '我是機器人'
    elif '訂位' in msg:
        r = '您想訂位，是嗎?'

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=r))


if __name__ == "__main__":
    app.run()