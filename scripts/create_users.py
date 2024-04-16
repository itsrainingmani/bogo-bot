import os
import sys
import random

from supabase import Client, create_client
from faker import Faker

try:
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_KEY")
except EnvironmentError as e:
    print(e)
    sys.exit(1)

supabase_client: Client = create_client(url, key)


def create_users(supabase_client, num_users, schedule=False):
    name_factory = Faker()
    days = ["mon", "tue", "wed", "thu", "fri"]
    user_data = [
        {
            "zulip_user_id": random.randint(100, 10000),
            "zulip_full_name": name_factory.name(),
            "is_subscribed": True,
            "schedule": (
                None if not schedule else random.sample(days, random.randint(1, 4))
            ),
        }
        for _ in range(num_users)
    ]
    results = supabase_client.table("users").upsert(user_data).execute()
    print(results)


create_users(supabase_client, 5, schedule=True)
