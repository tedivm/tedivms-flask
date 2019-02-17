"""This file sets up a command line manager.

Use "python manage.py" for a list of available commands.
Use "python manage.py runserver" to start the development web server on localhost:5000.
Use "python manage.py runserver --help" for additional runserver options.
"""

from flask import Flask
#from flask_migrate import MigrateCommand
from flask.cli import FlaskGroup

import click

from app import create_app

from app.commands import user


@click.group(cls=FlaskGroup, create_app=create_app)
@click.pass_context
def cli(ctx):
    """Management script for the Wiki application."""
    if ctx.parent:
        click.echo(ctx.parent.get_help())

@cli.command(help='Add a User')
@click.argument('username')
@click.argument('email')
@click.argument('password', required=False)
@click.argument('role', required=False, default=None)
@click.option('-f', '--firstname', default='')
@click.option('-l', '--lastname', default='')
@click.option('-s', '--secure', is_flag=True, default=False, help='Set password with prompt without it appearing on screen')
def add_user(username, email, password, role, firstname, lastname, secure):
    if not password and secure:
        password = click.prompt('Password', hide_input=True, confirmation_prompt=True)
    if not password:
        raise click.UsageError("Password must be provided for the user")
    user_role = None
    if role:
        user_role = user.find_or_create_role(role, role)
    user.find_or_create_user(firstname, lastname, username, email, password, user_role)


@cli.command(help='Add a Role')
@click.argument('name')
@click.argument('label', required=False)
def add_role(name, label):
    if not label:
        label = name
    user.find_or_create_role(name, label)



@cli.command(help='Change the password of a user')
@click.argument('email')
@click.argument('password', required=False)
@click.option('-s', '--secure', is_flag=True, default=False, help='Set password with prompt without it appearing on screen')
def reset_password(email, password, secure):
    if not password and secure:
        password = click.prompt('Password', hide_input=True, confirmation_prompt=True)
    if not password:
        raise click.UsageError("Password must be provided for the user")

    user = User.query.filter(User.email == email).first()
    if not user:
        raise click.UsageError("User does not exist")

    user.password = current_app.user_manager.hash_password(password)
    db.session.commit()




if __name__ == "__main__":
    cli()
