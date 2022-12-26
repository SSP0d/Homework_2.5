from datetime import datetime, timedelta
from typing import Union
import aiohttp
import asyncio
import platform
import sys


def argument_parser() -> Union[int, str]:
    if len(sys.argv) == 0:
        arg: int = 1
    elif len(sys.argv) == 1:
        arg: int = int(sys.argv[1])
    elif len(sys.argv) == 2:
        currency: str = int(sys.argv[2])
    else:
        raise Exception('Error! Too many parameters')

    return arg, currency


def days() -> int:
    day: int = argument_parser()
    if day >= 11:
        raise Exception("Error! Too many day's. Max 10 day's")
    return day


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
