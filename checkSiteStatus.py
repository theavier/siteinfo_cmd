import click
import csv
import requests


def get_csv(_input):
    with open(_input) as csv_file:
        items = list(csv.DictReader(csv_file))
    return items


def write_csv(_items: list, output: str) -> None:
    keys = _items[0].keys()
    print(f'items: {_items}')
    with open(output, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, keys)
        writer.writeheader()
        writer.writerows(_items)


def add_statuscode(_items: list) -> list:
    results = list()
    for item in _items:
        r = requests.get(item['url'], stream=True)
        ip = r.raw._connection.sock.getpeername()[0]
        item['statuscode'] = r.status_code
        item['ip'] = ip
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
