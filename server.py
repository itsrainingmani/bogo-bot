import sys
import zulip
import os
import requests
import json

import utils

from flask import Flask, request
from pprint import pprint
from dotenv import load_dotenv
from supabase import create_client, Client, PostgrestAPIError

load_dotenv()

url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")
UBER_URL = "https://recurse-eats.dim.codes/scraped.json"

if not url or not key:
    pprint("Supabase Env Variables not present")
    sys.exit(1)
supabase_client: Client = create_client(url, key)

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
                return {"content": f"You are {"" if user_data.data[0]["is_subscribed"] else "not"} subscribed"}
            else:
                return {"content": "You've never subscribed!"}
        elif content == "show deals":
            data = requests.get(UBER_URL).text
            deals_json = json.loads(data)

            processed_deals = utils.get_deals(deals_json)
            pprint(processed_deals)
            return {"content": utils.render_deals(deals_json=processed_deals)}
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
            return {
                "content": """
Commands:
* `show deals`: to display available BOGO deals
* `status`: to show your subscription status
* `subscribe`: to start getting matched with other BOGOBot users for pair lunching
* `unsubscribe`: to stop getting matched
"""
            }

    except PostgrestAPIError as e:
        pprint(e)
        return {"content": ";-( Something went wrong 🥺 👉🏼👈🏼"}
