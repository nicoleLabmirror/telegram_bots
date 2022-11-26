#!/usr/bin/python3

import datetime as dt

import pandas as pd

file_name = "YOUR FILE"
headers = ["Date", "Shop", "Amount"]
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


def get_expenses_for_each_shop():
    monthly_expenses = get_monthly_expenses()

    monthly_expenses_groupby = (
        monthly_expenses.groupby(["Shop"]).sum(numeric_only=True).reset_index()
    )
    monthly_expenses_per_shop = [
        [monthly_expenses_groupby.Shop[entry], monthly_expenses_groupby.Amount[entry]]
        for entry in range(len(monthly_expenses_groupby))
    ]

    return monthly_expenses_per_shop


def write_data_to_file(input_list):
    df_budget = get_data_from_file(file_name)

    df_new_entry = pd.DataFrame(
        {"Date": date, "Shop": input_list[0], "Amount": [input_list[1]]}
    )
    df_budget = pd.concat([df_budget, df_new_entry], ignore_index=True)

    df_budget.to_csv(file_name, index=False, header=False)


# TODO add user_profile
def handle_user_input(user_input):
    if user_input == "?":
        print(
            get_sum_of_expenses(), get_monthly_expenses(), get_expenses_for_each_shop()
        )
    else:
        user_input_list = [
            user_input.split()[0],
            float(user_input.split()[1].replace(",", ".")),
        ]
        write_data_to_file(user_input_list)


def main():
    # TESTING lol
    #    total_amount_expenses = get_sum_of_expenses()
    #    monthly_expenses_per_shop = get_expenses_for_each_shop()
    #    write_data_to_file()
    #    return total_amount_expenses, monthly_expenses_per_shop
    handle_user_input("Billa 43,00")
    handle_user_input("?")


if __name__ == "__main__":
    main()
