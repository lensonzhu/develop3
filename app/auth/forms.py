from flask.ext.wtf import Form
from wtforms import StringField,PasswordField,BooleanField,SubmitField
from wtforms.validators import Required,Length,Email
from wtforms import ValidationError
from .. models import User

'''
class RegistrationForm(Form):
    email=StringField('Email',validators=[Required(),Length(1,64),Email()])
    password=PasswordField('Password',validators=[Required(),EqualTo('password2',message='Passwords must be match.')])
    password2=PasswordField('Confirm password',validators=[Required()])
    submit=SubmitField('Register')

    def validate_email(self,field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')

    def validate_username(self,field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use.')

'''

class LoginForm(Form):
    email=StringField('Email',validators=[Required(),Length(1,64),Email()])
    password=PasswordField('password',validators=[Required()])
    remember_me=BooleanField('Keep me Logged in')
    submit=SubmitField('Log In')
