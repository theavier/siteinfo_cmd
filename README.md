Python check for status of urls. Returns ip, statuscode

Usage:
/> python siteinfo.py --csv input_csv --output results.json status 

Outputs to --output filename. If no value given, prints results

Python check for whois attributes. Returns ['registrant_name', 'expiration_date', 'registrar', 'name_servers'] if available.
Usage:
/> python siteinfo.py --csv input_csv --output results.json whois 

Check only one site.
/> python siteinfo.py whois mydomain.com 

Check for what is running. Returns json 
Usage:
/> python siteinfo.py --csv input.csv --output results.json whatis 

Check ip address resolves to
/> python siteinfo.py --csv input.csv --output results.json status 

Check it all
/> python siteinfo.py --csv input.csv --output results.json all  

Check params
/> python siteinfo.py --help
/> python siteinfo.py whatis --help
/> python siteinfo.py whois --help
/> python siteinfo.py status --help
