import click
import whois
import re
from checkSiteStatus import get_csv, write_csv

""" trims away http[s] and www."""
def cleanup_url(url: str) -> str:
    pattern_replace = re.compile(r"http[s]://|www.")
    return pattern_replace.sub("", url)

@click.command()
@click.option('--input', prompt='filename')
@click.option('--output', default='result.csv')
def run_main(input: str, output: str) -> None:
    items = get_csv(input)
    for item in items:
        item_clean = cleanup_url(item['url'])
        print(f'{item_clean}:, type:{type(item_clean)} Checking...')
        w = whois.whois(item_clean)
        print(w['registrant_name'])
        item['lookup'] = item_clean
        item['registrant'] = w['registrant_name']
        item['expiration_date'] = w['expiration_date'].strftime("%Y-%m-%d")
        item['registrar'] = w['registrar']
        ns = [re.findall(r"\w+[.]\w+[.]\w+",item) for item in w['name_servers']]
        print(ns)



if __name__ == '__main__':
    run_main()