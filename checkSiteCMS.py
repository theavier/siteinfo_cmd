import os
import json
from checkSiteStatus import validate_http, get_csv
import click

""" whatis query that runs wad-cmd"""
def query_whatis_run(domain:str) -> str:
        cmd = "wad -u "+domain
        return os.popen(cmd).read()


def whatis_loop(items: list) -> list:
    # return [json.loads(query_whatis_run(validate_http(item["url"]))) for item in items]
    _results = list()
    for item in items:
        print(f'{item["url"]}: Checking')
        _results.append(json.loads(query_whatis_run(validate_http(item["url"]))))
    return _results

def write_json(items: list, output) -> None:
    with open(output, 'w') as outfile:
        json.dump(items, outfile)

@click.command()
@click.option('--input', prompt='filename')
@click.option('--output', default='result_whatis.json')
def run_main(input: str, output: str) -> None:
    items = get_csv(input)
    results = whatis_loop(items)
    #print(f'final results: {results}')
    write_json(results, output)


if __name__ == '__main__':
    run_main()
