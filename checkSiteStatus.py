import click
import csv
import requests

@click.command()
@click.option('--input', prompt='filename')
@click.option('--output', default='result.csv')
def hello(input, output):
    print(f'inputfile: {input}, outputfile: {output}')
    #read inputfile
    with open(input) as csv_file:
        items = list(csv.DictReader(csv_file))
    print(f'got {len(items)} items, result: {items}')
    # get results with requests
    results = list()
    results = [(item['statuscode']:=requests.get(item['url'])) for item in items]
    for item in items:
        r = requests.get(item['url'])
        item['statuscode'] = r.status_code
        results.append(item)
    print(results)
    # write results to csv
    keys = results[0].keys()
    with open(output, 'w', encoding='utf-8') as file:
        writer = csv.DictWriter(file, keys)
        writer.writeheader()
        writer.writerows(results)
    #return result


if __name__ == '__main__':
    hello()