# RC UberEats BOGO Bot

## To Run

Create Bot in Zulip
Add the bot to Zulip: <https://zulip.com/help/add-a-bot-or-integration>

name: whatever
email: whatever
bot type: outgoing webhook
endpoint URL: $DOMAIN/webhooks, e.g. `<YOUR-DOMAIN-HERE>.ngrok-free.app/webhooks`

> interface: generic

## Install Flask and Run Bot Server

Flask installation instructions: <https://flask.palletsprojects.com/en/3.0.x/installation/#install-flask>

Save this file, go to the folder containing `main.py` and run the following:

```shell
pip install flask
flask --app main run --port 8000

```

## Set up ngrok

Use ngrok to serve your localhost server publically. Make an account and get a static URL [https://dashboard.ngrok.com/get-started/setup/macos](here)

Example (use your static URL instead):

```shell
brew install ngrok/ngrok/ngrok
ngrok config add-authtoken <TOKEN>
```

## Serve localhost

```shell
DOMAIN=<YOUR-DOMAIN-HERE>.ngrok-free.app
PORT=8000
ngrok http --domain=$DOMAIN $PORT

```

## DM the bot you created to test

You should be able to get responses to about or help or any message (with "hello world")
