Python check for status of urls. Returns ip, statuscode

Usage:
/> python checkSiteStatus.py --input_file input.csv --output newname.csv

Outputs to --output filename. If now value given, defaults to results.csv

Python check for whois attributes. Returns ['registrant_name', 'expiration_date', 'registrar', 'name_servers'] if available.
Usage:
/> python checkSiteWhois.py --csv input.csv --output newname.csv


Check only one site.
/> python checkSiteWhois.py --input_raw mydomain.com 

Python check for what is running. Returns json. 
Usage:
/> python checkSitecms.py --input input.csv --output result_whatis.json

