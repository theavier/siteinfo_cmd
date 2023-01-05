import typer
from checkSiteWhois import whois_domain_items
from checkSiteCMS import whatis_items
from checkSiteStatus import add_statuscode
from whereis import whereis_items
from loguru import logger
from tools import merge_list_dicts, log_init, list_or_item, save_or_print

app = typer.Typer()


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

    # add whereis results
    results_whereis = whereis_items(items)
    end_results = merge_list_dicts(end_results, results_whereis, "url")

    save_or_print(end_results, output)


@app.command('whereis')
def whereis_main(url: str = typer.Argument(None, help='url to scan'),
    csv: str = typer.Option(None, help='csv with urls to scan'),
    output: str = typer.Option(None, help='output filename'),
    verbose: bool = typer.Option(False)) -> None:
    """ Runs ip provider lookup on url """
    log_init(verbose)
    items = list_or_item(url, csv)
    end_results = whereis_items(items)
    save_or_print(end_results, output)

@app.command('whatis')
def whatis_main(url: str = typer.Argument(None, help='url to scan'),
    csv: str = typer.Option(None, help='csv with urls to scan'),
    output: str = typer.Option(None, help='output filename'),
    verbose: bool = typer.Option(False)) -> None:
    """ Runs whatcms on url """
    log_init(verbose)
    items = list_or_item(url, csv)
    end_results = whatis_items(items)
    save_or_print(end_results, output)


@app.command('status')
def status_main(url: str = typer.Argument(None, help='url to scan'),
    csv: str = typer.Option(None, help='csv with urls to scan'),
    output: str = typer.Option(None, help='output filename'),
    verbose: bool = typer.Option(False)) -> None:
    """ Runs ip lookup on url """
    log_init(verbose)
    items = list_or_item(url, csv)
    end_results = add_statuscode(items)
    save_or_print(end_results, output)


@app.command('whois')
def whois_main(url: str = typer.Argument(None, help='url to scan'),
             csv: str = typer.Option(None, help='csv with urls to scan'),
             output: str = typer.Option(None, help='output filename'),
             verbose: bool = typer.Option(False)) -> None:
    """ Runs whois on url """
    log_init(verbose)
    items = list_or_item(url, csv)
    results = whois_domain_items(items)
    save_or_print(results, output)


if __name__ == '__main__':
    app()
