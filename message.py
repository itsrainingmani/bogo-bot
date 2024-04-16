import os
from pprint import pprint
import sys
from supabase import Client
import zulip
import utils
from dotenv import load_dotenv

load_dotenv()


PAIRING_COMMANDS = """
Hey! This is BOGO bot! If you want to get paired for BOGO deals today, please respond!
- `sign me up boss`: yes :money_face:
- `shaddup`: skip today :pleading_face:
- `show deals first`: see current deals before deciding, but these change *frequently* throughout the day!
"""


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

###     PRODUCTION MESSAGES     ###


###     TEST MESSAGES       ###


def daily_message_blast():
    daily_user_ids = utils.get_todays_users(supabase_client)
    print(f"actual daily user_ids in daily message blast {daily_user_ids}")
    # daily_user_ids = [677939, 674511]   #mani & stef
    daily_user_ids = [674511]  # stef

    message_individuals(daily_user_ids, PAIRING_COMMANDS)


def message_individuals(user_ids, contents):
    for user in user_ids:
        result = client.send_message(
            message_data={
                "type": "private",
                "to": [user],
                "content": contents,
            }
        )
        # pprint(result)


def message_group(user_ids, contents):
    result = client.send_message(
        message_data={
            "type": "private",
            "to": user_ids,
            "content": contents,
        }
    )
    # pprint(result)
