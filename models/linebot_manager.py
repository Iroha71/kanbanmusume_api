import os
from linebot import LineBotApi
from linebot.models import TextSendMessage
from linebot.exceptions import LineBotApiError
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(dotenv_path)

LINE_ID: str = os.environ.get("LINE_ID")
CHANNEL_TOKEN: str = os.environ.get("LINE_CHANNEL_TOKEN")
linebot_api = LineBotApi(CHANNEL_TOKEN)
def push_msg(taskname: str=None):
  try:
    linebot_api.push_message(LINE_ID, TextSendMessage(text="テスト"))
  except LineBotApiError as e:
    print("失敗")
    print(e)

if __name__ == "__main__":
  push_msg()