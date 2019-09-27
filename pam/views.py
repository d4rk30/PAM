from flask import render_template,redirect,url_for,request,flash
from multiprocessing import Process
from pam import app,db
from pam.models import Project,Domain
from pam.forms import CreateProjectForm,CreateDomainForm
from pam.lib import getSubdomain

@app.route('/index/',methods=['GET','POST'])
@app.route('/index',methods=['GET','POST'])
@app.route('/',methods=['GET','POST'])
def index():
	return render_template('index.html')

@app.route('/home/',methods=['GET','POST'])
@app.route('/home',methods=['GET','POST'])
def home():
	return render_template('home.html')

@app.route('/project/',methods=['GET','POST'])
@app.route('/project',methods=['GET','POST'])
def project():
	create_project_form = CreateProjectForm()
	if request.method == 'POST' and create_project_form.validate():
		name = create_project_form.name.data
		describe = create_project_form.describe.data
		project = Project(name = name,describe = describe,domain_count = 0,subdomain_count = 0)
		db.session.add(project)
		db.session.commit()
		return redirect(url_for('project'))
	page = request.args.get('page',1,type=int) #查询字符串获取当前页数
	per_page = 20 #每页数量
	pagination = Project.query.paginate(page,per_page = per_page) #分页对象
	projects = pagination.items #当前页数记录的列表
	return render_template('project.html',create_project_form=create_project_form,projects = projects,pagination = pagination)

@app.route('/project/<id>/',methods=['GET','POST'])
@app.route('/project/<id>',methods=['GET','POST'])
def item(id):
	create_domain_form = CreateDomainForm()
	if request.method == 'POST' and create_domain_form.validate():
		domain = Domain(domain = create_domain_form.domain.data)
		db.session.add(domain)
		project = Project.query.filter(Project.id == id).first_or_404()
		project.domains.append(domain)
		project.domain_count = project.domain_count + 1
		db.session.commit()
		p = Process(target=getSubdomain, args=(domain,project,db,))
		p.start()
		return redirect(url_for('item',id=id))
	domains = Project.query.get(id).domains
	project = Project.query.get_or_404(id)
	return render_template('item.html',create_domain_form=create_domain_form,domains = domains,project = project)