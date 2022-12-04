#!/usr/bin/python3

import datetime as dt

import pandas as pd

import telepot as tb
import telepot.aio.loop
import telepot.loop


headers = ["Date", "Category", "Shop", "Amount"]
date = dt.date.today()

profile_1 = {
    "file_name": "YOUR FILE"
}

profile_2 = {
    "file_name": "ANOTHER FILE"
}


def read_data_from_file(file):
    df_budget = pd.read_csv(file, delimiter=",", names=headers)

    return df_budget


def get_monthly_expenses(file, category):
    df_budget = read_data_from_file(file)

    index_year = pd.DatetimeIndex(df_budget["Date"]).year
    df_budget_year = df_budget[index_year == date.year]

    if category == "Auto":
        return df_budget_year

    index_month = pd.DatetimeIndex(df_budget_year["Date"]).month
    df_budget_month = df_budget_year[index_month == date.month]

    return df_budget_month

def get_sum_of_expenses(file):
    monthly_expenses = get_monthly_expenses(file)

    total_amount_expenses = monthly_expenses.Amount.sum()

    return total_amount_expenses


def get_expenses_for_one_category(file, category):
    monthly_expenses = get_monthly_expenses(file, category)

    total_amount_expenses = monthly_expenses.Amount.sum()

    return total_amount_expenses


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
        [monthly_expenses_group_by.Shop[entry], monthly_expenses_group_by.Amount[entry]]
        for entry in range(len(monthly_expenses_group_by))
    ]

    return monthly_expenses_for_shops


def write_data_to_file(file, user_input):
    df_budget = read_data_from_file(file)

    df_new_entry = pd.DataFrame(
        {
            "Date": date,
            "Category": user_input[0],
            "Shop": user_input[1],
            "Amount": [user_input[2]],
        }
    )

    df_budget = pd.concat([df_budget, df_new_entry], ignore_index=True)

    df_budget.to_csv(file, index=False, header=False)


def send_message(data_to_send):
    if isinstance(data_to_send, float):
        print(f"Total expenses: {data_to_send}")
    else:
        for i in data_to_send:
            print(f"{i[0]}: {i[1]}")


def handle_user_input(user_profile, user_input):
    file = user_profile["file_name"]

    if user_input == "?":
        data_to_send = get_sum_of_expenses(file)
        send_message(data_to_send)

    elif "?" in user_input:
        category = user_input.split("?")[0]
        data_to_send = get_expenses_for_shops_of_one_category(file, category)
        send_message(data_to_send)

    else:
        user_input = [
            user_input.split()[0],
            user_input.split()[1],
            float(user_input.split()[2].replace(",", ".")),
        ]
        write_data_to_file(file, user_input)


def main():
    # TESTING
    handle_user_input(profile_2, "Auto?")
    #handle_user_input(profile_1, "Auto Shell 13,37")
    handle_user_input(profile_2, "Haushalt?")
    #handle_user_input(profile_2, "Auto Jet 42,00")
    #handle_user_input(profile_2, "?")
    #handle_user_input(profile_1, "?")


if __name__ == "__main__":
    main()
