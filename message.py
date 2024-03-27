from pprint import pprint
import sys
from supabase import Client
import zulip
import utils

try:
    supabase_client: Client = utils.init_supabase_client()
    client = zulip.Client(config_file="zuliprc")
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
            "content": "heheee 👉🏼👈🏼",
        }
    )
    pprint(result)
