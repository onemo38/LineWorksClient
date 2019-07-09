import os
import LineWorksClient as LWC
from dotenv import load_dotenv

load_dotenv()

conf = {
    "api_id": os.environ.get("API_ID"),
    "server_id": os.environ.get("SERVER_ID"),
    "private_key": os.environ.get("PRIVATE_KEY"),
    "consumer_key": os.environ.get("CONSUMER_KEY"),
    "bot_no": os.environ.get("BOT_NO"),
    "exp_min": 20
}

lwc = LWC.LineWorksClient(**conf)
svtoken = lwc.get_server_token()

#send text message
to_room_id = "xxxxxxx"
res = lwc.send_text_message(to_room_id, "Hello!")
print(res)