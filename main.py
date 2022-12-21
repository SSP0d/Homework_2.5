from datetime import datetime, timedelta
import aiohttp
import asyncio
import platform
import sys


def argument_parser() -> int:
    if len(sys.argv) == 1:
        day: int = 1
    elif len(sys.argv) == 2:
        day: int = int(sys.argv[1])
    else:
        raise Exception('Error! Too many parameters')

    return day


def day_to_view() -> int:
    day: int = argument_parser()
    if day >= 11:
        raise Exception("Error! Too many day's. Max 10 day's")
    return day


def date_to_view() -> str:
    delta = day_to_view()
    if delta == 1:
        date = datetime.today()
        return date.strftime('%d.%m.%Y')
    else:
        date = datetime.today() - timedelta(delta)

    return date.strftime('%d.%m.%Y')


DATE: str = date_to_view()
URL = "https://api.privatbank.ua/p24api/exchange_rates?date=" + DATE


async def main():
    with aiohttp.ClientSession() as session:
        with await session.get(URL) as response:
            print("Status:", response.status)
            print("Content-type:", response.headers['content-type'])
            print('Cookies: ', response.cookies)
            print(response.ok)
            result = response.json()
            return result


if __name__ == '__main__':
    if platform.system() == 'Windows':
        asyncio.get_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
