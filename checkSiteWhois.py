import click
import whois
import re
from datetime import datetime
from checkSiteStatus import get_csv, write_csv

""" trims away http[s] and www."""
def cleanup_url(url: str) -> str:
    pattern_replace = re.compile(r"http[s]://|www\.")
    return pattern_replace.sub("", url)


""" looks up domain and returns result """
def whois_domain(domain: str) -> dict:
    domain = cleanup_url(domain)
    try:
        return whois.whois(domain)
    except BaseException as err:
        print(f'{domain} Problem. Error: {err}')
        return None


def whois_domain_extract(w: dict, attributs: list = \
        ['registrant_name', 'expiration_date', 'registrar', 'name_servers','dnssec','org']) -> dict:
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
                #print(f'{w["domain_name"]}: {attribut_whois} Problem. Error: {err}')
                _result[attribut_whois] = "N/A"
    else:
        _result = whois_domain_attribute_empty(_result, attributs)
    return _result

def whois_domain_attribute_empty(w: dict, attributs: list) -> dict:
    for attribut in attributs:
        w[attribut] = "Not found"
    return w

def whois_domain_attributes(url):
    return whois_domain_extract(whois_domain(url))

def whois_domain_raw(items):
    for item in items:
        print(whois_domain(cleanup_url(item['url'])))

def whois_domain_raw_name(item):
    print(whois_domain(cleanup_url(item)))

""" takes input dict, runs whois on url and returns item with added attributs to dict"""
def whois_domain_loop(items: list) -> list:
    _results = list()
    for item in items:
        item.update(whois_domain_attributes(item['url']))
        _results.append(item)

    #_results = [item.update(whois_domain_attributes(item['url'])) for item in items]
    #print(f'whois_domain_loop: outer type={type(_results)}, inner type={type(_results[0])}')
    return _results


@click.command()
@click.option('--input', default='input.csv')
@click.option('--input_raw', default=None)
@click.option('--output', default='result.csv')
@click.option('--raw', default='False', type=bool)
def run_main(input: str, input_raw: str, output: str, raw: bool) -> None:
    if input_raw:
        return whois_domain_raw_name(input_raw)
    else:
        items = get_csv(input)
    if raw:
        whois_domain_raw(items)
    else:
        results = whois_domain_loop(items)
        write_csv(results, output)


if __name__ == '__main__':
    run_main()