from flask import Blueprint, redirect, render_template, current_app
from flask import request, url_for, flash, send_from_directory, jsonify, render_template_string
from flask_user import current_user, login_required, roles_accepted

from flask import Flask, session, redirect, url_for, request, render_template, jsonify, abort
from app import db
from app.models import user_models as users
from app.utils import forms

import time
import uuid


# When using a Flask app factory we must use a blueprint to avoid needing 'app' for '@apikeys_blueprint.route'
apikeys_blueprint = Blueprint('apikeys', __name__, template_folder='templates')


@apikeys_blueprint.route('/user/apikeys')
@roles_accepted('dev', 'admin')
def apikeys_index():
    all_keys = users.ApiKey.query.filter_by(user_id=current_user.id).all()
    return render_template("apikeys/list.html", keys=all_keys)


@apikeys_blueprint.route('/user/create_apikey', methods=['GET', 'POST'])
@roles_accepted('dev', 'admin')
def apikeys_create():
    form = users.ApiKeyForm(request.form)
    if request.method == 'POST' and form.validate():
        label = request.form.get('label', None)
        id = uuid.uuid4().hex[0:12]
        key = uuid.uuid4().hex
        hash = current_app.user_manager.hash_password(key)
        new_key = users.ApiKey(id=id, hash=hash, user_id=current_user.id, label=label)
        db.session.add(new_key)
        db.session.commit()
        return render_template("apikeys/newkey.html", id=id, key=key, label=label)
    return render_template("apikeys/create.html", form=form)


@apikeys_blueprint.route('/user/apikeys/<key_id>/delete', methods=['GET', 'POST'])
@roles_accepted('dev', 'admin')
def apikeys_delete(key_id):
    form = forms.ConfirmationForm(request.form)
    if request.method == 'POST':
        remove_key = users.ApiKey.query.filter_by(id=key_id, user_id=current_user.id).first()
        if remove_key:
            db.session.delete(remove_key)
            db.session.commit()
        return redirect(url_for('apikeys.apikeys_index'))
    return render_template("apikeys/delete.html", form=form, key_id=key_id)
