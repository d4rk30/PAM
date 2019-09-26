import click
from pam import app,db

@app.cli.command()
def initdb():
	"""reset db."""
	db.drop_all()
	db.create_all()