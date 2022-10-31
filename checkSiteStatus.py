import click
import requests
import re
from loguru import logger
from tools import get_csv, write_csv


def validate_http(url: str) -> str:
    """ adds https:// if missing"""
    return url if re.match("^http[s]://", url) else f'https://{url}'


def add_statuscode(_items: list) -> list:
    """ makes request, gets status and ip and returns result """
    return [add_statuscode_item(item) for item in _items]


def make_request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36', }):
    """ makes connection to url """
    r = requests.get(validate_http(url), stream=True, headers=headers)
    ip = r.raw._connection.sock.getpeername()[0]
    return r.status_code, ip


def add_statuscode_item(item: dict) -> dict:
    """ makes lookup of ip for item, adds ip and statuscode to dict """
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
@click.option('--input_file', prompt='filename')
@click.option('--output', default='result.csv')
def run_main(input_file: str, output: str) -> None:
    logger.add("log.log", rotation="12:00")
    items = get_csv(input_file)
    results = add_statuscode(items)
    write_csv(results, output)


if __name__ == '__main__':
    run_main()
