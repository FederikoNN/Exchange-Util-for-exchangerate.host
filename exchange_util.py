import asyncio
from api_requests import currencies_list, convert_currency, historical_rates
import argparse


def currencies_list_out(args):
    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(currencies_list())
    return [print(f'{a}- {b["description"]}') for a, b in result.items()]


def convert_currency_out(args):
    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(
        convert_currency(args.fr, args.to, args.volume))
    return print(result)


def historical_rates_out(args):
    date_from = f'{args.date_from[:4]}-{args.date_from[4:6]}-' \
                f'{args.date_from[6:]}'
    date_to = f'{args.date_to[:4]}-{args.date_to[4:6]}-{args.date_to[6:]}'
    loop = asyncio.get_event_loop()
    loop.run_until_complete(
        historical_rates(args.fr, args.to, date_from, date_to, args.volume))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('cmd', type=str)
    subparsers = parser.add_subparsers()
    parser_pow = subparsers.add_parser('symbols')
    parser_pow.set_defaults(f=currencies_list_out)

    parser_log = subparsers.add_parser('convert')
    parser_log.add_argument('-from', dest='fr', type=str)
    parser_log.add_argument('-to', type=str)
    parser_log.add_argument('volume', type=float)
    parser_log.set_defaults(f=convert_currency_out)

    parser_log = subparsers.add_parser('history')
    parser_log.add_argument('-from', dest='fr', type=str)
    parser_log.add_argument('-to', type=str)
    parser_log.add_argument('-date_from', type=str)
    parser_log.add_argument('-date_to', type=str)
    parser_log.add_argument('volume', type=float)
    parser_log.set_defaults(f=historical_rates_out)

    p = parser.parse_args()
    p.f(p)
