#coding:utf-8
import requests
HEADERS = {'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'}
with open('../dictionary/wydomain.csv','r') as f:
	for sub in f.readlines():
		object_request = None
		http = 'http://'+sub.strip()+'.'+'mju.edu.cn'
		https = 'https://'+sub.strip()+'.'+'mju.edu.cn'
		try:
			rs = requests.get(https,headers=HEADERS,timeout=2,allow_redirects=False)
			if rs.status_code == 200:
				print("子域："+sub.strip()+',存在，协议为https')
			else:
				try:
					r = requests.get(http,headers=HEADERS,timeout=2,allow_redirects=False)
					if r.status_code == 200:
						print("子域："+sub.strip()+',存在，协议为http')
				except requests.exceptions.RequestException as e:
					pass
		except requests.exceptions.RequestException as e:
			try:
				
					print("子域："+sub.strip()+',存在，协议为http')
			except requests.exceptions.RequestException as e:
				pass
