import os
from pprint import pprint
import sys
from supabase import Client
import zulip
import utils
from dotenv import load_dotenv

load_dotenv()

try:
    supabase_client: Client = utils.init_supabase_client()
    client = zulip.Client(
        api_key=os.environ.get("ZULIP_API_KEY"),
        email=os.environ.get("ZULIP_EMAIL"),
        site=os.environ.get("ZULIP_SITE"),
        # config_file="zuliprc"
    )
except (EnvironmentError, zulip.ConfigNotFoundError) as e:
    pprint(e)
    sys.exit(1)

# user_ids = [677939, 690946, 677960]
subscribed_users = utils.get_subscribed_users(supabase_client)

for user in subscribed_users.data:
    result = client.send_message(
        message_data={
            "type": "private",
            "to": [user["zulip_user_id"]],
            "content": utils.get_show_deals_message(),
        }
    )
    pprint(result)
