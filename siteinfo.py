import typer
from checkSiteWhois import whois_domain_items
from checkSiteCMS import whatis_items
from checkSiteStatus import add_statuscode
from loguru import logger
from tools import merge_list_dicts, get_csv, write_json, log_remove_verbose
from checkSiteWhois import app as whois_app
from checkSiteStatus import app as status_app
from checkSiteCMS import app as whatis_app

app = typer.Typer()
app.add_typer(whois_app, name='whois')
app.add_typer(status_app, name='status')
app.add_typer(whatis_app, name='whatis')


@app.command('lookup')
def run_main(url: str = typer.Argument(None, help='url to scan'),
            csv: str = typer.Option(None, help='csv with urls to scan'),
            output: str = typer.Option(None, help='output filename'),
            verbose: bool = typer.Option(True)) -> None:

    if verbose is not True:
        log_remove_verbose()
    logger.add("log.log")

    end_results = list()
    if csv:
        logger.debug(f'csv param used: {csv}')
        items = get_csv(csv)
        logger.debug(f'items: {items}')
        results = whois_domain_items(items)
    else:
        logger.debug(f'no csv param used: {url}')
        items = [{'url': url}]
        logger.debug(f'after making list: {items}')
    logger.info(f'results: {items}')

    # add whois results
    results_whois = whois_domain_items(items)
    end_results = merge_list_dicts(end_results, results_whois, "url")
    logger.info(f'Current: {end_results}, after whois')

    # add status results
    results_status = add_statuscode(items)
    end_results = merge_list_dicts(end_results, results_status, "url")
    logger.info(f'Current: {end_results}, after status')

    # add whatis results
    results_whatis = whatis_items(items)
    end_results = merge_list_dicts(end_results, results_whatis, "url")
    logger.info(f'Current: {end_results}, after whatis')

    # output results
    if output:
        logger.info(f' output param used: {output}')
        write_json(end_results, output)
    else:
        logger.info(f'Printing results...')
        print(end_results)


if __name__ == '__main__':
    app()
