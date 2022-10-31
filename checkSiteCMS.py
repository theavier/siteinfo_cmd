import os
import json
from checkSiteStatus import validate_http
import click
from loguru import logger
from tools import get_csv, write_csv, write_json

""" whatis query that runs wad-cmd"""
def query_whatis_run(domain:str) -> str:
        cmd = "wad -u "+domain
        return os.popen(cmd).read()


def whatis_items(items: list) -> list:
    """ runs whatis_item on list of dicts """
    return [whatis_item(item) for item in items]


def whatis_item(item: dict) -> dict:
    """ runs query_whatis_run on item['url'],
    turns returned json into dict and places into returning dict under ['cms']
    If return is empty, return N/A """
    logger.info(f'Checking: {item["url"]}')
    result = json.loads(query_whatis_run(validate_http(item['url'])))
    item['cms'] = list(result.values())[0] if result else "N/A"
    return item


@click.command()
@click.option('--csv', prompt='filename')
@click.option('--output', default='result_whatis.json')
def run_main(csv: str, output: str) -> None:
    items = get_csv(csv)
    results = whatis_items(items)
    #print(f'final results: {results}')
    write_json(results, output)


if __name__ == '__main__':
    run_main()
