import csv
import json
from loguru import logger
import sys


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


def save_or_print(results: list, output: str = None):
    logger.debug(f' output: {output}, type: {type(output)}')
    if output:
        logger.info(f'Saved file to {output}')
        write_json(results, output)
        #write_csv(results, output)
    else:
        logger.debug(f'Printing results...')
        print(results)


def list_or_item(url: str = None, _csv: str = None) -> list:
    """ if csv it set, return that else make list of url-string """
    if _csv:
        logger.debug(f'csv param used: {_csv}')
        items = get_csv(_csv)
    else:
        logger.debug(f'no csv param used: {url}')
        items = [{'url': url}]
    return items


def log_remove_verbose() -> None:
    """ Sets minimum loglevel on loguru """
    logger.remove()
    logger.add(sys.stderr, level='INFO')


def log_init(verbose: bool, logname: str = "log.log") -> None:
    """ Checks if verbose is set and sets loglevel accordingly """
    if verbose is not True:
        log_remove_verbose()
    logger.add(logname)
