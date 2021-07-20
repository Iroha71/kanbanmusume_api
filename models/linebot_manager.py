from os import path, environ
from linebot import LineBotApi
from linebot.models import TextSendMessage
from linebot.exceptions import LineBotApiError
from dotenv import load_dotenv
from pathlib import Path

dotenv_path = Path(__file__).parent
dotenv_path /= '../'
dotenv_path = path.join(dotenv_path.resolve(), '.env')
load_dotenv(dotenv_path)
LINE_ID: str = environ.get("LINE_ID")
CHANNEL_TOKEN: str = environ.get("LINE_CHANNEL_TOKEN")
linebot_api = LineBotApi(CHANNEL_TOKEN)

def push_msg(taskname: str=None):
  try:
    linebot_api.push_message(LINE_ID, TextSendMessage(text="テスト"))
  except LineBotApiError as e:
    print("失敗")
    print(e)

if __name__ == "__main__":
  push_msg()