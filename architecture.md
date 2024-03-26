# General Thoughts

- Show BOGO deals of the day (Default to show the first deal)
- Are you interested? - Y/N
- Show specific Food options
- Lunch interval pref

## Commands

- `help`
- `subscribe`
- `show deals`
- `unsubscribe`

## BOGO Deal Selection

Represent each bogo restaurant deal under a numbered list. User responds with all the places that they are interested in

## Lunch Intervals

Represent lunch as a list of 1 hour time chunks. User can respond with which number (corresponding to an interval)

a. 11:00a - 12:00p
b. 12:00p - 1:00p
c. 1:00p - 2:00p
d. 2:00p - 3:00p

## DB

User table - user_id, user_fullname, is_subscribed, schedule

Daily Pairing Q
user_id, lunch_interval, datetime, food_pref
