import click
import json
from checkSiteWhois import whois_domain_items, whois_domain, get_csv, write_csv
from checkSiteCMS import whatis_items
from checkSiteStatus import add_statuscode
from loguru import logger
from tools import merge_list_dicts

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
    logger.info(f'results: {items}')
    if who_is:
        results_whois = whois_domain_items(items)
        end_results = merge_list_dicts(end_results, results_whois, "url")
    if status:
        results_status = add_statuscode(items)
        end_results = merge_list_dicts(end_results, results_status, "url")
    #if what_is:
     #   results_whatis = whatis_loop(items)[0]
        #print(f'current type: {type(results_whatis)}')
        #print(results_whatis)
        # combine results
        #results.update(results_whatis)
    logger.info(f"Type: {type(end_results)}Results: {end_results}")
    # write_csv(results, output)


if __name__ == '__main__':
    run_main()