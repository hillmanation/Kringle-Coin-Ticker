import random as r
import csv
import pandas as pd
from datetime import date, datetime, time, timedelta
import nest_asyncio
from pywebio import *
from pywebio.output import *
from pywebio.input import *
from pywebio.session import *
nest_asyncio.apply()


def rand_trend(seed_a, change, variation):
    return round(r.uniform((seed_a + change) - r.randint(0, variation), (seed_a + change) + r.randint(0, variation)), 2)


def main():
    set_env(title='KringleKoin Ticker Config Page')
    set_env(input_panel_fixed=False)

    df = pd.read_csv('baseprices.csv')
    csv_size = len(df.index) - 1
    export = []
    start_time = datetime.strptime(df.iloc[csv_size, 2], '%H:%M:%S')
    initialKringle = df.iloc[csv_size - 1, 1]
    initialKeebler = df.iloc[csv_size, 1]
    print(df.loc[[csv_size-1]])
    print(df.loc[[csv_size]])
    new_time = start_time + timedelta(seconds=6)

    KringleKoin = input_group("KringleKoin",[
        input("\nEnter the value change for KringleKoin: ", name='change', type=NUMBER),
        checkbox(options=["Set above value to negative (for Samsung keyboard users)"], name='sign'),
        input("Enter random variation for KringleKoin: ", name='var', type=NUMBER)
    ])
    if KringleKoin['sign']:
        KringleKoin['change'] = int(KringleKoin['change'] * (-1))
    kringle_new_price = rand_trend(initialKringle, int(KringleKoin['change']), int(KringleKoin['var']))
    print(f"New KringleKoin value ${kringle_new_price}")
    export.append(("KringleKoin", kringle_new_price, new_time.strftime('%H:%M:%S'), 53))

    KeeblerCoin = input_group("KeeblerCoin", [
        input("\nEnter the value change for KeeblerCoin: ", name='change', type=NUMBER),
        checkbox(options=["Set above value to negative (for Samsung keyboard users)"], name='sign'),
        input("Enter random variation for KeeblerCoin: ", name='var', type=NUMBER)
    ])
    if KeeblerCoin['sign']:
        KeeblerCoin['change'] = int(KeeblerCoin['change'] * (-1))
    keebler_new_price = rand_trend(initialKeebler, int(KeeblerCoin['change']), int(KeeblerCoin['var']))
    print(f"New KeeblerCoin value ${keebler_new_price}")
    export.append(("KeeblerCoin", keebler_new_price, new_time.strftime('%H:%M:%S'), 53))

    export = tuple(export)

    with open("baseprices.csv", "a") as f:
        writer = csv.writer(f, delimiter=",", lineterminator="\r")
        writer.writerows(export)

    stock_ticker_new = [("COMPANY", "PRICE", "CHANGE")]

    with open('stock_list.csv', 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            old_price = float(row['PRICE'])

            if row['COMPANY'] == "KRNGL":
                new_price = kringle_new_price
            elif row['COMPANY'] == "KBCN":
                new_price = keebler_new_price
            else:
                new_price = rand_trend(old_price, 0, 18)

            change = new_price/old_price

            if change == 1:
                percent_change = 0.0
            elif change < 1:
                percent_change = round((new_price/old_price * 100) - 100, 2)
            else:
                percent_change = round((new_price/old_price * 100) - 100, 2)

            stock_ticker_new.append((row['COMPANY'], new_price, percent_change))

        csv_file.close()

    with open("stock_list.csv", "w") as f:
        writer = csv.writer(f, delimiter=",", lineterminator="\r")
        writer.writerows(stock_ticker_new)

    print(stock_ticker_new)

    put_button("Refresh", onclick=lambda: run_js('window.location.reload()'))


start_server(main, port=8080, debug=True)
