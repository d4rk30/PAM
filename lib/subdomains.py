#coding:utf-8
import requests

HEADERS = {'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'}
SUBS = []

#加载字典
with open('db/wydomain.csv','r') as f:
    for line in f.readlines():
        SUBS.append(line.strip())


#爆破子域名
def search(domain):
    subdomains=[]
    for sub in SUBS:
        try:
            http = 'http://'+sub+'.'+domain
            https = 'https://'+sub+'.'+domain
            r = requests.get(http,headers=HEADERS,timeout=2)
            rs = requests.get(https,headers=HEADERS,timeout=2)
            if r.status_code == 200 or r.status_code ==302:
                if rs.status_code == 200 or rs.status_code ==302:
                    print(https)
                    print(rs.status_code)
                    subdomains.append(https)
                else:
                    print(http)
                    print(r.status_code)
                    subdomains.append(http)
            elif rs.status_code == 200 or rs.status_code ==302:
                print(https)
                print(rs.status_code)
                subdomains.append(https)
        except requests.exceptions.RequestException as e:
            pass
    return subdomains
