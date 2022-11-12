#!/usr/bin/python3

import csv
import datetime as dt

import bs4 as bs
import telepot as tb
import urllib3 as ul3

itn_bot = tb.Bot("YOUR BOT TOKEN")
chat_id = "YOUR CHAT ID"
url = "YOUR PLAYERS PROFILE"
file = "YOUR FILE"

itn_bot = tb.Bot("580953211:AAG4yN0AmaO1wFNS48Rm1CWpV3-XRDiUkTw")
chat_id = 326247323

url = "www.noetv.at/spieler/detail/mm/pi/NU33326.html"
file = "/home/k2/Dokumente/Code/PYTHON/telegram_bots/values.csv"

def get_current_itn_value(url):
    request = ul3.PoolManager().request("GET", url)
    itn_from_web = bs.BeautifulSoup(request.data, "html.parser").find_all(
        "td", {"class": "text-right"}
    )
    itn_from_web = float(itn_from_web[0].text.strip().replace(",", "."))
    return itn_from_web


def read_itn_from_csv(file):
    with open(file, "r") as csv_file:
        data_from_csv = csv.reader(csv_file, delimiter=",")
        itn_data = [row for row in data_from_csv]
        itn_from_file = float(itn_data[-1][-1])
        return itn_from_file


def write_itn_to_csv(file, itn_value):
    date = dt.date.today()
    with open(file, "a") as csv_file:
        data_for_csv = csv.writer(csv_file, delimiter=",")
        data_for_csv.writerow([date, itn_value])


itn_old = read_itn_from_csv(file)
itn_new = get_current_itn_value(url)

if itn_new > itn_old:
    itn_bot.sendMessage(
        chat_id,
        f"Hey Joe, bad news: {itn_old} down to {itn_new}.",
    )
    write_itn_to_csv(file, itn_new)

elif itn_new < itn_old:
    itn_bot.sendMessage(
        chat_id,
        f"Hey Joe, good news: {itn_old} up to {itn_new}.",
    )
    write_itn_to_csv(file, itn_new)

else:
    itn_bot.sendMessage(chat_id, f"Hey Joe, nothing happend.")
    write_itn_to_csv(file, itn_new)
