Python check for status of urls. Returns ip, statuscode

Usage:
/> python siteinfo.py status lookup --csv input_csv --output results.json

Outputs to --output filename. If no value given, prints results

Python check for whois attributes. Returns ['registrant_name', 'expiration_date', 'registrar', 'name_servers'] if available.
Usage:
/> python siteinfo.py whois lookup --csv input_csv --output results.json

Check only one site.
/> python siteinfo.py whois lookup mydomain.com 

Check for what is running. Returns json 
Usage:
/> python siteinfo.py whatis --csv input.csv --output results.json

Check ip address resolves to
/> python siteinfo.py status --csv input.csv --output results.json

Check it all
/> python siteinfo.py lookup --csv input.csv --output results.json 

Check params
/> python siteinfo.py --help
/> python siteinfo.py whatis --help
/> python siteinfo.py whois --help
/> python siteinfo.py status --help
