import click
import json
from checkSiteWhois import whois_domain_loop, whois_domain, get_csv, write_csv, whois_domain_raw
from checkSiteCMS import whatis_loop


@click.command()
@click.option('--input', prompt='filename')
@click.option('--output', default='result.csv')
@click.option('--raw', default='False', type=bool)
@click.option('--who_is', default=True, type=bool)
@click.option('--what_is', default=True, type=bool)
def run_main(input: str, output: str, raw: bool, who_is: bool, what_is: bool) -> None:
    items = get_csv(input)
    if who_is and raw:
        whois_domain_raw(items)
    elif who_is and not raw:
        results = whois_domain_loop(items)[0]
    if what_is:
        results_whatis = whatis_loop(items)[0]
        #print(f'current type: {type(results_whatis)}')
        #print(results_whatis)
        # combine results
        results.update(results_whatis)




    print(f'results: {results}, type: {type(results)}')
    # write_csv(results, output)


if __name__ == '__main__':
    run_main()