
from flask import current_app, g
from flask_login import current_user
from flask_user import UserManager
from flask_user.forms import LoginForm
from flask_user.translation_utils import lazy_gettext as _    # map _() to lazy_gettext()

import datetime
from ldap3 import Server, Connection, ALL
from app import db
from app.models import user_models


def authenticate(user, password):
    # define the server
    s = Server(current_app.config['LDAP_HOST'], get_info=ALL)  # define an unsecure LDAP server, requesting info on DSE and schema

    # define the connection
    user_dn = get_dn_from_user(user)
    c = Connection(current_app.config['LDAP_HOST'], user=user_dn, password=password)

    # perform the Bind operation - used to check user password.
    if not c.bind():
        print('Unable to bind user %s' % (user_dn))
        return False

    # check to see if user is actually a valid user.
    return True


def get_user_email(user):
    email_attribute = current_app.config.get('LDAP_EMAIL_ATTRIBUTE', False)
    if not email_attribute:
        return False
    conn = get_bound_connection()
    user_search = get_dn_from_user(user)
    user_object = '(objectclass=%s)' % (current_app.config['LDAP_USER_OBJECT_CLASS'],)
    conn.search(user_search, user_object, attributes=[email_attribute])
    if len(conn.entries) < 1:
        return False
    return getattr(conn.entries[0], email_attribute, False)[0]


def user_in_group(user, group):
    conn = get_bound_connection()
    group_search = get_dn_from_group(group)
    group_object = '(objectclass=%s)' % (current_app.config['LDAP_GROUP_OBJECT_CLASS'],)
    conn.search(group_search, group_object, attributes=['memberUid'])
    if len(conn.entries) < 1:
        return False
    members = conn.entries[0].memberUid
    return user in members


def get_bound_connection():
    if 'ldap_connection' in g:
        return g.ldap_connection
    server = Server(current_app.config['LDAP_HOST'], get_info=ALL)  # define an unsecure LDAP server, requesting info on DSE and schema
    g.ldap_connection = Connection(server, current_app.config['LDAP_BIND_DN'], current_app.config['LDAP_BIND_PASSWORD'], auto_bind=True)
    return g.ldap_connection


def get_dn_from_user(user):
    return "%s=%s,%s" % (current_app.config['LDAP_USERNAME_ATTRIBUTE'], user, current_app.config['LDAP_USER_BASE'] )


def get_dn_from_group(group):
    return '%s=%s,%s' % (current_app.config['LDAP_GROUP_ATTRIBUTE'], group, current_app.config['LDAP_GROUP_BASE'])


class TedivmLoginForm(LoginForm):

    def validate_user(self):
        user_manager =  current_app.user_manager
        if current_app.config.get('USER_LDAP', False):
            if not authenticate(self.username.data, self.password.data):
                return False
            user = user_manager.db_manager.find_user_by_username(self.username.data)
            if not user:
                email = get_user_email(self.username.data)
                if not email:
                    email = None

                user = user_models.User(username=self.username.data,
                            email=email,
                            #first_name=form.first_name.data,
                            #last_name=form.last_name.data,
                            #password=current_app.user_manager.hash_password(form.password.data),
                            active=True,
                            email_confirmed_at=datetime.datetime.utcnow())
                db.session.add(user)
                db.session.commit()
            return True



        # Find user by username and/or email
        user = None
        user_email = None
        if user_manager.USER_ENABLE_USERNAME:
            # Find user by username
            user = user_manager.db_manager.find_user_by_username(self.username.data)

            # Find user by email address (username field)
            if not user and user_manager.USER_ENABLE_EMAIL:
                user, user_email = user_manager.db_manager.get_user_and_user_email_by_email(self.username.data)

        else:
            # Find user by email address (email field)
            user, user_email = user_manager.db_manager.get_user_and_user_email_by_email(self.email.data)

        # Handle successful authentication
        if user and user_manager.verify_password(self.password.data, user.password):
            return True                         # Successful authentication



    def validate(self):
        # Remove fields depending on configuration
        user_manager =  current_app.user_manager
        if user_manager.USER_ENABLE_USERNAME:
            delattr(self, 'email')
        else:
            delattr(self, 'username')

        # Validate field-validators
        if not super(LoginForm, self).validate():
            return False

        if self.validate_user():
            return True

        # Handle unsuccessful authentication
        # Email, Username or Email/Username depending on settings
        if user_manager.USER_ENABLE_USERNAME and user_manager.USER_ENABLE_EMAIL:
            username_or_email_field = self.username
            username_or_email_text = (_('Username/Email'))
        elif user_manager.USER_ENABLE_USERNAME:
            username_or_email_field = self.username
            username_or_email_text = (_('Username'))
        else:
            username_or_email_field = self.email
            username_or_email_text = (_('Email'))

        # Always show 'incorrect username/email or password' error message for additional security
        message = _('Incorrect %(username_or_email)s and/or Password', username_or_email=username_or_email_text)
        username_or_email_field.errors.append(message)
        self.password.errors.append(message)

        return False                                # Unsuccessful authentication



# Customize Flask-User
class TedivmUserManager(UserManager):
    def customize(self, app):
        self.LoginFormClass = TedivmLoginForm
