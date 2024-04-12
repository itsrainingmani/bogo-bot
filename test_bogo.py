import os
import pytest
import zulip
from utils import init_supabase_client, get_user
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
    supabase = init_supabase_client()
    test_user_id = 677939

    test_user_info = get_user(supabase_client=supabase, user_id=test_user_id)

    assert len(test_user_info.data) > 0
