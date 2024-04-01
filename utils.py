import json
import os
from pprint import pprint
import sys
from typing import Any

import requests
from supabase import create_client

UBER_URL = "https://recurse-eats.dim.codes/scraped.json"


def init_supabase_client():
    from dotenv import load_dotenv

    load_dotenv()

    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_KEY")

    if not url or not key:
        raise EnvironmentError("Supabase URL or Key not found")
    return create_client(url, key)


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
    # deals = {"restaurant": "some name", "first_deal": "", "total_deals": 5}
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
    # deal_name = res["deals"][0]["title"]
    # formatted_price = f"${res['deals'][0]['price']/200:.2f}"
    # total_deals = f" | {len(res["deals"])} deals" if len(res["deals"]) > 1 else ""
    deals = "\n".join([render_deal(deal) for deal in res["deals"]])
    return f" - {link} ({distance_km:.0f} m away)\n{deals}"
    # return f" - {link}{total_deals} | {deal_name} | {formatted_price}"


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
