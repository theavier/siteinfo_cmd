Python check for status of urls. Returns ip, statuscode

Usage:
/> python checkSiteStatus.py --csv input.csv --output newname.csv

Outputs to --output filename. If now value given, defaults to results.csv

Python check for whois attributes. Returns ['registrant_name', 'expiration_date', 'registrar', 'name_servers'] if available.
Usage:
/> python checkSiteWhois.py --csv input.csv --output newname.csv

Check only one site.
/> python checkSiteWhois.py --input_raw mydomain.com 

Python check for what is running. Returns dict. 
Usage:
/> python checkSitecms.py --csv input.csv --output result_whatis.json

Check it all
/> python siteinfo.py --csv input.csv --output result_siteinfo.json --who_is True --what_is True --status True

