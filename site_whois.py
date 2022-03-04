import click
import whois
import re
from datetime import datetime
from checkSiteStatus import get_csv, write_csv

""" trims away http[s] and www."""
def cleanup_url(url: str) -> str:
    pattern_replace = re.compile(r"http[s]://|www.")
    return pattern_replace.sub("", url)


""" takes input dict, runs whois on url and returns item with added attributs to dict"""
def whois_domain(item: dict) -> dict:
    item_clean = cleanup_url(item['url'])
    w = whois.whois(item_clean)
    attributs_whois = ['registrant_name', 'expiration_date', 'registrar', 'name_servers']
    item['lookup'] = item_clean
    for attribut_whois in attributs_whois:
        #print(f'{item_clean}: Checking {attribut_whois}')
        try:
            if isinstance(w[attribut_whois], datetime):
                item[attribut_whois] = w[attribut_whois].strftime("%Y-%m-%d")
            elif isinstance(w[attribut_whois], list):
                item[attribut_whois] = ",".join(w[attribut_whois])
            else:
                item[attribut_whois] = w[attribut_whois]
        except BaseException as err:
            print(f'{item_clean}: Problem. Error: {err}')
            item[attribut_whois] = "N/A"
    return item


@click.command()
@click.option('--input', prompt='filename')
@click.option('--output', default='result.csv')
def run_main(input: str, output: str) -> None:
    items = get_csv(input)
    for item in items:
        item = whois_domain(item)
    print(items)




if __name__ == '__main__':
    run_main()