import platform

import aiohttp
import asyncio

import logging
from datetime import datetime, timedelta

import sys

data_output = []

async def request(url: str):
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url) as resp:
                if resp.status == 200:
                    r = await resp.json()
                    return r
                logging.error(f"Error status: {resp.status} for {url}")
                return None
        except aiohttp.ClientConnectorError as err:
            logging.error(f"Connection error: {str(err)}")
            return None

def time_interval():
    if sys.argv:
        command = " ".join(sys.argv)
        _, days_amount, *_ = command.split()
        if days_amount and 0 < int(days_amount) <= 10:
            return int(days_amount)        
    else:
        while True:
            try:
                interval = int(input("Enter the digit - time interval in days, not > 10: "))
                if 0 < interval <= 10:
                    return interval
                print("Input interval: ")
            except ValueError:
                print("Please, enter the digit")

async def get_exchange():
    nowdate = datetime.now()
    amount_days = time_interval()    
    for day in range(0, amount_days):
        date = (nowdate - timedelta(days=day)).strftime('%d.%m.%Y')
        result = await request(f"https://api.privatbank.ua/p24api/exchange_rates?date={date}")
        if result:
            res = result["exchangeRate"]
            cur_usd = list(filter(lambda el: el["currency"] == "USD", res))
            cur_eur = list(filter(lambda el: el["currency"] == "EUR", res))

            data_output.append({date: cur_usd + cur_eur})

    return data_output
        



if __name__ == "__main__":
    if platform.system() == 'Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    result = asyncio.run(get_exchange())
    print(result)