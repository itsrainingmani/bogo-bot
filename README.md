# RC UberEats BOGO Bot

There are many UberEats Buy One Get One deals available around 397 Bridge St. This is a Zulip bot that will pair lunchers so people can take advantage of the BOGO Deals.

This project is directly inspired by the experience of Recursers at the Brooklyn Hub & by the [RC Eats](https://recurse-eats.dim.codes/) project created by [Angelo Lloti (W2'24)](https://github.com/XdimGG)

## Create Zulip Bot

Add a bot to Zulip by following the instructions here - <https://zulip.com/help/add-a-bot-or-integration#add-a-bot-or-integration_1>

Please make sure that the type of your bot is `Outgoing Webhook` since the bot will be receiving new messages via HTTP POST requests from Zulip.

```text
name: whatever
email: whatever
bot type: outgoing webhook
endpoint URL: $DOMAIN/webhooks, e.g. `<YOUR-DOMAIN-HERE>.ngrok-free.app/webhooks`

> interface: generic
```

## Install Python Requirements

⚠️ This project uses python 3.12.0. Other python versions are not guaranteed to work.

Install the necessary requirements with -

```shell
pip install -r requirements.txt
```

## Set up ngrok

We are using ngrok to serve our localhost server publically. You can use any option (eg. [Tailscale Funnel](https://tailscale.com/kb/1223/funnel), [localtunnel](https://github.com/localtunnel/localtunnel)) that allows you to serve localhost to a static publicly available URL.

Make an account and get a static URL [here](https://dashboard.ngrok.com/get-started/setup/macos)

Example (use your static URL instead):

```shell
brew install ngrok/ngrok/ngrok
ngrok config add-authtoken <TOKEN>
```

## Serve Local Web Server

```shell
DOMAIN=<YOUR-DOMAIN-HERE>.ngrok-free.app
PORT=8000
ngrok http --domain=$DOMAIN $PORT
```

## Run Flask Server

```shell
flask --app server run --port 8000
```

If you'd like to hot-reload your server on code changes, add the `--debug` flag to the above command.

## DM the bot you created to test

The currently supported commands are -

```markdown
- `show deals`: to display available BOGO deals
- `status`: to show your subscription status
- `subscribe`: to start getting matched with other BOGOBot users for pair lunching
- `unsubscribe`: to stop getting matched
```

## TO DO

- user functionality

  - [x] user scheduling preferences

- pairing functionality

  - [ ] update command list for when users are in the process of getting paired?
  - [ ] determine what pref info to get from users
    - deals are going up and down very frequently, should we present food/deal pref option with the risk it goes down, or do we keep it so people getting paired have an idea of what the other person wants to eat?
    - i was having a hard time getting the bot to list the deals in a numbered list (stef)
    - are users on the queue when they respond y to the bot or after they respond with their time/pref info
    - can they get put on the queue at other times during the day or is this lunch only? if we have dinner too, can people be matched for multiple meals a day?
    - can people have a command to see who is currently on the queue with time/food pref?
    - will 15-30 min messages be sent out to people who haven't matched/skipped about who's on the queue?
  - [x] structure daily database/queue (architecture.md)
  - [ ] pairing logic - timing, pref, etc
  - [ ] followup for weekly stats

- unit testing

  - [x] check zulip rc client connection
  - [x] check supabase connection
  - [ ] load in testing db
  - [ ] load in deals json

- integration testing
