# This file defines command line commands for manage.py
#
# Copyright 2014 SolidBuilds.com. All rights reserved
#
# Authors: Ling Thio <ling.thio@gmail.com>

import datetime

from flask import current_app

from app import db
from app.models.user_models import User, Role


def find_or_create_role(name, label):
    """ Find existing role or create new role """
    role = Role.query.filter(Role.name == name).first()
    if not role:
        role = Role(name=name, label=label)
        db.session.add(role)
        db.session.commit()
    return role


def find_or_create_user(first_name, last_name, username, email, password, role=None):
    """ Find existing user or create new user """
    if username:
        user = User.query.filter(User.username == username).first()
    else:
        user = User.query.filter(User.email == email).first()

    if not user:
        user = User(email=email,
                    first_name=first_name,
                    last_name=last_name,
                    password=current_app.user_manager.hash_password(password),
                    active=True,
                    email_confirmed_at=datetime.datetime.utcnow())
        if role:
            user.roles.append(role)
        db.session.add(user)
        db.session.commit()
    return user
