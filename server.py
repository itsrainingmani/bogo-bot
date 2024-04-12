import os
import sys

import utils
import message as zulip_message

from flask import Flask, request
from pprint import pprint
from supabase import Client, PostgrestAPIError
from dotenv import load_dotenv

load_dotenv()

COMMANDS = """
Commands:
* `show deals`: to display available BOGO deals
* `status`: to show your subscription status
* `schedule`: to set your weekly pairing schedule
  * ex. `schedule mon tue thu`, `schedule mon fri`
* `subscribe`: to start getting matched with other BOGOBot users for pair lunching
* `unsubscribe`: to stop getting matched
"""

SHOW_DEALS_FIRST = utils.get_show_deals_message() + """
    
*Would you like to be paired?*
* `sign me up boss` or `shaddup`
""" #dont remove the blank line in this...

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

    ##       DEV RESPONSES          ##
        elif content == "today":
            zulip_message.daily_message_blast()
            return {"content": 'testing...'} 
        
        elif content == "sign me up boss":
            pass

        elif content == "shaddup":
            return {"content": "Skipping pairing today"}

        elif content == "show deals first":
            return {"content": SHOW_DEALS_FIRST}
        

        elif content == "all subs":
            all_data = utils.get_subscribed_users(supabase_client)
            all_users = []
            if all_data.data:
                for users in all_data.data:
                    all_users.append(f" - {users['zulip_full_name']}")

            return {"content": '\n'.join(all_users) if all_users else 'No subscribed users yet!'}




        ##       PRODUCTION RESPONSES        ##

        elif content == "status":
            user_data = utils.get_user(supabase_client, sender_id)
            msg = ""
            if user_data.data:
                msg = f"You are {"" if user_data.data[0]["is_subscribed"] else "not"} subscribed"
            else:
                msg = "You've never subscribed!"
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

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8000))
    app.run(debug=True, host='0.0.0.0', port=port)
