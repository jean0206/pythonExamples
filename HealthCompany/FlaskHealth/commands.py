import click
from flask.cli import  with_appcontext

from .extensions import db
from .models import *


@click.command(name='create_tables')
@with_appcontext
def create_tables():
    db.create_all()
    rol = Role(rol_name="Hospital")
    rol1 = Role(rol_name="Paciente")
    rol2 = Role(rol_name="Doctor")
    db.session.add(rol)
    db.session.add(rol1)
    db.session.add(rol2)
    db.session.commit()

