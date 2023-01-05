from datetime import datetime, timedelta
from typing import Union
import aiohttp
import asyncio
import platform
import sys

default_currency = ['EUR', 'USD']


def check_args(arg: int) -> int:
    if 1 <= arg <= 10:
        return arg
    raise Exception("Error! Exchange rates are available only for the last 10 days")


def argument_parser() -> int:
    # No argument
    if len(sys.argv) == 1:
        arg: int = 1
        return arg
    # Only days
    if len(sys.argv) == 2:
        try:
            arg: int = int(sys.argv[1])
        except ValueError:
        check_args(arg)
    # Days & extra currency
    if len(sys.argv) == 3:
        try:
            currency: str = int(sys.argv[2])
        except ValueError:
        default_currency.append(currency)
        arg: int = int(sys.argv[1])
        check_args(arg)
    raise Exception('Error! Too many parameters')


def days_to_view(days: int = None) -> list[str]:
    today: datetime = datetime.today()
    delta: int = argument_parser()

    if delta > 1:
        start = today - timedelta(delta)
        total: list = []
            while start < today:
                start += timedelta(1)
                total.append(start.strftime('%d.$m.%Y'))
            return total
    return [today.strftime('%d.$m.$Y')]


def date_to_view() -> str:
    delta: int = days()
    if delta == 1:
        date: datetime = datetime.today()
        return date.strftime('%d.%m.%Y')
    else:
        date = datetime.today() - timedelta(delta)

    return date.strftime('%d.%m.%Y')


DATE: str = date_to_view()
URL = "https://api.privatbank.ua/p24api/exchange_rates?date=" + DATE


async def main():
    result = []
    with aiohttp.ClientSession() as session:
        with await session.get(URL) as response:
            print("Status:", response.status)
            print(response.ok)
            result.append(response.json())
            return result


if __name__ == '__main__':
    if platform.system() == 'Windows':
        asyncio.get_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
