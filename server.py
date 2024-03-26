import zulip
from flask import Flask, request
import json
from pprint import pprint

client = zulip.Client(config_file="zuliprc", client=f"RC UberEats BOGO Pairing Bot")

app = Flask(__name__)


@app.route("/")
def hello_world():
    pprint(request)
    return "<p>RC UberEats BOGO Pairing Bot!</p>"


@app.route("/webhooks", methods=["GET", "POST"])
def handle():
    response = request.get_json()
    pprint(response)
    sender = response["message"]["sender_full_name"]
    content = response["message"]["content"]

    if content == "about":
        return {"content": "Hello! This is BOGO bot! Please type 'help' for help!"}
    elif content == "help":
        return {
            "content": """
Commands:
  - help: show help
  - get url: get BOGO url
  - signup: sign up for this thing
"""
        }

    return {"content": f"hello, {sender}"}
