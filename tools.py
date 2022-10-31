import csv
import json
from loguru import logger


def get_csv(_input: str) -> list:
    """ imports csv content, returns list"""
    with open(_input) as csv_file:
        items = list(csv.DictReader(csv_file))
        return items


def write_csv(_items: list, output: str) -> None:
    """ outputs changes to csv """
    keys = _items[0].keys()
    logger.info(f'items: {_items}')
    with open(output, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, keys)
        writer.writeheader()
        writer.writerows(_items)


def write_json(items: list, output) -> None:
    with open(output, 'w') as outfile:
        json.dump(items, outfile)


def get_csv_asjson(_input: str):
    with open(_input) as csv_file:
        items = list(csv.DictReader(csv_file))
        results = json.dumps(items, indent=2)
    return results


def merge_dicts(first: dict, second: dict, key: str):
    """ merge two dicts into one based on key value"""
    output_dict = dict()
    for dct in first, second:
        output_dict.setdefault(dct[key], dict()).update(dct)
    return list(output_dict.values())[0]


def merge_list_dicts(first: list, second: list, key: str) -> list:
    """ merge two lists of dicts based on key value """
    if not first:
        return second
    elif not second:
        return first
    results = list()
    for item in first:
        second_match = [i for i in second if i[key] == item[key]]
        if second_match:
            results.append(merge_dicts(item, second_match[0], key))
        else:
            results.append(item)
    return results
