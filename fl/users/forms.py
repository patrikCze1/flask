from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import BooleanField, StringField, PasswordField, validators, SubmitField
from fl.models import User


class RegistrationForm(FlaskForm):
    username = StringField('Username', [validators.DataRequired()])
    email = StringField('Email Address', [validators.Length(min=5, max=35), validators.Email(), validators.DataRequired()])
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match'),
        validators.Length(min=4)
    ])
    confirm = PasswordField('Repeat Password', [validators.DataRequired()])
    accept_tos = BooleanField('I accept the terms and conditions', [validators.DataRequired()])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(name=username.data).first()

        if user:
            raise validators.ValidationError('Name already exists')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()

        if user:
            raise validators.ValidationError('Email already exists')


class LoginForm(FlaskForm):
    email = StringField('Email Address', [validators.Length(min=6, max=35), validators.Email()])
    password = PasswordField('Password')
    remember = BooleanField('Remember me')
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    image = FileField('Profile picture', validators=[FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!'), validators.DataRequired()])
    submit = SubmitField('Update')


class ChangePasswordForm(FlaskForm):
    password = PasswordField('New Password', validators=[
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')
    submit = SubmitField('Change')


class RequestResetForm(FlaskForm):
    email = StringField('Email Address', [validators.DataRequired(), validators.Email()])
    submit = SubmitField('Submit')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()

        if user is None:
            raise validators.ValidationError('No Email with this address')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')
    submit = SubmitField('Reset')