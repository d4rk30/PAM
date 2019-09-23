from flask import render_template,redirect,url_for,request,flash
from multiprocessing import Process
from pam import app,db
from pam.models import Project,Domain
from pam.forms import CreateProjectForm,CreateDomainForm
from pam.lib import getSubdomain

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
		p = Process(target=getSubdomain, args=(domain,project,db,))
		p.start()
		return redirect(url_for('project',id=id))
	domains = Project.query.get(id).domains
	project = Project.query.get_or_404(id)
	return render_template('project.html',create_domain_form=create_domain_form,domains = domains,project = project)