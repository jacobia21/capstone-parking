from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, HiddenField, SelectMultipleField, widgets
from wtforms.validators import DataRequired,Email, ValidationError
from app.models import User, Zone, Lot


def validate_name(form,_):
        user = User.query.filter_by(first_name=form.first_name.data).filter_by(last_name=form.last_name.data).filter_by(middle_initial= form.middle_initial.data).first()
        if user is not None:
            raise ValidationError('This person is already an administrator.')

class MultiCheckboxField(SelectMultipleField):
    """
    A multiple-select, except displays a list of checkboxes.

    Iterating the field will produce subfields, allowing custom rendering of
    the enclosed checkbox fields.
    """
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

class AddAdminForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    first_name = StringField('First Name',validators=[DataRequired(),validate_name])
    last_name = StringField('Last Name', validators=[DataRequired(), validate_name])
    middle_initial = StringField('Middle Initial', validators=[DataRequired(), validate_name])
    group = SelectField(u'Admin Type', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Add Aministrator')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

class EditAdminForm(FlaskForm):
    #BUG an error occurs if the edited information is unique to another row in the table
    # this should be addressed by checking to see if there are any users besides the one
    # being updated with the same information
    email = StringField('Email', validators=[DataRequired(), Email()])
    first_name = StringField('First Name',validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    middle_initial = StringField('Middle Initial', validators=[DataRequired()])
    group = SelectField(u'Admin Type', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Edit Aministrator')

class AddZoneForm(FlaskForm):
    name = StringField('Zone Name', validators=[DataRequired()])
    color = StringField('Zone Color',validators=[DataRequired()])
    submit = SubmitField('Add Zone')
    
    def validate_name(self, name):
        zone = Zone.query.filter_by(name=name.data).first()
        if zone is not None:
            raise ValidationError('Please use a unique zone name.')

    def validate_color(self, color):
        color = Zone.query.filter_by(color=color.data).first()
        if color is not None:
            raise ValidationError('Please use a unique zone color.')

class EditZoneForm(FlaskForm):
    zone_id = HiddenField()
    name = StringField('Zone Name', validators=[DataRequired()])
    color = StringField('Zone Color',validators=[DataRequired()])
    submit = SubmitField('Edit Zone')
    
    def validate_name(self, name):
        zone = Zone.query.filter_by(name=name.data).filter(Zone.id != self.zone_id.data).first()
        if zone is not None:
            raise ValidationError('Please use a unique zone name.')

    def validate_color(self, color):
        color = Zone.query.filter_by(color=color.data).filter(Zone.id != self.zone_id.data).first()
        if color is not None:
            raise ValidationError('Please use a unique zone color.')

class AddLotForm(FlaskForm):
    name = StringField('Lot Name', validators=[DataRequired()])
    zones = MultiCheckboxField(u'Allowed Zones', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Add Lot')
    
    def validate_name(self, name):
        lot = Lot.query.filter_by(name=name.data).first()
        if lot is not None:
            raise ValidationError('Please use a unique lot name.')


class AddLotForm(FlaskForm):
    name = StringField('Lot Name', validators=[DataRequired()])
    zones = MultiCheckboxField(u'Allowed Zones', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Add Lot')
    
    def validate_name(self, name):
        lot = Lot.query.filter_by(name=name.data).first()
        if lot is not None:
            raise ValidationError('Please use a unique zone name.')

class EditLotForm(FlaskForm):
    name = StringField('Lot Name', validators=[DataRequired()])
    zones = MultiCheckboxField(u'Allowed Zones', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Add Lot')
    
    def validate_name(self, name):
        lot = Lot.query.filter_by(name=name.data).first()
        if lot is not None:
            raise ValidationError('Please use a unique zone name.')