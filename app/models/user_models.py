# Copyright 2014 SolidBuilds.com. All rights reserved
#
# Authors: Ling Thio <ling.thio@gmail.com>, Matt Hogan <matt@twintechlabs.io>

from flask import current_app
from flask_user import UserMixin
from flask_user.forms import RegisterForm
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, validators, PasswordField, BooleanField
from app import db
from app.utils.forms import MultiCheckboxField
from app.extensions import ldap


class TedivmUserMixin(UserMixin):

    def has_roles(self, *requirements):
        """ Return True if the user has all of the specified roles. Return False otherwise.

            has_roles() accepts a list of requirements:
                has_role(requirement1, requirement2, requirement3).

            Each requirement is either a role_name, or a tuple_of_role_names.
                role_name example:   'manager'
                tuple_of_role_names: ('funny', 'witty', 'hilarious')
            A role_name-requirement is accepted when the user has this role.
            A tuple_of_role_names-requirement is accepted when the user has ONE of these roles.
            has_roles() returns true if ALL of the requirements have been accepted.

            For example:
                has_roles('a', ('b', 'c'), d)
            Translates to:
                User has role 'a' AND (role 'b' OR role 'c') AND role 'd'"""

        # Translates a list of role objects to a list of role_names
        user_manager = current_app.user_manager

        # has_role() accepts a list of requirements
        for requirement in requirements:
            if isinstance(requirement, (list, tuple)):
                # this is a tuple_of_role_names requirement
                tuple_of_role_names = requirement
                authorized = False
                for role_name in tuple_of_role_names:
                    if self.has_role(role_name):
                        # tuple_of_role_names requirement was met: break out of loop
                        authorized = True
                        break
                if not authorized:
                    return False                    # tuple_of_role_names requirement failed: return False
            else:
                # this is a role_name requirement
                role_name = requirement
                # the user must have this role
                if self.has_role(role_name):
                    return False                    # role_name requirement failed: return False

        # All requirements have been met: return True
        return True




# Define the User data model. Make sure to add the flask_user.UserMixin !!
class User(db.Model, TedivmUserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)

    # User authentication information (required for Flask-User)
    username = db.Column(db.String(50), nullable=True, unique=True)
    email = db.Column(db.Unicode(255), nullable=True, unique=True)
    email_confirmed_at = db.Column(db.DateTime())
    password = db.Column(db.String(255), nullable=False, server_default='')

    # User information
    active = db.Column('is_active', db.Boolean(), nullable=False, server_default='0')
    first_name = db.Column(db.Unicode(50), nullable=False, server_default=u'')
    last_name = db.Column(db.Unicode(50), nullable=False, server_default=u'')

    # Relationships
    roles = db.relationship('Role', secondary='users_roles', backref=db.backref('users', lazy='dynamic'))

    # API Keys
    apikeys = db.relationship('ApiKey', backref='user')

    def has_role(self, role, allow_admin=True):

        if current_app.config.get('USER_LDAP', False):
            group = current_app.config.get('LDAP_GROUP_TO_ROLE_%s' % role.upper(), False)
            if not group:
                return False
            return ldap.user_in_group(self.username, group)

        for item in self.roles:
            if item.name == role:
                return True
            if allow_admin and item.name == 'admin':
                return True
        return False

    def role(self):
        for item in self.roles:
            return item.name

    def name(self):
        return self.first_name + " " + self.last_name



class ApiKey(db.Model):
    __tablename__ = 'api_keys'
    id = db.Column(db.Unicode(255), primary_key=True, unique=True)
    hash = db.Column(db.Unicode(255), nullable=False)
    label = db.Column(db.Unicode(255), nullable=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'))


# Define the Role data model
class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), nullable=False, server_default=u'', unique=True)  # for @roles_accepted()
    label = db.Column(db.Unicode(255), server_default=u'')  # for display purposes


# Define the UserRoles association model
class UsersRoles(db.Model):
    __tablename__ = 'users_roles'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer(), db.ForeignKey('roles.id', ondelete='CASCADE'))


# Define the User registration form
# It augments the Flask-User RegisterForm with additional fields
class MyRegisterForm(RegisterForm):
    first_name = StringField('First name', validators=[ validators.DataRequired('First name is required')])
    last_name = StringField('Last name', validators=[ validators.DataRequired('Last name is required')])


# Define the User profile form
class UserProfileForm(FlaskForm):
    first_name = StringField('First name', validators=[])
    last_name = StringField('Last name', validators=[])
    email = StringField('Email', validators=[validators.DataRequired('Last name is required')])
    password = PasswordField('Password', validators=[])
    roles = MultiCheckboxField('Roles', coerce=int)
    active = BooleanField('Active')
    submit = SubmitField('Save')



# Define the User profile form
class ApiKeyForm(FlaskForm):
    label = StringField('Key Label', validators=[validators.DataRequired('Key Label is required')])
    submit = SubmitField('Save')
