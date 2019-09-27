from flask_wtf import FlaskForm
from wtforms import Form,StringField,PasswordField,BooleanField,SubmitField
from wtforms.validators import DataRequired,Length

class LoginForm(FlaskForm):
	username = StringField('Username',validators = [DataRequired()])
	password = PasswordField('Password',validators = [DataRequired(),Length(8,128)])
	remember = BooleanField('Remember me')
	submit = SubmitField('Log in')
	
class CreateProjectForm(FlaskForm):
	name = StringField('Project Name',render_kw = {'class':'form-control'},validators = [DataRequired()])
	describe = StringField('Describe',render_kw = {'class':'form-control'},validators = [DataRequired()])
	submit = SubmitField('Create',render_kw = {'class':'btn btn-bluegreen'})
	
class CreateDomainForm(FlaskForm):
	domain = StringField('Domain',validators = [DataRequired()])
	submit = SubmitField('Create')