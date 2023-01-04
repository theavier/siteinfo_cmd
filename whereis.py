from ipwhois import IPWhois
import socket
import re
from typing import Union
from loguru import logger
import typer
from tools import log_init, list_or_item, save_or_print

app = typer.Typer()


""" gets network info from ip using IPWhois """
def query_ip(ip: str) -> dict:
    return (IPWhois(ip)).lookup_rdap(depth=1)


""" extract relevant values from whois result """
def query_ip_extract(result):
    search_values = [('network', 'country'), 'asn_description', 'asn_country_code', 'query']
    result_dict = dict()
    for search_value in search_values:
        logger.info(f'Value: {search_value}, type: {type(search_value)}')
        try:
            if (isinstance(search_value, tuple)):
                result_dict.update({search_value[len(search_value)]: result[search_value][0][search_value[1]]})
            else:
                result_dict.update({search_value: result[search_value]})
        except BaseException as err:
            if isinstance(search_value, tuple):
                result_dict.update({search_value[-1]: "N/A"})
            else:
                result_dict.update({search_value: "N/A"})
    return result_dict


""" gets query_ip results into dict with relevant fields"""
def query_ip_result(ip: str) -> dict:
    result = query_ip(ip)
    result_extract = query_ip_extract(result)
    #return result
    return result_extract


""" get ip from url, strips http[s]:// from url """
def get_ip(urladdress: str) -> Union[str, bool]:
    urladdress = re.sub("http[s]?://", "", urladdress)
    try:
        hostname = socket.gethostbyname(urladdress)
        return hostname, True
    except BaseException as e:
        return "N/A, Error: "+str(e), False


def whereis_item(item):
    logger.debug(f'Running whereis on {item["url"]}')
    result_ip = get_ip(item['url'])
    result = query_ip_result(result_ip[0])
    if result:
        item['whereis'] = result
    else:
        item['whereis'] = "N/A"
    return item


def whereis_items(items):
    return [whereis_item(item) for item in items]


@app.command('lookup')
def main(url: str = typer.Argument(None, help='url to scan'),
    csv: str = typer.Option(None, help='csv with urls to scan'),
    output: str = typer.Option(None, help='output filename'),
    verbose: bool = typer.Option(False)) -> None:
    """ Runs ip provider lookup on url """
    log_init(verbose)
    items = list_or_item(url, csv)
    end_results = whereis_items(items)
    save_or_print(end_results, output)


if __name__ == '__main__':
    app()