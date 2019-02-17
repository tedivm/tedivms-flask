from flask import Blueprint
from wtforms.fields import HiddenField


jinja_extensions_blueprint = Blueprint('jinja_extensions_blueprint', __name__, template_folder='templates')


@jinja_extensions_blueprint.app_template_filter()
def filesize_format(num):
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    return '%.0f%s' % (num, ['', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB'][magnitude])


@jinja_extensions_blueprint.app_template_global
def is_hidden_field_filter(field):
    return isinstance(field, HiddenField)
