from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, RadioField
from flaskapp.complexFields import MultiCheckboxField
from wtforms.validators import DataRequired, length, Email, EqualTo, ValidationError
from flaskapp.models import User
from flask_login import current_user
from datetime import datetime as dt
from flaskapp import db


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), length(min=2, max=20)])

    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password',
                             validators=[DataRequired()])

    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])

    location_choices = [('Washington, DC', 'Washington, DC'),
                        ('New York City, NY', 'New York City, NY')]

    location = SelectField('Location', choices=location_choices, )

    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password',
                             validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    location_choices = [
        ('Washington, DC', 'Washington, DC'),
        ('New York City, NY', 'New York City, NY')]

    location = SelectField('Location', choices=location_choices, validators=[DataRequired()])

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')


class SampleForm(FlaskForm):
    gender_list = [('M', 'Male', 'secondary'), ('F', 'Female', 'secondary')]

    age_list = [
        (1, '0-18', 'success'), (2, '19-25', 'success'),
        (3, '26-30', 'success'), (4, '31-40', 'success'),
        (5, '41-50', 'success'), (6, '51-65', 'success'),
        (7, '65-74', 'success'), (8, '75+', 'success')
    ]

    rating_list = [
        (4, 'Great', 'warning'), (3, 'Good', 'warning'),
        (2, 'Poor', 'warning'), (1, 'Very Poor', 'warning')
    ]

    purchase_list = [(True, 'Purchase', 'success'), (False, 'No Purchase', 'success')]

    survey_questions = {
        'Gender': gender_list,
        'Age': age_list,
        'Rating': rating_list,
        'Purchase': purchase_list
    }

    submit = SubmitField('Send Sample')

    '''
    NOTES ON RADIO BUTTONS
    - https://gist.github.com/doobeh/4667330
    '''


class AddUsersForm(FlaskForm):
    # decide whether to verify or remove users
    choices = [('verify', 'Verify'), ('remove', 'Remove')]
    verify_or_remove = RadioField('VerifyOrRemove', choices=choices)

    # verify and remove buttons
    submit = SubmitField('Submit')

    remove_verified = BooleanField('Confirm Removal')

    def add_users(self, selections):
        for selection in selections:
            editable_user = User.query.filter_by(id=selection).first()
            editable_user.verified = True
            db.session.commit()

    def remove_users(self, selections):
        for selection in selections:
            editable_user = User.query.filter_by(id=selection).first()
            db.session.delete(editable_user)
            db.session.commit()
