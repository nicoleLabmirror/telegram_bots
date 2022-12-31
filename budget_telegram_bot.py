#!/usr/bin/python3

import datetime as dt
import time as t

import pandas as pd
import telepot as tb
import telepot.aio.loop
import telepot.loop

headers = ["Date", "Category", "Shop", "Amount"]

profile_1 = {
    "file_name": "YOUR FILE",
    "chat_id": "YOUR CHAT ID",
    "thank_you": "Nice",
    "input": "VERY NICE",
    "query": "SUPER nice",
}

profile_2 = {
    "file_name": "ANOTHER FILE",
    "chat_id": "ANOTHER CHAT ID",
    "thank_you": "Thx",
    "input": "VERY THX",
    "query": "SUPER thx",
}

YOUR_BOT = tb.Bot("YOUR_BOT_TOKEN")
YOUR_BOT.getMe()


def read_data_from_file(file):
    df_budget = pd.read_csv(file, delimiter=",", names=headers)

    return df_budget


def get_monthly_expenses(file, category):
    df_budget = read_data_from_file(file)
    today = dt.date.today()

    index_year = pd.DatetimeIndex(df_budget["Date"]).year
    df_budget_year = df_budget[index_year == today.year]

    if category == "Auto":
        return df_budget_year

    index_month = pd.DatetimeIndex(df_budget_year["Date"]).month
    df_budget_month = df_budget_year[index_month == today.month]

    return df_budget_month


def get_expenses_for_one_category(file, category):
    monthly_expenses = get_monthly_expenses(file, category)

    monthly_expenses_for_category = monthly_expenses[
        monthly_expenses["Category"] == category
    ]

    return monthly_expenses_for_category


def get_expenses_for_shops_of_one_category(file, category):
    monthly_expenses = get_expenses_for_one_category(file, category)

    monthly_expenses_group_by = (
        monthly_expenses.groupby(["Shop"]).sum(numeric_only=True).reset_index()
    )

    monthly_expenses_for_shops = [
        ": ".join(
            [
                monthly_expenses_group_by.Shop[entry],
                str(monthly_expenses_group_by.Amount[entry]),
            ]
        )
        for entry in range(len(monthly_expenses_group_by))
    ]

    return monthly_expenses_for_shops


def write_data_to_file(file, user_input):
    df_budget = read_data_from_file(file)
    today = dt.date.today()

    df_new_entry = pd.DataFrame(
        {
            "Date": today,
            "Category": user_input[0],
            "Shop": user_input[1],
            "Amount": [user_input[2]],
        }
    )

    df_budget = pd.concat([df_budget, df_new_entry], ignore_index=True)

    df_budget.to_csv(file, index=False, header=False)


def send_message(chat_id, data_to_send, category=""):
    if not data_to_send:
        YOUR_BOT.sendMessage(chat_id, f"There are no entries for category {category}.")

    elif category == "thanks":
        YOUR_BOT.sendMessage(chat_id, f"{data_to_send}")

    elif category == "input":
        YOUR_BOT.sendMessage(chat_id, f"{data_to_send}")

    elif category == "Auto":
        current_year = dt.date.today().strftime("%Y")
        data_of_shops_to_send = "\n".join(data_to_send[1])
        YOUR_BOT.sendMessage(
            chat_id,
            f"{data_to_send[0]}\n\n"
            f"There are following entries for category {category} in {current_year}:\n"
            f"{data_of_shops_to_send}",
        )

    else:
        current_month = dt.date.today().strftime("%B")
        data_of_shops_to_send = "\n".join(data_to_send[1])
        YOUR_BOT.sendMessage(
            chat_id,
            f"{data_to_send[0]}\n\n"
            f"There are following entries for category {category} in {current_month}:\n"
            f"{data_of_shops_to_send}",
        )


def handle_user_input(user_profile, user_input):
    file = user_profile["file_name"]
    user_chat_id = user_profile["chat_id"]

    if "?" in user_input:
        category = user_input.split("?")[0]
        data_to_send = [
            user_profile["query"],
            get_expenses_for_shops_of_one_category(file, category),
        ]
        send_message(user_chat_id, data_to_send, category)

    elif "Thanks" in user_input:
        data_to_send = user_profile["thank_you"]
        category = "thanks"
        send_message(user_chat_id, data_to_send, category)

    else:
        category = "input"
        data_to_send = user_profile["input"]
        user_input = [
            user_input.split()[0],
            user_input.split()[1],
            float(user_input.split()[2].replace(",", ".")),
        ]
        write_data_to_file(file, user_input)
        send_message(user_chat_id, data_to_send, category)


def get_user_input(msg):
    if msg["from"]["id"] == profile_1["chat_id"]:
        handle_user_input(profile_1, msg["text"])

    elif msg["from"]["id"] == profile_2["chat_id"]:
        handle_user_input(profile_2, msg["text"])


def main():
    telepot.loop.MessageLoop(YOUR_BOT, get_user_input).run_forever()
    while True:
        t.sleep(10)


if __name__ == "__main__":
    main()
