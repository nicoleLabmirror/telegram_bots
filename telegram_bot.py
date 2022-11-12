#!/usr/bin/python3

import datetime as dt
import bs4 as bs
import telepot as tb
import urllib3 as ul3

itn_bot = tb.Bot("YOUR BOT TOKEN")
chat_id = "YOUR CHAT ID"
url = "YOUR PLAYERS PROFILE"
file = "YOUR FILE"


def get_current_itn_value(url):
    request = ul3.PoolManager().request("GET", url)
    itn_from_web = bs.BeautifulSoup(request.data, "html.parser").find_all(
        "td", {"class": "text-right"}
    )
    itn_from_web = float(itn_from_web[0].text.strip().replace(",", "."))
    return itn_from_web


def read_itn_from_csv(file):
    with open(file, "r") as f:
        itn_from_file = f.read()[-6:]
    return itn_from_file


def write_itn_to_csv(file, itn_value):
    date = dt.datetime.now().strftime("%Y-%m-%d")
    with open(file, "a") as f:
        f.write(date + "," + str(itn_value) + "\n")


itn_old = float(read_itn_from_csv(file))
itn_new = get_current_itn_value(url)

if itn_new > itn_old:
    itn_bot.sendMessage(
        chat_id,
        "Hey Joe,\nbad news:\n {} auf {}.".format(itn_old, itn_new),
    )
    write_itn_to_csv(file, itn_new)

elif itn_new < itn_old:
    itn_bot.sendMessage(
        chat_id,
        "Hey Joe, \ngood news:\n {} up to {}.".format(itn_old, itn_new),
    )
    write_itn_to_csv(file, itn_new)

else:
    itn_bot.sendMessage(chat_id, "Hey Joe, nothing happend.")
    write_itn_to_csv(file, itn_new)
