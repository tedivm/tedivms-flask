from flask import Blueprint
from wtforms.fields import HiddenField
from jinja2 import evalcontextfilter, Markup
import re

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


@jinja_extensions_blueprint.app_template_filter()
@evalcontextfilter
def nl2br(eval_ctx, value):
    """Converts newlines into <p> and <br />s."""
    normalized_value = re.sub(r'\r\n|\r|\n', '\n', value) # normalize newlines
    html_value = normalized_value.replace('\n', '\n<br />\n')
    if eval_ctx.autoescape:
        return Markup(html_value)
    return html_value
