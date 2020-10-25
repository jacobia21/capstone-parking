from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, HiddenField, \
    SelectMultipleField, IntegerField, widgets
from wtforms.validators import DataRequired, Email, IPAddress, ValidationError

from app.models import Administrator, Zone, Lot, Camera


def validate_name(form, _):
    user = Administrator.query.filter_by(first_name=form.first_name.data).filter_by(
        last_name=form.last_name.data).filter_by(middle_initial=form.middle_initial.data).first()
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
    first_name = StringField('First Name', validators=[
        DataRequired(), validate_name])
    last_name = StringField('Last Name', validators=[
        DataRequired(), validate_name])
    middle_initial = StringField('Middle Initial', validators=[
        DataRequired(), validate_name])
    group = SelectField(u'Admin Type', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Add Administrator')

    def validate_email(self, email):
        user = Administrator.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')


class EditAdminForm(FlaskForm):
    user_id = HiddenField(validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    middle_initial = StringField('Middle Initial', validators=[DataRequired()])
    group = SelectField(u'Admin Type', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Edit Administrator')

    def validate_email(self, email):
        admin = Administrator.query.filter_by(email=email.data).filter(
            Administrator.id != self.user_id.data).first()
        if admin is not None:
            raise ValidationError('Please use a unique email.')

    def validate_first_name(self, first_name):
        admin = Administrator.query.filter_by(first_name=first_name.data).filter_by(last_name=self.last_name.data).filter_by(
            middle_initial=self.middle_initial.data).filter(Administrator.id != self.user_id.data).first()
        if admin is not None:
            raise ValidationError('Please use a unique email.')


class AddZoneForm(FlaskForm):
    name = StringField('Zone Name', validators=[DataRequired()])
    color = StringField('Zone Color', validators=[DataRequired()])
    additional_zones = MultiCheckboxField('Additional Zones', coerce=int,
                                          description="Select any zones that drivers with this parking pass can also park in, if any.")
    lots = MultiCheckboxField(
        u'Allowed Lots', coerce=int, description="Select the lots that have specific spaces for this zone.")
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
    zone_id = HiddenField(validators=[DataRequired()])
    name = StringField('Zone Name', validators=[DataRequired()])
    color = StringField('Zone Color', validators=[DataRequired()])
    additional_zones = MultiCheckboxField('Additional Zones', coerce=int)
    lots = MultiCheckboxField(
        u'Allowed Lots', coerce=int,
        description="Select the lots that have specific spaces for this zone.")
    submit = SubmitField('Edit Zone')

    def validate_name(self, name):
        zone = Zone.query.filter_by(name=name.data).filter(
            Zone.id != self.zone_id.data).first()
        if zone is not None:
            raise ValidationError('Please use a unique zone name.')

    def validate_color(self, color):
        color = Zone.query.filter_by(color=color.data).filter(
            Zone.id != self.zone_id.data).first()
        if color is not None:
            raise ValidationError('Please use a unique zone color.')


class AddLotForm(FlaskForm):
    name = StringField('Lot Name', validators=[DataRequired()])
    submit = SubmitField('Add Lot')

    def validate_name(self, name):
        lot = Lot.query.filter_by(name=name.data).first()
        if lot is not None:
            raise ValidationError('Please use a unique zone name.')


class EditLotForm(FlaskForm):
    lot_id = HiddenField(validators=[DataRequired()])
    name = StringField('Lot Name', validators=[DataRequired()])
    submit = SubmitField('Edit Lot')

    def validate_name(self, name):
        lot = Lot.query.filter_by(name=name.data).filter(
            Lot.id != self.lot_id.data).first()
        if lot is not None:
            raise ValidationError('Please use a unique lot name.')


class AddCameraForm(FlaskForm):
    ip_address = StringField('IP Address',
                             validators=[DataRequired(), IPAddress(message="Please enter a valid IP Address")])
    location = IntegerField('Location', validators=[DataRequired()])
    status = SelectField(u'Status', validators=[DataRequired()])
    lot = SelectField(u'Lot', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Add Camera')

    def validate_ip_address(self, ip_address):
        cameras = Camera.query.filter_by(ip_address=ip_address.data).all()
        if cameras:
            raise ValidationError('Please enter a unique IP address.')

    def validate_location(self, location):
        cameras = Camera.query.filter_by(
            location=location.data).filter_by(lot_id=self.lot.data).all()

        if len(cameras) != 0:
            raise ValidationError(
                'This location is already being used by a camera in this lot')


class EditCameraZone(FlaskForm):
    camera_id = HiddenField(validators=[DataRequired()])
    location = IntegerField('Location', validators=[DataRequired()])
    status = SelectField(u'Status', validators=[DataRequired()])
    lot = SelectField(u'Lot', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Edit Camera')

    def validate_location(self, location):
        camera = Camera.query.filter_by(location=location.data).filter(
            Camera.id != self.camera_id.data).first()
        if camera is not None:
            raise ValidationError(
                'This location is already being used by a camera in this zone')
