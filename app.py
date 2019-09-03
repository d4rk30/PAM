from flask import Flask,render_template
from flask_sqlalchemy import SQLAlchemy
import os,sys
from lib.subdomains import *

WIN = sys.platform.startswith('win')
if WIN:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(app.root_path, 'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

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
    
    #定义外键
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))

    #和Domain建立关联关系
    domains = db.relationship('Domain')

class Domain(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    url = db.Column(db.String(255))

    #定义外键
    project_id = db.Column(db.Integer,db.ForeignKey('project.id'))

    #与Subdomain建立关联关系
    subdomains = db.relationship('Subdomain')

class Subdomain(db.Model): 
    id = db.Column(db.Integer,primary_key = True)
    url = db.Column(db.String(255))
    
    #定义外键
    domain_id = db.Column(db.Integer,db.ForeignKey('domain.id'))

    #与SubdomainInfo建立关联关系
    subdomaininfos = db.relationship('SubdomainInfo')

class SubdomainInfo(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(255))
    mail = db.Column(db.String(255))
    phone = db.Column(db.String(255))
    city = db.Column(db.String(255))
    ip = db.Column(db.String(100))
    country = db.Column(db.String(255))
    background = db.Column(db.String(255))
    updatetime = db.Column(db.DateTime)

    #定义外键
    subdomain_id = db.Column(db.Integer,db.ForeignKey('subdomain.id'))

    #与Port建立关联关系
    ports = db.relationship('Port')

    #与WebFingerprint建立关联关系
    webfingerprints = db.relationship('WebFingerprint')

class Port(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    port = db.Column(db.Integer)
    server = db.Column(db.String(255))
    updatetime = db.Column(db.DateTime)

    #定义外键
    subdomain_info_id = db.Column(db.Integer,db.ForeignKey('subdomain_info.id'))

class WebFingerprint(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    info = db.Column(db.String(255))
    uodatetime = db.Column(db.DateTime)

    #定义外键
    subdomain_info_id = db.Column(db.Integer,db.ForeignKey('subdomain_info.id'))


#操作数据库
#创建项目
def createProject(project_name,username):
    project = Project(name = project_name)
    db.session.add(project)
    user = User.query.filter(User.username == username).first_or_404()
    user.projects.append(project)
    db.session.commit()

#添加域名
def addDomain(domain_url,project_name):
    domain = Domain(url = domain_url)
    db.session.add(domain)
    project = Project.query.filter(Project.name == project_name).first_or_404()
    project.domains.append(domain)
    db.session.commit()

#添加子域
def addSubdomain(subdomain_url,domain_url):
    subdomain = Subdomain(url = subdomain_url)
    db.session.add(subdomain)
    domain = Domain.query.filter(Domain.url == domain_url).first_or_404()
    domain.subdomains.append(subdomain)
    db.session.commit()

#添加域名视图函数
def addview():
    addDomain('baidu.com','baidu')
    subdomains=search('baidu.com')
    for subdomain in subdomains:
        addSubdomain(subdomain,'baidu.com')



@app.route('/')
def index():
    subdomains = Subdomain.query.all()
    return render_template('index.html',subdomains = subdomains)

