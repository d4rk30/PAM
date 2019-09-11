from datetime import datetime
from pam import db

#数据库模型
class User(db.Model):
	id = db.Column(db.Integer,primary_key = True)
	mail = db.Column(db.String(120),unique = True)
	password = db.Column(db.String(32))
	username = db.Column(db.String(20),unique = True)

	#和Project建立关联关系
	projects = db.relationship('Project')

class Project(db.Model):
	id = db.Column(db.Integer,primary_key = True)
	name = db.Column(db.String(120))
	describe = db.Column(db.String(255))
	domain_count = db.Column(db.Integer)
	subdomain_count = db.Column(db.Integer)
	datetime = db.Column(db.DateTime,default = datetime.now)
	
	#定义外键
	user_id = db.Column(db.Integer,db.ForeignKey('user.id'))

	#和Domain建立关联关系
	domains = db.relationship('Domain')

class Domain(db.Model):
	id = db.Column(db.Integer,primary_key = True)
	domain = db.Column(db.String(255),unique = True)

	#定义外键
	project_id = db.Column(db.Integer,db.ForeignKey('project.id'))

	#与Subdomain建立关联关系
	subdomains = db.relationship('Subdomain')

class Subdomain(db.Model): 
	id = db.Column(db.Integer,primary_key = True)
	subdomain = db.Column(db.String(255),unique = True)
	datetime = db.Column(db.DateTime,default = datetime.now)
	
	#定义外键
	domain_id = db.Column(db.Integer,db.ForeignKey('domain.id'))

	#与SubdomainInfo建立关联关系
	subdomain_infos = db.relationship('SubdomainInfo')

class SubdomainInfo(db.Model):
	id = db.Column(db.Integer,primary_key = True)
	title = db.Column(db.String(255)) #网站名称
	name = db.Column(db.String(255)) #域名注册人
	mail = db.Column(db.String(255)) #域名注册邮箱
	phone = db.Column(db.String(255)) #域名注册手机
	city = db.Column(db.String(255)) #域名注册城市
	ip = db.Column(db.String(100)) 
	country = db.Column(db.String(255)) #IP所属国家
	background = db.Column(db.String(255)) #后台地址
	datetime = db.Column(db.DateTime,default = datetime.now) #更新时间

	#定义外键
	subdomain_id = db.Column(db.Integer,db.ForeignKey('subdomain.id'))

	#与Port建立关联关系
	ports = db.relationship('Port')

	#与WebFingerprint建立关联关系
	web_fingerprints = db.relationship('WebFingerprint')

class Port(db.Model):
	id = db.Column(db.Integer,primary_key = True)
	port = db.Column(db.Integer)
	server = db.Column(db.String(255))
	datetime = db.Column(db.DateTime,default = datetime.now)

	#定义外键
	subdomain_info_id = db.Column(db.Integer,db.ForeignKey('subdomain_info.id'))

class WebFingerprint(db.Model):
	id = db.Column(db.Integer,primary_key = True)
	info = db.Column(db.String(255))
	datetime = db.Column(db.DateTime,default = datetime.now)

	#定义外键
	subdomain_info_id = db.Column(db.Integer,db.ForeignKey('subdomain_info.id'))

