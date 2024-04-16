#!/bin/sh
cd /app
python src/message.py
# python -c "from tests.test_zulip_comms import test_send; test_send()"
echo "$(date) cron ran" > cron.log
