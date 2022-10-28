import click
import csv
import requests
import re
from loguru import logger

""" imports csv content, returns list"""
def get_csv(_input: str) -> list:
    with open(_input) as csv_file:
        items = list(csv.DictReader(csv_file))
    return items

""" outputs changes to csv """
def write_csv(_items: list, output: str) -> None:
    keys = _items[0].keys()
    #print(f'items: {_items}')
    logger.info(f'items: {_items}')
    with open(output, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, keys)
        writer.writeheader()
        writer.writerows(_items)


""" adds https:// if missing"""
def validate_http(url: str) -> str:
    return url if re.match("^http[s]://", url) else f'https://{url}'


""" makes request, gets status and ip and returns result """
def add_statuscode(_items: list) -> list:
    return [add_statuscode_item(item) for item in _items]


def make_request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36', }):
    r = requests.get(validate_http(url), stream=True, headers=headers)
    ip = r.raw._connection.sock.getpeername()[0]
    return r.status_code, ip


def add_statuscode_item(item: dict) -> dict:
    def _add_status_fill_na(_item: dict, err_message: str) -> dict:
        _item['error'] = err_message
        _item['statuscode'] = _item['ip'] = "N/A"
        return _item

    logger.info(f"Checking {item['url']}")
    try:
        status_code, ip = make_request(item['url'])
        item['statuscode'] = status_code
        item['ip'] = ip
        item['error'] = ""
    except requests.exceptions.HTTPError as errh:
        logger.error(f"Http Error: {errh}", )
        item = _add_status_fill_na(item, "Http Error")
    except requests.exceptions.ConnectionError as errc:
        logger.error(f"Error Connecting: {errc}", )
        item = _add_status_fill_na(item, "ConnectionError")
    except requests.exceptions.Timeout as errt:
        logger.error(f"Timeout Error: {errt}")
        item = _add_status_fill_na(item, "Timeout")
    except requests.exceptions.RequestException as err:
        logger.error(f"OOps: Something Else {err}", )
        item = _add_status_fill_na(item, "Something else")
    return item


@click.command()
@click.option('--input', prompt='filename')
@click.option('--output', default='result.csv')
def run_main(input: str, output: str) -> None:
    logger.add("log.log", rotation="12:00")
    items = get_csv(input)
    results = add_statuscode(items)
    write_csv(results, output)


if __name__ == '__main__':
    run_main()
