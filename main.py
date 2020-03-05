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
import os

from cotoha import trans

import pymysql
pymysql.install_as_MySQLdb()

app = Flask(__name__)

# 環境変数
YOUR_CHANNEL_ACCESS_TOKEN = os.environ["YOUR_CHANNEL_ACCESS_TOKEN"]
YOUR_CHANNEL_SECRET = os.environ["YOUR_CHANNEL_SECRET"]

REMOTE_HOST = CONF_DATA['REMOTE_HOST']
REMOTE_DB_NAME = CONF_DATA['REMOTE_DB_NAME']
REMOTE_DB_USER = CONF_DATA['REMOTE_DB_USER']
REMOTE_DB_PASS = CONF_DATA['REMOTE_DB_PASS']
REMOTE_DB_TB = CONF_DATA['REMOTE_DB_TB']



line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)


@app.route("/callback", methods=['POST'])
def callback():
    """
    webhookからのrequestをチェック

    """

    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    """
    messageを受け取ったときの処理

    """

    if event.reply_token == "00000000000000000000000000000000":
        return

    # 受け取ったテキストを返す
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=trans(event.message.text)))


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
