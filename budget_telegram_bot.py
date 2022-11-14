#!/usr/bin/python3

import datetime as dt
import pandas as pd

file_name = "YOUR FILE"
file_name = "/home/k2/Dokumente/Code/PYTHON/bots/botToado2/toadoHaushalt_K.csv"

def get_monthly_expenses(file):
    headers = ["Date", "Shop", "Amount"]

    df_budget = pd.read_csv(file, delimiter=",", names=headers)
    #date = dt.date.today()
    df_budget.month = pd.DatetimeIndex(df_budget["Date"]).month
    df_budget_result = df_budget[df_budget.month == 4]#date.month]

    df_budget_result.year = pd.DatetimeIndex(df_budget_result["Date"]).year
    df_budget_result = df_budget_result[df_budget_result.year == 2021]#date.year]

    return df_budget_result

# Callback? Dunno ... still researching :D
def get_sum_of_expenses():
    monthly_expenses = get_monthly_expenses(file_name)
    total_amount_expenses = monthly_expenses.Amount.sum()
    return total_amount_expenses

def get_expenses_for_each_shop():
    monthly_expenses = get_monthly_expenses(file_name)
    test_1 = monthly_expenses.groupby(["Shop"]).sum().reset_index()
    test_2 = []
    for i in range(0, len(test_1)):
        x = test_1.Shop[i]
        y = test_1.Amount[i]
        test_2.append(
            [
                x,
                y
            ]
        )

    return test_2


def main():
    result = get_sum_of_expenses()
    test_3 = get_expenses_for_each_shop()
    return result, test_3