from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,BooleanField,SubmitField
from wtforms.validators import Required,Length,Email,Regexp,EqualTo
from wtforms import ValidationError
from .. models import User


class ResetPasswordRequestForm(FlaskForm):
    email=StringField('Email',validators=[Required(),Length(1,64),Email()])
    submit=SubmitField('Reset Password')


class ResetPasswordForm(FlaskForm):
    email=StringField('Email',validators=[Required(),Length(1,64)])
    password=PasswordField('New password',validators=[Required(),EqualTo('password2',message='Password must be mach')])
    password2=PasswordField('Confirm password',validators=[Required()])
    submit=SubmitField('Reset Password')

    def validator_email(self,field):
        if User.query.filter_by(email=field.data).first() is None:
            raise ValidationError('Unknown email address')


class ChangePasswordForm(FlaskForm):
    old_password=PasswordField('Old password',validators=[Required()])
    password=PasswordField('New password',validators=[Required(),EqualTo('password2',message='Passwords must match')])
    password2=PasswordField('Confirm new password',validators=[Required()])
    submit=SubmitField('Update Password')



class RegistrationForm(FlaskForm):
    email=StringField('Email',validators=[Required(),Length(1,64),Email()])
    username=StringField('Username',validators=[Required(),Length(1,64),Regexp('^[A-Za-z][A-Za-z0-9_.]*$',0,'Username must be have only letters')])
    password=PasswordField('Password',validators=[Required(),EqualTo('password2',message='Passwords must be match.')])
    password2=PasswordField('Confirm password',validators=[Required()])
    submit=SubmitField('Register')

    def validate_email(self,field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')

    def validate_username(self,field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use.')



class LoginForm(FlaskForm):
    email=StringField('Email',validators=[Required(),Length(1,64),Email()])
    password=PasswordField('password',validators=[Required()])
    remember_me=BooleanField('Keep me Logged in')
    submit=SubmitField('Log In')
