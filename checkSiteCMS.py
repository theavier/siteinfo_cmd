import os
import json
from checkSiteStatus import validate_http, get_csv
import click
from loguru import logger

""" whatis query that runs wad-cmd"""
def query_whatis_run(domain:str) -> str:
        cmd = "wad -u "+domain
        return os.popen(cmd).read()


def whatis_items(items: list) -> list:
    # return [json.loads(query_whatis_run(validate_http(item["url"]))) for item in items]
    _results = list()
    for item in items:
        logger.info(f'{item["url"]}: Checking')
        _results.append(json.loads(query_whatis_run(validate_http(item["url"]))))
    return _results

def whatis_item(item: dict):
    logger.info(f'{item["url"]}: Checking')
    result = json.loads(query_whatis_run(validate_http(item['url'])))
    result_values = result.values()
    logger.info(f'looping type: {type(result_values)}')
    for sub_item in result_values:
        logger.info(f'type: {type(item)}, value: {sub_item} lap1')
        #item = sub_item.copy()
        item = item | sub_item
        for key in sub_item:

            print(key)

    # TODO figure out how to return same dict with added cmsinfo
    return item

def write_json(items: list, output) -> None:
    with open(output, 'w') as outfile:
        json.dump(items, outfile)



@click.command()
@click.option('--input', prompt='filename')
@click.option('--output', default='result_whatis.json')
def run_main(input: str, output: str) -> None:
    items = get_csv(input)
    results = whatis_items(items)
    #print(f'final results: {results}')
    write_json(results, output)


if __name__ == '__main__':
    run_main()
