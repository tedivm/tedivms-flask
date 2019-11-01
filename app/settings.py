# Settings common to all environments (development|staging|production)
# Place environment specific settings in env_settings.py
# An example file (env_settings_example.py) can be used as a starting point

import os

# Application settings
APP_NAME = "Flask Starter"
APP_SYSTEM_ERROR_SUBJECT_LINE = APP_NAME + " system error"
APP_OWNER_NAME = "Change this in settings."

# Flask settings
CSRF_ENABLED = True
SECRET_KEY = None

# Flask-SQLAlchemy settings
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = 'sqlite:///app.sqlite'

# Celery Configuration
CELERY_BROKER = False
CELERY_RESULTS = False

# Cache
CACHE_TYPE = False
CACHE_ROOT = False
CACHE_URL = False



# Flask-User settings
USER_APP_NAME = APP_NAME
USER_ENABLE_CHANGE_PASSWORD = True  # Allow users to change their password
USER_ENABLE_CHANGE_USERNAME = False  # Allow users to change their username
USER_ENABLE_CONFIRM_EMAIL = True  # Force users to confirm their email
USER_ENABLE_FORGOT_PASSWORD = True  # Allow users to reset their passwords
USER_ENABLE_EMAIL = True  # Register with Email
USER_ENABLE_REGISTRATION = True  # Allow new users to register
USER_REQUIRE_RETYPE_PASSWORD = True  # Prompt for `retype password` in:
USER_ENABLE_USERNAME = False  # Register and Login with username
USER_AFTER_LOGIN_ENDPOINT = 'main.member_page'
USER_AFTER_LOGOUT_ENDPOINT = 'main.member_page'
USER_ALLOW_LOGIN_WITHOUT_CONFIRMED_EMAIL = False


USER_LDAP = False
LDAP_HOST=False
LDAP_BIND_DN=False
LDAP_BIND_PASSWORD=False
LDAP_USERNAME_ATTRIBUTE=False
LDAP_USER_BASE=False
LDAP_USER_OBJECT_CLASS = False
LDAP_GROUP_OBJECT_CLASS=False
LDAP_GROUP_ATTRIBUTE=False
LDAP_GROUP_BASE=False
LDAP_GROUP_TO_ROLE_ADMIN=False
LDAP_GROUP_TO_ROLE_DEV=False
LDAP_GROUP_TO_ROLE_USER=False
LDAP_EMAIL_ATTRIBUTE=False


# Flask-Mail settings
# For smtp.gmail.com to work, you MUST set "Allow less secure apps" to ON in Google Accounts.
# Change it in https://myaccount.google.com/security#connectedapps (near the bottom).
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 587
MAIL_USE_SSL = False
MAIL_USE_TLS = True
MAIL_USERNAME = 'you@gmail.com'
MAIL_PASSWORD = 'yourpassword'
MAIL_DEFAULT_SENDER = '"You" <you@gmail.com>'
ADMINS = [
    '"Admin One" <admin1@gmail.com>',
    ]
