from flask import Flask,render_template,redirect,url_for,request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os,sys
from lib.subdomains import *
from forms import LoginForm,CreateProjectForm,CreateDomainForm

WIN = sys.platform.startswith('win')
if WIN:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(app.root_path, 'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'secret string'

db = SQLAlchemy(app)
migrate = Migrate(app,db)

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
    datetime = db.Column(db.DateTime)
    
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
    datetime = db.Column(db.DateTime)
    
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
    datetime = db.Column(db.DateTime) #更新时间

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
    datetime = db.Column(db.DateTime)

    #定义外键
    subdomain_info_id = db.Column(db.Integer,db.ForeignKey('subdomain_info.id'))

class WebFingerprint(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    info = db.Column(db.String(255))
    datetime = db.Column(db.DateTime)

    #定义外键
    subdomain_info_id = db.Column(db.Integer,db.ForeignKey('subdomain_info.id'))


#操作数据库
def addUser(username = 'Danny'):
    user = User(username = username)
    db.session.add(user)
    db.session.commit()

#创建项目
def createProject(project_name='百度',username = 'Danny'):
    project = Project(name = project_name)
    db.session.add(project)
    user = User.query.filter(User.username == username).first_or_404()
    user.projects.append(project)
    db.session.commit()

#添加域名
def addDomain(domain_url='baidu.com',project_name="百度"):
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

@app.route('/',methods=['GET','POST'])
def index():
    create_project_form = CreateProjectForm()
    if request.method == 'POST' and create_project_form.validate():
        project_name = create_project_form.name.data
        createProject(project_name = project_name)
        return redirect(url_for('index'))
    projects = Project.query.all()
    return render_template('index.html',create_project_form=create_project_form,projects = projects)
    
@app.route('/forms')
def forms():
    form = LoginForm()
    return render_template('test.html',form=form)

    

