import requests
from bs4 import BeautifulSoup
from pam.models import Subdomain,SubdomainInfo

# 关闭未受信的证书提示
requests.packages.urllib3.disable_warnings()

HEADERS = {'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'}

def getSubdomain(domain,project,db):
	with open('dictionary/wydomain.csv','r') as f:
		for sub in f.readlines():
			http = 'http://'+sub.strip()+'.'+domain.domain
			https = 'https://'+sub.strip()+'.'+domain.domain
			try:
				rs = requests.get(https,headers=HEADERS,timeout=2,allow_redirects=False,verify=False)
				if rs.status_code == 200:
					subdomain = Subdomain(subdomain = https)
					db.session.add(subdomain)
					domain.subdomains.append(subdomain)
					project.subdomain_count = project.subdomain_count + 1
					db.session.commit()
#					TODO获取网站Title
					rs.encoding="utf-8"
					soup = BeautifulSoup(rs.text,'lxml')
					print(https)
					print(soup.title)
				else:
					try:
						r = requests.get(http,headers=HEADERS,timeout=2,allow_redirects=False,verify=False)
						if r.status_code == 200:
							subdomain = Subdomain(subdomain = http)
							db.session.add(subdomain)
							domain.subdomains.append(subdomain)
							project.subdomain_count = project.subdomain_count + 1
							db.session.commit()
							print(http)
					except requests.exceptions.RequestException as e:
						pass
			except requests.exceptions.RequestException as e:
				try:
					r = requests.get(http,headers=HEADERS,timeout=2,allow_redirects=False,verify=False)
					if r.status_code == 200:
						subdomain = Subdomain(subdomain = http)
						db.session.add(subdomain)
						domain.subdomains.append(subdomain)
						project.subdomain_count = project.subdomain_count + 1
						db.session.commit()
						print(http)
				except requests.exceptions.RequestException as e:
					pass

def getTitle():
	pass

def getName():
	pass
	
def getMail():
	pass

def getPhone():
	pass
	
def getCity():
	pass

def getIP():
	pass
	
def getCountry():
	pass  

def getBackground():
	pass