import os
import sys
import random
import time
import datetime

from supabase import Client, create_client

try:
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_KEY")
except EnvironmentError as e:
    print(e)
    sys.exit(1)

supabase_client: Client = create_client(url, key)


def get_todays_users(supabase_client):
    weekday = ["mon", "tue", "wed", "thu", "fri"]
    today = datetime.date.today().weekday()  # m = 0, f = 4
    daily_users = (
        supabase_client.table("users")
        .select("*")
        .eq("is_subscribed", True)
        .or_(f'schedule.is.null, schedule.cs.{{"{weekday[today]}"}}')
        .execute()
    )
    return [user["zulip_user_id"] for user in daily_users.data]


def create_daily_q_entries(supabase_client, num_entries):
    times = [ch for ch in "abcd"]
    foods = [ch for ch in "12345"]
    todays_users = get_todays_users(supabase_client)
    user_data = [
        {
            "zulip_user_id": user,
            "time_pref": random.sample(times, random.randint(1, 4)),
            "food_pref": random.sample(foods, random.randint(1, 5)),
        }
        for user in todays_users
    ]

    for i in range(num_entries):
        supabase_client.table("daily_q").upsert(user_data[i]).execute()
        time.sleep(random.randint(1, 10))


create_daily_q_entries(supabase_client, 4)
