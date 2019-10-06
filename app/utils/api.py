from app.models import user_models as users
from functools import wraps
from flask import request, abort, current_app


def is_authorized_api_user(roles=False):
    """Verify API Token and its owners permission to use it"""
    if 'API_ID' not in request.headers:
        return False
    if 'API_KEY' not in request.headers:
        return False
    api_key = users.ApiKey.query.filter(users.ApiKey.id==request.headers['API_ID']).first()
    if not api_key:
        return False
    if not current_app.user_manager.verify_password(request.headers['API_KEY'], api_key.hash):
        return False
    if not roles:
        return True
    if api_key.user.has_role('admin'):
        return True
    for role in roles:
        if api_key.user.has_role(role):
            return True
    return False


def roles_accepted_api(*role_names):
    def wrapper(view_function):
        @wraps(view_function)
        def decorated_view_function(*args, **kwargs):
            if not is_authorized_api_user(role_names):
                return abort(403)
            return view_function(*args, **kwargs)
        return decorated_view_function
    return wrapper


def api_credentials_required():
    def wrapper(view_function):
        @wraps(view_function)
        def decorated_view_function(*args, **kwargs):
            if not is_authorized_api_user():
                return abort(403)
            return view_function(*args, **kwargs)
        return decorated_view_function
    return wrapper
