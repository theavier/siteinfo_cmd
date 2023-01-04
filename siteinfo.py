import typer
from checkSiteWhois import whois_domain_items
from checkSiteCMS import whatis_items
from checkSiteStatus import add_statuscode
from loguru import logger
from tools import merge_list_dicts, log_init, list_or_item, save_or_print
from checkSiteWhois import main as whois_main
from checkSiteStatus import main as status_main
from checkSiteCMS import main as whatis_main
from whereis import main as whereis_main

app = typer.Typer()
app.command('whois')(whois_main)
app.command('status')(status_main)
app.command('whatis')(whatis_main)
app.command('whereis')(whereis_main)

@app.command('all')
def run_main(url: str = typer.Argument(None, help='url to scan'),
            csv: str = typer.Option(None, help='csv with urls to scan'),
            output: str = typer.Option(None, help='output filename'),
            verbose: bool = typer.Option(True)) -> None:
    """ Runs whois, ip lookup and whatcms on url(s) """
    log_init(verbose)
    items = list_or_item(url, csv)
    end_results = list()

    # add whois results
    results_whois = whois_domain_items(items)
    end_results = merge_list_dicts(end_results, results_whois, "url")

    # add status results
    results_status = add_statuscode(items)
    end_results = merge_list_dicts(end_results, results_status, "url")

    # add whatis results
    results_whatis = whatis_items(items)
    end_results = merge_list_dicts(end_results, results_whatis, "url")

    save_or_print(end_results, output)


if __name__ == '__main__':
    app()
