import click
import csv
import requests
import re

""" imports csv content, returns list"""
def get_csv(_input: str) -> list:
    with open(_input) as csv_file:
        items = list(csv.DictReader(csv_file))
    return items

""" outputs changes to csv """
def write_csv(_items: list, output: str) -> None:
    keys = _items[0].keys()
    print(f'items: {_items}')
    with open(output, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, keys)
        writer.writeheader()
        writer.writerows(_items)


""" adds https:// if missing"""
def validate_http(url):
    return url if re.match("^http[s]://", url) else f'https://{url}'


""" makes request, gets status and ip and returns result """
def add_statuscode(_items: list) -> list:
    def _add_status_fill_na(_item_err, err_message):
        _item_err['error'] = err_message
        _item_err['statuscode'] = "N/A"
        _item_err['ip'] = "N/A"
        return _item_err
    results = list()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36', }
    for item in _items:
        try:
            r = requests.get(validate_http(item['url']), stream=True, headers=headers)
            ip = r.raw._connection.sock.getpeername()[0]
            item['statuscode'] = r.status_code
            item['ip'] = ip
            item['error'] = ""
        except requests.exceptions.HTTPError as errh:
            print("Http Error:", errh)
            item = _add_status_fill_na(item, "Http Error")
        except requests.exceptions.ConnectionError as errc:
            print("Error Connecting:", errc)
            item = _add_status_fill_na(item, "ConnectionError")
        except requests.exceptions.Timeout as errt:
            print("Timeout Error:", errt)
            item = _add_status_fill_na(item, "Timeout")
        except requests.exceptions.RequestException as err:
            print("OOps: Something Else", err)
            item = _add_status_fill_na(item, "Something else")
        results.append(item)
    return results


@click.command()
@click.option('--input', prompt='filename')
@click.option('--output', default='result.csv')
def run_main(input: str, output: str) -> None:
    items = get_csv(input)
    results = add_statuscode(items)
    write_csv(results, output)


if __name__ == '__main__':
    run_main()
