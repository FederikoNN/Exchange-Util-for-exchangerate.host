import asyncio
from datetime import timedelta, datetime
import aiohttp


async def currencies_list():
    url = 'https://api.exchangerate.host/symbols'
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            response = await resp.json()
            return response['symbols']


async def convert_currency(currency_base_code: str, currency_code: str,
                           currency_volume: float):
    url = f'https://api.exchangerate.host/convert?from=' \
          f'{currency_base_code}&to={currency_code}&places=2&amount=' \
          f'{currency_volume}'
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            response = await resp.json()
            return response['result']


# async def historical_rates(currency_base_code, currency_code, date_start,
#                            date_end, limit_connections):
#     url = f'https://api.exchangerate.host/timeseries?start_date=' \
#           f'{date_start}&end_date={date_end}' \
#           f'&base={currency_base_code}&symbols={currency_code}'
#     connector = aiohttp.TCPConnector(limit=int(limit_connections))
#     async with aiohttp.ClientSession(connector=connector) as session:
#         async with session.get(url) as resp:
#             response = await resp.json()
#             return response['rates']

async def historical_rates(currency_base_code: str, currency_code: str,
                           date_start: str, date_end: str,
                           currency_volume: float):
    date_start = datetime.strptime(date_start, '%Y-%m-%d')
    date_end = datetime.strptime(date_end, '%Y-%m-%d')
    out_dict = {}

    def daterange(start_date, end_date):
        for n in range(int((end_date - start_date).days) + 1):
            yield start_date + timedelta(n)

    async def fetch(client, date):
        url = f'https://api.exchangerate.host/' \
              f'{date.strftime("%Y-%m-%d")}' \
              f'?base={currency_base_code}&symbols={currency_code}&amount=' \
              f'{currency_volume}&places=2'
        async with client.get(url) as resp:
            response = await resp.json(content_type=None)
            out_dict[date.strftime("%Y-%m-%d")] = response["rates"][
                f"{currency_code}"]

    connector = aiohttp.TCPConnector(limit=50)
    async with aiohttp.ClientSession(connector=connector) as client:
        await asyncio.gather(
            *[asyncio.ensure_future(fetch(client, single_date)) for single_date
              in daterange(date_start, date_end)])
        [print(
            f'Date: {date}\tfrom {currency_volume} {currency_base_code} to '
            f'{currency_code}:{rate}')
            for date, rate in sorted(out_dict.items())]

# loop = asyncio.get_event_loop()
# loop.run_until_complete(
#     historical_rates('USD', 'EUR', '2020-01-01', '2020-05-01', 1000))
