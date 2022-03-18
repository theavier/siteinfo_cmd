from ipwhois import IPWhois
import socket
import re
from typing import Union

""" gets network info from ip using IPWhois """
def query_ip(ip: str) -> dict:
    return (IPWhois(ip)).lookup_rdap(depth=1)


""" gets query_ip results into dict with relevant fields"""
def query_ip_result(ip: str) -> dict:
    result = query_ip(ip)
    return {
        "country": result['network']['country'],
        "network": result['asn_description'],
        "owners": result['network']['remarks'][0]['description'],
        "raw": result['network']
    }

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