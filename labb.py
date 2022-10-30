from checkSiteWhois import whois_domain_items
from checkSiteCMS import whatis_items, whatis_item
from checkSiteStatus import add_statuscode
#from checkSiteStatus import get_csv
from tools import get_csv, get_csv_asjson, merge_list_dicts

#test
csv = "C:\code\siteinfo_cmd\dnslistan_test_small.csv"
items = get_csv(csv)
#print(f'type: {type(items)}, items: {items}')

#results = whois_domain_items(items)
#print(f'type: {type(results)}, items: {results}')
#items2 = get_csv(csv)
#results_code = add_statuscode(items2)
#print(f'type: {type(results_code)}, itemscode: {results_code}')

#results_whatis = whatis_items(items)
#print(f'whatis results: {type(results_whatis)}, content: {results_whatis}')

results_whatis = whatis_item(items[1])
print(f'whatis results: {type(results_whatis)}, content: {results_whatis}')

#combine values
#result = merge_list_dicts(results, items2, "url")
#print(f'merged_results: {result}, type: {type(result)}')