#!/usr/bin/python3

import telepot as tb
import telepot.aio.loop
import telepot.loop

from sql_helper import *

BOT = tb.Bot("BOT_TOKEN")
CHAT_ID = "CHAT_ID"

BOT = tb.Bot("5922809115:AAHs1god0Lw9l6sd9l-6Gqi2YjzVR8X2Gf8")
CHAT_ID = 326247323


def read_message_from_user(msg):
    user_text = msg["text"]
    user_id = msg["from"]["id"]

    handle_message(user_text, user_id)


def handle_message(user_text, user_id):
    if user_text == "?":
        text = read_route_data(user_id)
    else:
        text = write_route_data(user_text, user_id)

    send_message(text)


def read_route_data(user_id):
    data = read_route_data_from_db(user_id)

    return data


def write_route_data(user_text, user_id):
    user = read_route_data_from_db(user_id)
    data = write_route_data()

    return data

def send_message(text):
    BOT.sendMessage(CHAT_ID, text)


def main():
    telepot.loop.MessageLoop(BOT, read_message_from_user).run_forever()


if __name__ == "__main__":
    main()
