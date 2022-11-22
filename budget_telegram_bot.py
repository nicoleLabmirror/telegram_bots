#!/usr/bin/python3

import datetime as dt

import pandas as pd

file_name = "YOUR FILE"
date = dt.date.today()


def get_data_from_file(file):
    headers = ["Date", "Shop", "Amount"]
    df_budget = pd.read_csv(file, delimiter=",", names=headers)

    return df_budget


def get_monthly_expenses():
    df_budget = get_data_from_file(file_name)
    df_budget.month = pd.DatetimeIndex(df_budget["Date"]).month
    df_budget_result = df_budget[df_budget.month == date.month]

    df_budget_result.year = pd.DatetimeIndex(df_budget_result["Date"]).year
    df_budget_result = df_budget_result[df_budget_result.year == date.year]

    return df_budget_result


def get_sum_of_expenses():
    monthly_expenses = get_monthly_expenses()
    total_amount_expenses = monthly_expenses.Amount.sum()

    return total_amount_expenses


def get_expenses_for_each_shop():
    monthly_expenses = get_monthly_expenses()
    monthly_expenses_groupby = monthly_expenses.groupby(["Shop"]).sum().reset_index()

    monthly_expenses_per_shop = [
        [monthly_expenses_groupby.Shop[entry], monthly_expenses_groupby.Amount[entry]]
        for entry in range(len(monthly_expenses_groupby))
    ]

    return monthly_expenses_per_shop


def write_data_to_file():
    df_budget = get_data_from_file(file_name)

    # TODO Still using test data here ;)
    df_new_entry = pd.DataFrame({"Date": date, "Shop": "BIPA", "Amount": [42.00]})

    # TODO FutureWarning: replace pandas.append and use pandas.concat instead
    df_budget = df_budget.append(df_new_entry, ignore_index=True)
    df_budget.to_csv(file_name, index=False, header=False)


def main():
    total_amount_expenses = get_sum_of_expenses()
    monthly_expenses_per_shop = get_expenses_for_each_shop()
    write_data_to_file()
    return total_amount_expenses, monthly_expenses_per_shop


if __name__ == "__main__":
    main()
