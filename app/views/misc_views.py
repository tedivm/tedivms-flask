# Copyright 2017 Twin Tech Labs. All rights reserved

from flask import Blueprint, redirect, render_template, current_app
from flask import request, url_for, flash, send_from_directory, jsonify, render_template_string
from flask_user import current_user, login_required, roles_accepted

from app import db
from app.models.user_models import UserProfileForm, User, UsersRoles
import uuid, json, os
import datetime

# When using a Flask app factory we must use a blueprint to avoid needing 'app' for '@app.route'
main_blueprint = Blueprint('main', __name__, template_folder='templates')

# The User page is accessible to authenticated users (users that have logged in)
@main_blueprint.route('/')
def member_page():
    if not current_user.is_authenticated:
        return redirect(url_for('user.login'))

    return render_template('pages/member_base.html')

# The Admin page is accessible to users with the 'admin' role
@main_blueprint.route('/admin')
@roles_accepted('admin')  # Limits access to users with the 'admin' role
def admin_page():
    return render_template('pages/admin_page.html')

@main_blueprint.route('/users')
@roles_accepted('admin')
def user_admin_page():
    users = User.query.all()
    return render_template('pages/admin/users.html',
        users=users)

@main_blueprint.route('/create_user', methods=['GET', 'POST'])
@roles_accepted('admin')
def create_user_page():
    form = UserProfileForm(request.form, obj=current_user)

    if request.method == 'POST':
        user = User.query.filter(User.email == request.form['email']).first()
        if not user:
            user = User(email=request.form['email'],
                        first_name=request.form['first_name'],
                        last_name=request.form['last_name'],
                        password=current_app.user_manager.hash_password(request.form['password']),
                        active=True,
                        confirmed_at=datetime.datetime.utcnow())
            db.session.add(user)
            db.session.commit()
        return redirect(url_for('main.user_admin_page'))
    return render_template('pages/admin/create_user.html',
                           form=form)

@main_blueprint.route('/delete_user', methods=['GET'])
@roles_accepted('admin')
def delete_user_page():
    try:
        user_id = request.args.get('user_id')

        db.session.query(UsersRoles).filter_by(user_id = user_id).delete()
        db.session.query(User).filter_by(id = user_id).delete()
        db.session.commit()

        flash('You successfully deleted your user!', 'success')
        return redirect(url_for('main.user_admin_page'))
    except Exception as e:
        flash('Opps!  Something unexpected happened.  On the brightside, we logged the error and will absolutely look at it and work to correct it, ASAP.', 'error')
        return redirect(request.referrer)

@main_blueprint.route('/pages/profile', methods=['GET', 'POST'])
@login_required
def user_profile_page():
    # Initialize form
    form = UserProfileForm(request.form, obj=current_user)

    # Process valid POST
    if request.method == 'POST' and form.validate():
        # Copy form fields to user_profile fields
        form.populate_obj(current_user)

        # Save user_profile
        db.session.commit()

        # Redirect to home page
        return redirect(url_for('main.user_profile_page'))

    # Process GET or invalid POST
    return render_template('pages/user_profile_page.html',
                           current_user=current_user,
                           form=form)
