import whois
import typer
import re
from loguru import logger
from datetime import datetime
from tools import get_csv, write_csv, log_remove_verbose

app = typer.Typer()

def cleanup_url(url: str) -> str:
    """ trims away http[s] and www."""
    pattern_replace = re.compile(r"http[s]://|www\.")
    return pattern_replace.sub("", url)


def whois_domain(domain: str) -> dict:
    """ looks up domain and returns result """
    logger.info(f'Running whois on {domain}')
    domain = cleanup_url(domain)
    logger.info(f'Cleaned {domain}')
    try:
        return whois.whois(domain)
    except BaseException as err:
        logger.warning(f'{domain} Problem. Error: {err}')
        return None


def whois_domain_extract(w: dict, attributs: list = \
        ['registrant_name', 'expiration_date', 'registrar', 'name_servers', 'dnssec', 'org']) -> dict:
    def _attribute_empty(w: dict, attributs: list) -> dict:
        for attribut in attributs:
            w[attribut] = "Not found"
        return w

    _result = dict()
    if w:
        for attribut_whois in attributs:
            try:
                if isinstance(w[attribut_whois], datetime):
                    _result[attribut_whois] = w[attribut_whois].strftime("%Y-%m-%d")
                elif isinstance(w[attribut_whois], list):
                    _result[attribut_whois] = ";".join(w[attribut_whois])
                else:
                    _result[attribut_whois] = w[attribut_whois]
            except BaseException as err:
                logger.warning(f'{w["domain_name"]}: {attribut_whois} Problem. Error: {err}')
                _result[attribut_whois] = "N/A"
    else:
        _result = _attribute_empty(_result, attributs)
    return _result


def whois_domain_items(items) -> list:
    """ takes input dict, runs whois on url and returns item with added attributs to dict"""
    _results = list()
    for item in items:
        item.update(whois_domain_extract(whois_domain(item['url'])))
        _results.append(item)
    return _results


@app.command('lookup')
def run_main(url: str = typer.Argument(None, help='url to scan'),
             csv: str = typer.Option(None, help='csv with urls to scan'),
             output: str = typer.Option(None, help='output filename'),
             verbose: bool = typer.Option(False)) -> None:
    """ main function """
    if verbose is not True:
        log_remove_verbose()
    logger.add("log.log")
    if csv:
        logger.info(f'csv param used: {csv}')
        items = get_csv(csv)
        results = whois_domain_items(items)
    else:
        logger.info(f'url param used: {url}')
        results = whois_domain_extract(whois_domain(url))
    if output:
        logger.info(f' output param used: {output}')
        write_csv(results, output)
    else:
        logger.info(f'Printing results...')
        print(results)


if __name__ == '__main__':
    app()
