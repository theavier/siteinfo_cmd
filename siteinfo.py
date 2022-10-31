import click
from checkSiteWhois import whois_domain_items
from checkSiteCMS import whatis_items
from checkSiteStatus import add_statuscode
from loguru import logger
from tools import merge_list_dicts, get_csv, write_csv, write_json


@click.command()
@click.option('--csv', prompt='filename')
@click.option('--output', default='result.csv')
@click.option('--raw', default='False', type=bool)
@click.option('--who_is', default=True, type=bool)
@click.option('--what_is', default=True, type=bool)
@click.option('--status', default=True, type=bool)
def run_main(csv: str, output: str, raw: bool, who_is: bool, what_is: bool, status: bool) -> None:
    items = get_csv(csv)
    end_results = list()
    #logger.info(f'results: {items}')
    if who_is:
        results_whois = whois_domain_items(items)
        end_results = merge_list_dicts(end_results, results_whois, "url")
    #logger.info(f'Current: {end_results}, after whois')
    if status:
        results_status = add_statuscode(items)
        end_results = merge_list_dicts(end_results, results_status, "url")
    #logger.info(f'Current: {end_results}, after status')
    if what_is:
        results_whatis = whatis_items(items)
        end_results = merge_list_dicts(end_results, results_whatis, "url")
    #logger.info(f'Current: {end_results}, after whatis')
    write_json(end_results, output)


if __name__ == '__main__':
    run_main()