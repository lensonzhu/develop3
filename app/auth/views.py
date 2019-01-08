from flask import render_template
from . import auth
from app.main.forms import NameForm
from flask import render_template,redirect,request,url_for,flash
from flask.ext.login import login_user
from . import auth
from .. models import User
from . forms import LoginForm,RegistrationForm
from flask.ext.login import logout_user,login_required


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form=RegistrationForm()
    if form.validate_on_submit():
        user=User(email=form.email.data,username=form.username.data,password=form.password.data)
        db.session.add(user)
        flash('You can now to login.')
        return redirect(url_fot('auth.login'))
    return render_template('auth/register.html',form=form)


@auth.route('/login',methods=['GET','POST'])
def login():
    form=LoginForm()
    print('~~~~~~~~~~~~~~~~~form=',form)
    if form.validate_on_submit():
        user=User.query.filter_by(email=form.email.data).first()
        print('============pass validate',user)
        if user is not None and user.verify_password(form.password.data):
            login_user(user,form.remember_me.data)
            return redirect(request.args.get('next') or url_for('main.index'))
            print('------------------pass login')
        flash('Invalid username or password.')
    return render_template('auth/login.html',form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been loget out.')
    return redirect(url_for('main.index'))

