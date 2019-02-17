# Copyright 2018 Twin Tech Labs. All rights reserved

from flask import Blueprint, redirect
from flask import request, url_for, jsonify, current_app

from app import db
from app.models import user_models
from app.utils.api import roles_accepted_api
from app.extensions.ldap import authenticate

import uuid

# When using a Flask app factory we must use a blueprint to avoid needing 'app' for '@app.route'
api_blueprint = Blueprint('api', __name__, template_folder='templates')

@api_blueprint.route('/api/credentials', methods=['POST'])
def api_create_credentials():
    username = request.form['username']
    password = request.form['password']
    label = request.form.get('label', None)
    user = user_models.User.query.filter(user_models.User.email == username).first()
    if not user:
        user = user_models.User.query.filter(user_models.User.username == username).first()
        if not user:
            abort(400)

    if current_app.config.get('USER_LDAP', False):
        if not authenticate(username, password):
            abort(401)
    else:
        if not current_app.user_manager.verify_password(password, user.password):
            abort(401)

    id = uuid.uuid4().hex[0:12]
    key = uuid.uuid4().hex
    hash = current_app.user_manager.hash_password(key)
    new_key = user_models.ApiKey(id=id, hash=hash, user_id=user.id, label=label)
    db.session.add(new_key)
    db.session.commit()

    return jsonify({'id': id,'key': key})
