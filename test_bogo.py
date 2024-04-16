import os
import pytest
import zulip
from src.db import BogoDB
from dotenv import load_dotenv

load_dotenv()


def test_zulip_client():
    client = zulip.Client(
        api_key=os.environ.get("ZULIP_API_KEY"),
        email=os.environ.get("ZULIP_EMAIL"),
        site=os.environ.get("ZULIP_SITE"),
    )

    assert client.client_name == "ZulipPython/0.9.0"


def test_supabase_connection():
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_KEY")
    db = BogoDB(url=url, key=key)
    test_user_id = 677939

    test_user_info = db.get_user(user_id=test_user_id)
    print(test_user_info.data[0])

    assert len(test_user_info.data) > 0
