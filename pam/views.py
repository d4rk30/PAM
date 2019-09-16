from flask import render_template,redirect,url_for,request,flash
from multiprocessing import Process
from pam import app,db
from pam.models import Project,Domain,Subdomain
from pam.forms import CreateProjectForm,CreateDomainForm
import requests

HEADERS = {'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'}

@app.route('/project/',methods=['GET','POST'])
@app.route('/project',methods=['GET','POST'])
def projectList():
	create_project_form = CreateProjectForm()
	if request.method == 'POST' and create_project_form.validate():
		name = create_project_form.name.data
		describe = create_project_form.describe.data
		project = Project(name = name,describe = describe,domain_count = 0,subdomain_count = 0)
		db.session.add(project)
		db.session.commit()
		return redirect(url_for('projectList'))
	projects = Project.query.all()
	return render_template('index.html',create_project_form=create_project_form,projects = projects)

@app.route('/project/<id>/',methods=['GET','POST'])
@app.route('/project/<id>',methods=['GET','POST'])
def project(id):
	create_domain_form = CreateDomainForm()
	if request.method == 'POST' and create_domain_form.validate():
		domain = Domain(domain = create_domain_form.domain.data)
		db.session.add(domain)
		project = Project.query.filter(Project.id == id).first_or_404()
		project.domains.append(domain)
		project.domain_count = project.domain_count + 1
		db.session.commit()
		p = Process(target=searchSubdomain, args=(domain,project,))
		p.start()
		return redirect(url_for('project',id=id))
	domains = Project.query.get(id).domains
	project = Project.query.get_or_404(id)
	return render_template('project.html',create_domain_form=create_domain_form,domains = domains,project = project)
	
def searchSubdomain(domain,project):
	print(project)
	print(project.subdomain_count)
	with open('dictionary/wydomain.csv','r') as f:
		for sub in f.readlines():
			http = 'http://'+sub.strip()+'.'+domain.domain
			https = 'https://'+sub.strip()+'.'+domain.domain
			try:
				rs = requests.get(https,headers=HEADERS,timeout=2,allow_redirects=False)
				if rs.status_code == 200:
					subdomain = Subdomain(subdomain = https)
					db.session.add(subdomain)
					domain.subdomains.append(subdomain)
					print(project.subdomain_count)
					project.subdomain_count = project.subdomain_count + 1
					db.session.commit()
					print(project.subdomain_count)
					print(https)
				else:
					try:
						r = requests.get(http,headers=HEADERS,timeout=2,allow_redirects=False)
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
					r = requests.get(http,headers=HEADERS,timeout=2,allow_redirects=False)
					if r.status_code == 200:
						subdomain = Subdomain(subdomain = http)
						db.session.add(subdomain)
						domain.subdomains.append(subdomain)
						project.subdomain_count = project.subdomain_count + 1
						db.session.commit()
						print(http)
				except requests.exceptions.RequestException as e:
					pass