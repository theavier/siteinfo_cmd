import typer
import os
import json
from checkSiteStatus import validate_http
from loguru import logger
from tools import get_csv, write_csv, write_json, log_init, list_or_item, save_or_print

app = typer.Typer()

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

@app.command('lookup')
def run_main(url: str = typer.Argument(None, help='url to scan'),
    csv: str = typer.Option(None, help='csv with urls to scan'),
    output: str = typer.Option(None, help='output filename'),
    verbose: bool = typer.Option(False)) -> None:

    log_init(verbose)
    items = list_or_item(url, csv)
    end_results = whatis_items(items)
    save_or_print(end_results, output)


if __name__ == '__main__':
    app()
