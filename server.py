import os
import sys

import utils

from flask import Flask, request
from pprint import pprint
from supabase import Client, PostgrestAPIError
from dotenv import load_dotenv

load_dotenv()

COMMANDS = """
Commands:
* `show deals`: to display available BOGO deals
* `status`: to show your subscription status
* `subscribe`: to start getting matched with other BOGOBot users for pair lunching
* `unsubscribe`: to stop getting matched
"""

try:
    supabase_client: Client = utils.init_supabase_client()
except EnvironmentError as e:
    print(e)
    sys.exit(1)

app = Flask(__name__)


@app.route("/")
def hello_world():
    pprint(request)
    return "<p>RC UberEats BOGO Pairing Bot!</p>"


@app.route("/webhooks", methods=["GET", "POST"])
def handle():
    response = request.get_json()
    pprint(response)
    message = response["message"]
    sender_full_name = message["sender_full_name"]
    sender_id = message["sender_id"]
    content = message["content"].lower().strip()

    try:
        if content == "about":
            return {"content": "Hello! This is BOGO bot! Please type 'help' for help!"}
        elif content == "status":
            user_data = utils.get_user(supabase_client, sender_id)
            if len(user_data.data) > 0:
                return {
                    "content": f"You are {"" if user_data.data[0]["is_subscribed"] else "not"} subscribed"
                }
            else:
                return {"content": "You've never subscribed!"}
        elif content == "show deals":
            return {"content": utils.get_show_deals_message()}
        elif content == "subscribe":
            user_data = utils.get_user(supabase_client, sender_id)
            if len(user_data.data) == 0 or not user_data.data[0]["is_subscribed"]:
                user_data = (
                    supabase_client.table("users")
                    .upsert(
                        {
                            "zulip_user_id": sender_id,
                            "zulip_full_name": sender_full_name,
                            "is_subscribed": True,
                        }
                    )
                    .execute()
                )
                return {"content": "You've been subscribed!"}

            else:
                return {"content": "You've already subscribed, silly!"}

        elif content == "unsubscribe":
            user_data = utils.get_user(supabase_client, sender_id)

            if len(user_data.data) > 0:
                # update the user flag
                user_data = (
                    supabase_client.table("users")
                    .update({"is_subscribed": False})
                    .eq("zulip_user_id", sender_id)
                    .execute()
                )
                return {"content": "You've been unsubscribed! BUT WHY?"}

            else:
                return {"content": "You've never subscribed!"}
        else:
            return {"content": COMMANDS}

    except PostgrestAPIError as e:
        pprint(e)
        return {"content": ";-( Something went wrong 🥺 👉🏼👈🏼"}

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8000))
    app.run(debug=True, host='0.0.0.0', port=port)
