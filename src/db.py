import datetime
from itertools import combinations
from pprint import pprint

from supabase import Client, create_client


class BogoDB:
    supabase_client: Client

    def __init__(self, url, key) -> None:
        self.supabase_client: Client = create_client(url, key)

    def pair_users():
        # take users off daily pairing Q
        # put users onto pairing history
        # message two users in DM
        pass

    def check_match_on_queue(self) -> bool:
        # get all users in a queue
        users_in_queue = (
            self.supabase_client.table("daily_q")
            .select("*")
            .order("q_time", desc=False)
            .execute()
        ).data
        user_pairs = combinations([u[0] for u in enumerate(users_in_queue)], 2)

        for u1, u2 in user_pairs:

            # intersection of time for u1 and u2
            time_intersection = set(users_in_queue[u1]["time_pref"]) & set(
                users_in_queue[u2]["time_pref"]
            )

            # intersection of food for u1 and u2
            food_intersection = set(users_in_queue[u1]["food_pref"]) & set(
                users_in_queue[u2]["food_pref"]
            )

            pprint(
                f"{users_in_queue[u1]['zulip_user_id']} & {users_in_queue[u2]['zulip_user_id']} matched for time - {time_intersection} with food prefs - {food_intersection}"
            )
        return False

    def clear_daily_q(self):
        results = (
            self.supabase_client.table("daily_q")
            .select("*")
            # .delete()
            .eq("q_date", datetime.date.today())
            .execute()
        )
        print(results)

    def update_time_preference(self, user_id, times):
        self.queue_user(user_id)
        all_times = ["a", "b", "c", "d"]
        time_pref = (
            all_times
            if "all" in times
            else [time for time in times if time in all_times]
        )
        result = (
            self.supabase_client.table("daily_q")
            .update({"time_pref": time_pref})
            .eq("zulip_user_id", user_id)
            .execute()
        )
        return result.data[0]["time_pref"]

    def update_food_preference(self, user_id, prefs):
        self.queue_user(user_id)
        all_prefs = ["1", "2", "3", "4", "5"]
        food_pref = (
            all_prefs
            if "all" in prefs
            else [food for food in prefs if food in all_prefs]
        )
        result = (
            self.supabase_client.table("daily_q")
            .update({"food_pref": food_pref})
            .eq("zulip_user_id", user_id)
            .execute()
        )
        # self.check_match_on_queue(
        #     self, result.data[0]["time_pref"], result.data[0]["food_pref"]
        # )
        # NEED TO CHECK FOR HMATCH HERE. DONT MATCH YOSELF
        return result.data[0]["food_pref"]

    def queue_user(self, user_id):
        self.supabase_client.table("daily_q").upsert(
            {
                "zulip_user_id": user_id,
            }
        ).execute()

        # check if user_id in daily_q
        # if lunch int, update lunch int in daily_q
        # if food_pref, update food_pref in daily_q
        #  check_match_on_queue
        #       true: pair_users
        #       false: post on pairing queue, respond with waiting for others

    def get_todays_users(self):
        weekday = ["mon", "tue", "wed", "thu", "fri"]
        today = datetime.date.today().weekday()  # m = 0, f = 4
        daily_users = (
            self.supabase_client.table("users")
            .select("*")
            .eq("is_subscribed", True)
            .or_(f'schedule.is.null, schedule.cs.{{"{weekday[today]}"}}')
            .execute()
        )
        return [user["zulip_user_id"] for user in daily_users.data]

    #
    #   GET USER INFO FOR SUBSCRIBE/UNSUBSCRIBE/SCHEDULE
    #

    def update_user_schedule(self, user_id, schedule):
        valid_days = set(["mon", "tue", "wed", "thu", "fri"])
        parsed_schedule = [day for day in schedule.split() if day in valid_days]
        parsed_schedule = None if not parsed_schedule else parsed_schedule
        user_data = (
            self.supabase_client.table("users")
            .update({"schedule": parsed_schedule, "is_subscribed": True})
            .eq("zulip_user_id", user_id)
            .execute()
        )
        return (
            "all days of the week" if not parsed_schedule else " ".join(parsed_schedule)
        )

    def get_subscribed_users(self):
        user_data = (
            self.supabase_client.table("users")
            .select("*")
            .eq("is_subscribed", True)
            .execute()
        )
        return user_data

    def get_user(self, user_id):
        user_data = (
            self.supabase_client.table("users")
            .select("*")
            .eq("zulip_user_id", user_id)
            .execute()
        )
        return user_data

    def subscribe_user(self, user_id, user_full_name):
        user_data = self.get_user(user_id)
        if not user_data.data or not user_data.data[0]["is_subscribed"]:
            user_data = (
                self.supabase_client.table("users")
                .upsert(
                    {
                        "zulip_user_id": user_id,
                        "zulip_full_name": user_full_name,
                        "is_subscribed": True,
                    }
                )
                .execute()
            )
            return "You've been subscribed!"
        return "You've already subscribed, silly!"

    def unsubscribe_user(self, user_id):
        user_data = self.get_user(user_id)
        if user_data.data:
            user_data = (
                self.supabase_client.table("users")
                .update({"is_subscribed": False})
                .eq("zulip_user_id", user_id)
                .execute()
            )
            return "You've been unsubscribed! BUT WHY?"
        return "You've never been subscribed!"
