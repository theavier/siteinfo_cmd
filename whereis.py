from ipwhois import IPWhois
import socket
import re
from typing import Union
from loguru import logger

NOT_FOUND_MSG = "N/A"

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
    return result_extract


""" get ip from url, strips http[s]:// from url """
def get_ip(urladdress: str) -> Union[str, bool]:
    urladdress = re.sub("http[s]?://", "", urladdress)
    try:
        hostname = socket.gethostbyname(urladdress)
        return hostname, True
    except BaseException as e:
        return "N/A, Error: "+str(e), False


def whereis_item(item: dict):
    logger.debug(f'{item["url"]}: running whereis...')
    result_ip, status = get_ip(item['url'])
    if status:
        logger.debug(f'{item["url"]}: running against ip {result_ip}, type: {type(result_ip)}')
        try:
            if isinstance(result_ip, str):
                result = query_ip_result(result_ip)
            else:
                logger.warning(f'Issue at {item["url"]}, type: {type(result_ip)}')
                result = query_ip_result(result_ip[0])
            end_result = result if result else NOT_FOUND_MSG
        except:
            logger.warning(f'Running against ip: {result_ip}, type: {type(result_ip)}')
            end_result = NOT_FOUND_MSG
    else:
        end_result = NOT_FOUND_MSG
        logger.warning(f'{item["url"]}: {result_ip}')
    item['whereis'] = end_result
    return item


def whereis_items(items: list):
    return [whereis_item(item) for item in items]
