from typing import Any


def get_user(supabase_client, user_id):
    user_data = (
        supabase_client.table("users")
        .select("*")
        .eq("zulip_user_id", user_id)
        .execute()
    )

    return user_data


def get_deal_info(deal_json: list[dict[str, Any]]):
    return [
        {
            "title": deal["title"],
            "description": deal["itemDescription"],
            "price": deal["priceTagline"]["text"],
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
    return "\n".join(
        [
            f" - [{res['name']}]({res['ubereats_link']}) | {res['deals'][0]['title']}"
            for res in deals_json
        ]
    )
