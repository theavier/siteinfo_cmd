from ipwhois import IPWhois
import socket
import re
from typing import Union

""" gets network info from ip using IPWhois """
def query_ip(ip: str) -> dict:
    return (IPWhois(ip)).lookup_rdap(depth=1)

"""WORK_IN_PROGRESS """
""" extract relevant values from whois result """
def query_ip_extract(result):
    search_values = [('network', 'country'), 'asn_description', 'asn_country_code']
    result_dict = dict()
    for search_value in search_values:
        print(f'Value: {search_value}, type: {type(search_value)}')
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

addresses = ['https://www.dataman.se',"https://www.lifelophelia.se"]

for item in addresses:
    print(f'value: {item}')
    #get ip
    result_ip = get_ip(item)
    print(f'result_ip: {result_ip}')
    result_query = query_ip_result(result_ip[0])
    print(f'result_query: {result_query}')