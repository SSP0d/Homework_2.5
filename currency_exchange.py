from datetime import datetime, timedelta
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
            print('Error! Arg must be integer...')
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
    return [today.strftime('%d.%m.%Y')]

def link_generator(days: int = None) -> list[str]:
    days_range = []
    for day in days_to_view(days):
        urls = f'https://api.privatbank.ua/p24api/exchange_rates?json&date={day}'
        days_range.append(urls)
    return days_range


async def exchange(days: int = None) -> list[dict]:
    result_list = []
    for url in link_generator(days):
        async with aiohttp.ClientSession() as session:
            async with await session.get(url, ssl=False) as response:
                result = await response.json()
                date: str = result['date']
                rates_day = {}
                for el in result['exchangeRate']:
                    if el['currency'] in default_currency:
                        rates_day[el['currency']] = {'sale': el['saleRate'], 'purchase': el['purchaseRate']}
                result_list.append({date: rates_day})
            return result_list


if __name__ == '__main__':
    if platform.system() == 'Windows':
        asyncio.get_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    rate = asyncio.run(exchange())
    print(rate)