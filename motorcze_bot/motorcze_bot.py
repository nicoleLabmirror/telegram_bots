#!/usr/bin/python3

import datetime as dt

import telepot as tb
import telepot.aio.loop
import telepot.loop

from sql_helper import read_route_data_from_db, write_route_data_to_db

BOT = tb.Bot("BOT_TOKEN")
CHAT_ID = "CHAT_ID"


def read_message_from_user(msg):
    user_text = msg["text"]
    user_id = msg["from"]["id"]

    handle_message(user_text, user_id)


def handle_message(user_text, user_id):
    if user_text == "?":
        text = read_route_data(user_id)
    else:
        write_route_data(user_text, user_id)
        text = "Route eingetragen"

    send_message(text)


def read_route_data(user_id):
    today_year = dt.date.today().year
    read_route = {
        "year": today_year,
        "person_id": user_id,
    }
    data = read_route_data_from_db(read_route)

    return data


def write_route_data(user_text, user_id):
    route_date = dt.date.today()
    route_name = user_text.split(" ")[0]
    route_distance = float(user_text.split(" ")[1])
    new_route = {
        "date": route_date,
        "name": route_name,
        "distance": route_distance,
        "person_id": user_id,
    }
    data = write_route_data_to_db(new_route)

    return data


def send_message(text):
    BOT.sendMessage(CHAT_ID, text)


def main():
    telepot.loop.MessageLoop(BOT, read_message_from_user).run_forever()


if __name__ == "__main__":
    main()
