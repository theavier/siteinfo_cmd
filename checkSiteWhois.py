import click
import whois
import re
import sys
from loguru import logger
from datetime import datetime
from checkSiteStatus import get_csv, write_csv


def cleanup_url(url: str) -> str:
    """ trims away http[s] and www."""
    pattern_replace = re.compile(r"http[s]://|www\.")
    return pattern_replace.sub("", url)


def whois_domain(domain: str) -> dict:
    """ looks up domain and returns result """
    domain = cleanup_url(domain)
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


def whois_domain_items(items: list) -> list:
    """ takes input dict, runs whois on url and returns item with added attributs to dict"""
    _results = list()
    for item in items:
        item.update(whois_domain_extract(whois_domain(item['url'])))
        _results.append(item)
    #_results = [item.update(whois_domain_attributes(item['url'])) for item in items]
    #print(f'whois_domain_loop: outer type={type(_results)}, inner type={type(_results[0])}')
    return _results


@click.command()
@click.option('--csv', default='input.csv')
@click.option('--output', default='result.csv')
def run_main(csv: str, output: str) -> None:
    logger.add("log.log", rotation="12:00")
    items = get_csv(csv)
    results = whois_domain_items(items)
    write_csv(results, output)


if __name__ == '__main__':
    run_main()