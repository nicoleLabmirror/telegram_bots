#!/usr/bin/python3

import datetime as dt
import time as t

import pandas as pd
import telepot as tb
import telepot.aio.loop
import telepot.loop

headers = ["Date", "Category", "Shop", "Amount"]

profile_1 = {
    "input_file_name": "YOUR FILE",
    "output_file_name": "YOUR FILE",
    "chat_id": "YOUR CHAT ID",
    "thank_you": "Nice",
    "input": "VERY NICE",
    "query": "SUPER nice",
    "xlsx": "Files!",
}

profile_2 = {
    "input_file_name": "ANOTHER FILE",
    "output_file_name": "ANOTHER FILE",
    "chat_id": "ANOTHER CHAT ID",
    "thank_you": "Thx",
    "input": "VERY THX",
    "query": "SUPER thx",
    "xlsx": "Files?",
}

YOUR_BOT = tb.Bot("YOUR_BOT_TOKEN")
YOUR_BOT.getMe()


def read_data_from_file(input_file):
    df_budget = pd.read_csv(input_file, delimiter=",", names=headers)

    return df_budget


def get_monthly_expenses(input_file, category):
    df_budget = read_data_from_file(input_file)
    today = dt.date.today()

    index_year = pd.DatetimeIndex(df_budget["Date"]).year
    df_budget_year = df_budget[index_year == today.year]

    if category == "Auto":
        return df_budget_year

    index_month = pd.DatetimeIndex(df_budget_year["Date"]).month
    df_budget_month = df_budget_year[index_month == today.month]

    return df_budget_month


def get_expenses_for_one_category(input_file, category):
    monthly_expenses = get_monthly_expenses(input_file, category)

    monthly_expenses_for_category = monthly_expenses[
        monthly_expenses["Category"] == category
    ]

    return monthly_expenses_for_category


def get_expenses_for_shops_of_one_category(input_file, category):
    monthly_expenses = get_expenses_for_one_category(input_file, category)

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


def write_data_to_file(input_file, user_input):
    df_budget = read_data_from_file(input_file)
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

    df_budget.to_csv(input_file, index=False, header=False)


def export_xlsx(input_file, output_file):
    df_budget = read_data_from_file(input_file)
    today = dt.date.today()

    index_year = pd.DatetimeIndex(df_budget["Date"]).year
    df_budget_year = df_budget[index_year == today.year]

    index_month = pd.DatetimeIndex(df_budget_year["Date"]).month
    index_month_set = set(index_month)

    with pd.ExcelWriter(output_file) as writer:
        for i in index_month_set:
            df_budget_month_by_index = df_budget_year[index_month == i]
            df_budget_month_for_excel = (
                df_budget_month_by_index.groupby(["Category"])
                .sum(numeric_only=True)
                .reset_index()
            )
            month_name_for_sheet = dt.datetime(today.year, i, 1).strftime("%B")
            df_budget_month_for_excel.to_excel(
                writer, sheet_name=month_name_for_sheet, index=False
            )


def send_message(group_chat_id, data_to_send, category=""):
    print(data_to_send)
    if not data_to_send[1]:
        YOUR_BOT.sendMessage(
            group_chat_id, f"There are no entries for category {category}."
        )

    elif category == "Excel":
        YOUR_BOT.sendMessage(
            group_chat_id,
            data_to_send[0],
        )
        YOUR_BOT.sendDocument(group_chat_id, data_to_send[1])

    elif category == "thanks":
        YOUR_BOT.sendMessage(group_chat_id, f"{data_to_send}")

    elif category == "input":
        YOUR_BOT.sendMessage(group_chat_id, f"{data_to_send}")

    elif category == "Auto":
        current_year = dt.date.today().strftime("%Y")
        data_of_shops_to_send = "\n".join(data_to_send[1])
        YOUR_BOT.sendMessage(
            group_chat_id,
            f"{data_to_send[0]}\n\n"
            f"There are following entries for category {category} in {current_year}:\n"
            f"{data_of_shops_to_send}",
        )

    else:
        current_month = dt.date.today().strftime("%B")
        data_of_shops_to_send = "\n".join(data_to_send[1])
        YOUR_BOT.sendMessage(
            group_chat_id,
            f"{data_to_send[0]}\n\n"
            f"There are following entries for category {category} in {current_month}:\n"
            f"{data_of_shops_to_send}",
        )


def handle_user_input(user_profile, user_input, group_chat_id):
    input_file = user_profile["input_file_name"]

    if user_input == "Excel?":
        output_file = user_profile["output_file_name"]
        export_xlsx(input_file, output_file)
        data_to_send = [user_profile["xlsx"], open(output_file, "rb")]
        category = "Excel"
        send_message(group_chat_id, data_to_send, category)

    elif "?" in user_input:
        category = user_input.split("?")[0]
        data_to_send = [
            user_profile["query"],
            get_expenses_for_shops_of_one_category(input_file, category),
        ]
        send_message(group_chat_id, data_to_send, category)

    elif "Thanks" in user_input:
        data_to_send = user_profile["thank_you"]
        category = "thanks"
        send_message(group_chat_id, data_to_send, category)

    else:
        category = "input"
        data_to_send = user_profile["input"]
        user_input = [
            user_input.split()[0],
            user_input.split()[1],
            float(user_input.split()[2].replace(",", ".")),
        ]
        write_data_to_file(input_file, user_input)
        send_message(group_chat_id, data_to_send, category)


def get_user_input(msg):
    content_type, chat_type, group_chat_id = telepot.glance(msg)

    if msg["from"]["id"] == profile_1["chat_id"]:
        handle_user_input(profile_1, msg["text"], group_chat_id)

    elif msg["from"]["id"] == profile_2["chat_id"]:
        handle_user_input(profile_2, msg["text"], group_chat_id)


def main():
    telepot.loop.MessageLoop(YOUR_BOT, get_user_input).run_forever()
    while True:
        t.sleep(10)


if __name__ == "__main__":
    main()
