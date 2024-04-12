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


def message_all_subscribers_ind():
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


def message_group():
    todays_users = utils.get_todays_users(supabase_client)
    user_ids = []
    for user in todays_users.data:
        user_ids.append(user["zulip_user_id"])

    result = client.send_message(
        message_data={
            "type": "private",
            "to": [user_ids],
            "content": "Hello this is a group message test!",
        }
    )
    pprint(result)
