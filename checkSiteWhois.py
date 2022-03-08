import click
import whois
import re
from datetime import datetime
from checkSiteStatus import get_csv, write_csv

""" trims away http[s] and www."""
def cleanup_url(url: str) -> str:
    pattern_replace = re.compile(r"http[s]://|www.")
    return pattern_replace.sub("", url)


""" looks up domain and returns result """
def whois_domain(domain: str) -> dict:
    return whois.whois(domain)

def whois_domain_attribute_getter(w: dict, attributs: list = \
        ['registrant_name', 'expiration_date', 'registrar', 'name_servers','dnssec']) -> dict:
    _result = dict()
    for attribut_whois in attributs:
        try:
            if isinstance(w[attribut_whois], datetime):
                _result[attribut_whois] = w[attribut_whois].strftime("%Y-%m-%d")
            elif isinstance(w[attribut_whois], list):
                _result[attribut_whois] = ";".join(w[attribut_whois])
            else:
                _result[attribut_whois] = w[attribut_whois]
        except BaseException as err:
            print(f'{w["domain_name"]}: {attribut_whois} Problem. Error: {err}')
            _result[attribut_whois] = "N/A"
    return _result


def whois_domain_raw(items):
    for item in items:
        print(whois_domain(cleanup_url(item['url'])))


""" takes input dict, runs whois on url and returns item with added attributs to dict"""
def whois_domain_loop(items: list) -> list:
    _results = list()
    for item in items:
        item['domain'] = cleanup_url(item['url'])
        item_w = whois_domain(item['domain'])
        item.update(whois_domain_attribute_getter(item_w))
        _results.append(item)
    return _results


@click.command()
@click.option('--input', prompt='filename')
@click.option('--output', default='result.csv')
@click.option('--raw', default='False', type=bool)
def run_main(input: str, output: str, raw: bool) -> None:
    items = get_csv(input)
    if raw:
        whois_domain_raw(items)
    else:
        results = whois_domain_loop(items)
        write_csv(results, output)


if __name__ == '__main__':
    run_main()