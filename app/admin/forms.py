from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired,Email, ValidationError
from app.models import User


def validate_name(form,_):
        user = User.query.filter_by(first_name=form.first_name.data).filter_by(last_name=form.last_name.data).filter_by(middle_initial= form.middle_initial.data).first()
        if user is not None:
            raise ValidationError('This person is already an administrator.')

class AddAdminForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    first_name = StringField('First Name',validators=[DataRequired(),validate_name])
    last_name = StringField('Last Name', validators=[DataRequired(), validate_name])
    middle_initial = StringField('Middle Initial', validators=[DataRequired(), validate_name])
    submit = SubmitField('Add Aministrator')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

class EditAdminForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    first_name = StringField('First Name',validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    middle_initial = StringField('Middle Initial', validators=[DataRequired()])
    submit = SubmitField('Edit Aministrator')