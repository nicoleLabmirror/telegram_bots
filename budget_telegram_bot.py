#!/usr/bin/python3

import datetime as dt
import pandas as pd

file_name = "YOUR FILE"

def get_monthly_expenses(file):
    headers = ["Date", "Shop", "Amount"]

    df_budget = pd.read_csv(file, delimiter=",", names=headers)
    date = dt.date.today()
    df_budget.month = pd.DatetimeIndex(df_budget["Date"]).month
    df_budget_result = df_budget[df_budget.month == date.month]

    df_budget_result.year = pd.DatetimeIndex(df_budget_result["Date"]).year
    df_budget_result = df_budget_result[df_budget_result.year == date.year]

    return df_budget_result

# Callback? Dunno ... still researching :D
def get_sum_of_expenses(file):
    monthly_expenses = get_monthly_expenses(file)
    total_amount_expenses = monthly_expenses.Amount.sum()
    return total_amount_expenses

def main():
    result = get_sum_of_expenses(file_name)
    return result