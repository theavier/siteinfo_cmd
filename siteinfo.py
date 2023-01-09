import typer
from checkSiteWhois import whois_domain_items
from checkSiteCMS import whatis_items
from checkSiteStatus import add_statuscode
from whereis import whereis_items
from loguru import logger
from tools import merge_list_dicts, log_init, list_or_item, save_or_print
from functools import partial

app = typer.Typer()
state = {"verbose": False, "csv": None, "output": None}

@app.command('all')
def run_main(url: str = typer.Argument(None, help='url to scan')) -> None:
    """ Runs whois, ip lookup and whatcms on url(s) """
    log_init(state['verbose'])
    items = list_or_item(url, state['csv'])

    all_functions = [partial(whois_domain_items), partial(add_statuscode), partial(whatis_items),
                     partial(whereis_items)]
    end_results = list()
    for all_function in all_functions:
        results_func = all_function(items)
        end_results = merge_list_dicts(end_results, results_func, "url")

    save_or_print(end_results, state['output'])


@app.command('whereis')
def whereis_main(url: str = typer.Argument(None, help='url to scan')) -> None:
    """ Runs ip provider lookup on url """
    log_init(state['verbose'])
    items = list_or_item(url, state['csv'])
    end_results = whereis_items(items)
    save_or_print(end_results, state['output'])


@app.command('whatis')
def whatis_main(url: str = typer.Argument(None, help='url to scan')) -> None:
    """ Runs whatcms on url """
    log_init(state['verbose'])
    items = list_or_item(url, state['csv'])
    end_results = whatis_items(items)
    save_or_print(end_results, state['output'])


@app.command('status')
def status_main(url: str = typer.Argument(None, help='url to scan')) -> None:
    """ Runs ip lookup on url """
    log_init(state['verbose'])
    items = list_or_item(url, state['csv'])
    end_results = add_statuscode(items)
    save_or_print(end_results, state['output'])


@app.command('whois')
def whois_main(url: str = typer.Argument(None, help='url to scan')) -> None:
    """ Runs whois on url """
    log_init(state['verbose'])
    items = list_or_item(url, state['csv'])
    results = whois_domain_items(items)
    save_or_print(results, state['output'])


@app.callback()
def main(csv: str = typer.Option(None, help='csv with urls to scan'),
         output: str = typer.Option(None, help='output filename'),
         verbose: bool = typer.Option(False, help='show verbose')) -> None:
    """ General site information tools """
    if verbose:
        state['verbose'] = True
    if csv:
        state['csv'] = csv
    if output:
        state['output'] = output




if __name__ == '__main__':
    app()
