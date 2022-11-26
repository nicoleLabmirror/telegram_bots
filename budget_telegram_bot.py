#!/usr/bin/python3

import datetime as dt

import pandas as pd

file_name = "YOUR FILE"
headers = ["Date", "Category", "Shop", "Amount"]
date = dt.date.today()


def get_data_from_file(file):
    df_budget = pd.read_csv(file, delimiter=",", names=headers)

    return df_budget


def get_monthly_expenses():
    df_budget = get_data_from_file(file_name)

    index_month = pd.DatetimeIndex(df_budget["Date"]).month
    df_budget_month = df_budget[index_month == date.month]

    index_year = pd.DatetimeIndex(df_budget_month["Date"]).year
    df_budget_result = df_budget_month[index_year == date.year]

    return df_budget_result


def get_sum_of_expenses():
    monthly_expenses = get_monthly_expenses()
    total_amount_expenses = monthly_expenses.Amount.sum()

    return total_amount_expenses


def get_expenses_for_one_category(category_name):
    monthly_expenses = get_monthly_expenses()

    monthly_expenses_for_category = monthly_expenses[
        monthly_expenses["Category"] == category_name
    ]

    return monthly_expenses_for_category


def get_expenses_for_shops_of_one_category(input_category):
    monthly_expenses = get_expenses_for_one_category(input_category)

    monthly_expenses_group_by = (
        monthly_expenses.groupby(["Shop"]).sum(numeric_only=True).reset_index()
    )

    monthly_expenses_for_shops = [
        [monthly_expenses_group_by.Shop[entry], monthly_expenses_group_by.Amount[entry]]
        for entry in range(len(monthly_expenses_group_by))
    ]

    return monthly_expenses_for_shops


def write_data_to_file(input_list):
    df_budget = get_data_from_file(file_name)

    df_new_entry = pd.DataFrame(
        {
            "Date": date,
            "Category": input_list[0],
            "Shop": input_list[1],
            "Amount": [input_list[2]],
        }
    )

    df_budget = pd.concat([df_budget, df_new_entry], ignore_index=True)

    df_budget.to_csv(file_name, index=False, header=False)


# TODO add user_profile
def handle_user_input(user_input):
    if "?" in user_input:
        category = user_input.split("?")[0]
        print(get_expenses_for_shops_of_one_category(category))

    else:
        user_input_list = [
            user_input.split()[0],
            user_input.split()[1],
            float(user_input.split()[2].replace(",", ".")),
        ]
        write_data_to_file(user_input_list)


def main():
    # TESTING lol
    handle_user_input("Haushalt?")
    handle_user_input("Haushalt Hofer 0,01")
    handle_user_input("Haushalt?")
    handle_user_input("Auto?")
    handle_user_input("Auto Shell 13,37")
    handle_user_input("Auto?")


if __name__ == "__main__":
    main()
