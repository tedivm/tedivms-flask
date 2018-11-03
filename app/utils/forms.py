from flask_wtf import FlaskForm

from wtforms import SubmitField, validators, SelectMultipleField
from wtforms.widgets import CheckboxInput, ListWidget


class MultiCheckboxField(SelectMultipleField):
    """
    A multiple-select, except displays a list of checkboxes.

    Iterating the field will produce subfields, allowing custom rendering of
    the enclosed checkbox fields.
    """
    widget = ListWidget(prefix_label=False)
    option_widget = CheckboxInput()

class ConfirmationForm(FlaskForm):
    submit = SubmitField('Confirm')
