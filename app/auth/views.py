from flask import render_template,redirect,request,url_for,flash
from . import auth
from .. import db
from .. models import User
from ..email import send_email
from . forms import LoginForm,RegistrationForm,ChangePasswordForm
from flask_login import login_user,logout_user,login_required,current_user


@auth.route('/update_password',methods=['GET','POST'])
@login_required
def update_password():
    form=ChangePasswordForm()
    if form.validate_on_submit():
        #print('pass_validate=============',form)
        if current_user.verify_password(form.old_password.data):
            current_user.password=form.password.data
            db.session.add(current_user)
            logout_user()
            #print('add_user_success===============',current_user)
            flash('Your password has been updated.')
            return redirect(url_for('auth.login'))

        flash('Invalid password try again')
        return redirect(url_for('main.index'))
    print('form========')
    return render_template('auth/update_password.html',form=form)


@auth.route('/confirm')
@login_required
def resend_confirmation():
    token=current_user.generate_confirmation_token()
    send_email(current_user.email,'Confirm Your Account','auth/email/confirm',user=current_user,token=token)
    flash('A new confirmation email has been sent to you by email.')
    return redirect(url_for('main.index'))


@auth.before_app_request
def before_request():
    if current_user.is_authenticated and not current_user.confirmed and request.endpoint[:5] !='auth.' and request.endpoint !='static':
        return redirect(url_for('auth.unconfirmed'))

@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))
    print('unconfirmed============')
    return render_template('auth/unconfirmed.html')


@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        flash('You have confirmed your account.Thanks!')
    else:
        flash('The confirmation link is invalid or has expired')
    return redirect(url_for('main.index'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form=RegistrationForm()
    if form.validate_on_submit():
        user=User(email=form.email.data,username=form.username.data,password=form.password.data)

        db.session.add(user)
        db.session.commit()
        token=user.generate_confirmation_token()
        send_email(user.email,'Confirm your Account','auth/email/confirm',user=user,token=token)
        print('email============',user.email)
        flash('A confirmation email has been sent to you by email You can now to login.')
        return redirect(url_for('main.index'))
    return render_template('auth/register.html',form=form)


@auth.route('/login',methods=['GET','POST'])
def login():
    form=LoginForm()
   # print('~~~~~~~~~~form=',form)
    if form.validate_on_submit():
        user=User.query.filter_by(email=form.email.data).first()
       # print('=========user=',user)
        if user is not None and user.verify_password(form.password.data):
           # print('=========user=',user)

            login_user(user,form.remember_me.data)
            print('--------',user.email)
            return redirect(request.args.get('next') or url_for('main.index'))
        #print('Invalid username or password.')
        flash('Invalid username or password.')
    return render_template('auth/login.html',form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been loget out.')
    return redirect(url_for('main.index'))

