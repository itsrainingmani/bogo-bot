import sys

import utils

from flask import Flask, request
from pprint import pprint
from supabase import Client, PostgrestAPIError

COMMANDS = """
Commands:
* `show deals`: to display available BOGO deals
* `status`: to show your subscription status
* `schedule`: to set your weekly pairing schedule
  * ex. `schedule mon tue thu`, `schedule mon fri`
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
        
        elif content == "all subs":
            all_data = utils.get_subscribed_users(supabase_client)
            for users in all_data.data:
                print(users['zulip_full_name'])
            return {"content": all_data.data}
        
        elif content == "today":
            daily = utils.get_todays_users(supabase_client)
            return {"content": daily.data}


        elif content == "status":
            user_data = utils.get_user(supabase_client, sender_id)
            msg = "You've never subscribed!" if not user_data.data else f"You are {"" if user_data.data[0]["is_subscribed"] else "not"} subscribed"
            return {"content": msg}
            
        elif content == "show deals":
            return {"content": utils.get_show_deals_message()}
        
        elif content == "subscribe":
            msg = utils.subscribe_user(supabase_client, sender_id, sender_full_name)
            return {"content": msg}

        elif content == "unsubscribe":
            msg = utils.unsubscribe_user(supabase_client, sender_id)
            return {"content": msg}
            
        elif content.startswith('schedule'):
            user_data = utils.update_user_schedule(supabase_client, sender_id, content)
            return {"content": f"Your weekly schedule has been updated with {user_data}"}
        
        else:
            return {"content": COMMANDS}

    except PostgrestAPIError as e:
        pprint(e)
        return {"content": ";-( Something went wrong 🥺 👉🏼👈🏼"}
