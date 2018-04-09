# Copyright 2018 Twin Tech Labs. All rights reserved

from flask import Blueprint, redirect, render_template
from flask import request, url_for, flash, send_from_directory, jsonify, render_template_string
from flask_user import current_user, login_required, roles_accepted

from app import db
from app.models.user_models import UserProfileForm
import uuid, json, os
import datetime

# When using a Flask app factory we must use a blueprint to avoid needing 'app' for '@app.route'
api_blueprint = Blueprint('api', __name__, template_folder='templates')

@api_blueprint.route('/sample_call', methods=['POST'])
def sample_page():

    ret = {"sample return": 10}
    return(jsonify(ret), 200)
