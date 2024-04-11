import json
import os
import datetime
from pprint import pprint
import sys
from typing import Any

import requests
from supabase import create_client

UBER_URL = "https://recurse-eats.dim.codes/scraped.json"


def init_supabase_client():
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_KEY")

    if not url or not key:
        raise EnvironmentError("Supabase URL or Key not found")
    return create_client(url, key)


#
#   DAILY PAIRING
#


def pair_users():
    # take users off daily pairing Q
    # put users onto pairing history
    # message two users in DM
    pass


def check_match_on_queue(supabase_client, lunch_interval, food_pref):
    # for user on queue, if overlapping lunch_int & overlapping food_pref
    #   return matching user
    # else
    #   return
    pass


def queue_user(supabase_client, user_id, lunch_interval, food_pref):
    # check for matching users on daily pairing Q
    #   if match, then pair
    # else
    #   post user onto daily pairing Q
    pass


def get_todays_users(supabase_client):
    weekday = datetime.date.today().weekday()  # m = 0, f = 4
    # find all users that are subscribed and have no schedule or scheduled for todays day
    # return list
    pass


#
#   GET USER INFO FOR SUBSCRIBE/UNSUBSCRIBE
#


def update_user_schedule(supabase_client, user_id, schedule):
    valid_days = set(["mon", "tue", "wed", "thu", "fri"])
    parsed_schedule = [
        day.lower() for day in schedule[8:].strip().split() if day.lower() in valid_days
    ]
    user_data = (
        supabase_client.table("users")
        .update({"schedule": " ".join(parsed_schedule)})
        .eq("zulip_user_id", user_id)
        .execute()
    )
    return " ".join(parsed_schedule)


def get_user(supabase_client, user_id):
    user_data = (
        supabase_client.table("users")
        .select("*")
        .eq("zulip_user_id", user_id)
        .execute()
    )
    return user_data


def get_subscribed_users(supabase_client):
    user_data = (
        supabase_client.table("users").select("*").eq("is_subscribed", True).execute()
    )

    return user_data


#
#   RENDERING DEALS TO USERS
#


def get_deal_info(deal_json: list[dict[str, Any]]):
    return [
        {
            "title": deal["title"],
            "description": deal["itemDescription"],
            "price": deal["price"],
            "isSoldOut": deal["isSoldOut"],
            "isAvailable": deal["isAvailable"],
        }
        for deal in deal_json
    ]


def get_deals(uber_json):
    deals = [
        {
            "ubereats_link": res["@id"],
            "name": res["name"],
            "cuisine": res["servesCuisine"],
            "geo": res["geo"],
            "telephone": res["telephone"],
            "rating": (
                res["aggregateRating"]["ratingValue"] if res["aggregateRating"] else -1
            ),
            "deals": get_deal_info(res["deals"]),
        }
        for res in uber_json
    ]
    return deals


def render_deals(deals_json):
    return "Here are today's BOGO deals! Prices are per person.\n" + "\n".join(
        [render_restaurant_info(res) for res in deals_json]
    )


def render_restaurant_info(res):
    link = render_link(res["name"], res["ubereats_link"])
    distance_km = calc_distance(res["geo"])
    deals = "\n".join([render_deal(deal) for deal in res["deals"]])
    return f" - {link} ({distance_km:.0f} m away)\n{deals}"


def render_deal(deal):
    deal_name = deal["title"]
    formatted_price = f"${deal['price']/200:.2f}"
    return f"  - {deal_name} | {formatted_price}"


def render_link(text, link):
    return f"[{text}]({link}?diningMode=PICKUP)"


def get_show_deals_message():
    data = requests.get(UBER_URL).text
    deals_json = json.loads(data)

    processed_deals = get_deals(deals_json)
    pprint(processed_deals)
    return render_deals(deals_json=processed_deals)


def calc_distance(res_geo):
    from math import radians, sin, cos, sqrt, atan2

    rc_coord = (40.69136, -73.9852)
    lat1, lon1, lat2, lon2 = map(
        radians, [rc_coord[0], rc_coord[1], res_geo["latitude"], res_geo["longitude"]]
    )
    dlon, dlat = lon2 - lon1, lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance_m = 6371 * c * 1000
    return distance_m
