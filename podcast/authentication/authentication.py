from flask import session
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, AnyOf
from password_validator import PasswordValidator
from wtforms.validators import ValidationError
from podcast.authentication.services import auth_services
import podcast.adapters.abstract_repository as repo

class PasswordValid:
    # Error message when invalid password is entered
    def __init__(self, message=None):
        if not message:
            message = (u'Your password must contain at least 8 characters, and contain an upper case letter, ' +
                       u'lower case letter and a digit')
        self.message = message

    # Password must be at least 8 characters long etc.
    def __call__(self, form, field):
        schema = PasswordValidator()
        schema \
            .min(8) \
            .has().uppercase() \
            .has().lowercase() \
            .has().digits()
        if not schema.validate(field.data):
            raise ValidationError(self.message)

class RegistrationForm(FlaskForm):

    username = StringField('Username',[
        DataRequired(message='Your username is required'),
        Length(min=3, message='Your username must be at least 3 characters')
    ])

    password = PasswordField('Password', [
        DataRequired(message='Your password is required'),
        PasswordValid()
    ])

    # Label is 'Register'
    submit = SubmitField('Register')

class LoginForm(FlaskForm):

    username = StringField('Username',[
        DataRequired(message='Your username is required'),
        Length(min=3, message='Your username must be at least 3 characters')
    ])

    # Will allow more types of passwords
    password = PasswordField('Password', [
        DataRequired(message='Your password is required'),
    ])

    submit = SubmitField('Login')
