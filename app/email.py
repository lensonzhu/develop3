from threading import Thread
from flask import current_app,render_template
from flask_mail import Message
from . import mail



def send_async_email(app,msg):
    try:
         with app.app_context():
             mail.send(msg)
    except Exception as e:
        print('your mail is wrong:',e)

def send_email(to,subject,template,**kwargs):
    try:
        app=current_app._get_current_object()
        msg=Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX']+''+subject,sender=app.config['FLASKY_MAIL_SENDER'],recipients=[to])
        msg.body = render_template(template + '.txt', **kwargs)
        msg.html = render_template(template + '.html', **kwargs)
        thr = Thread(target=send_async_email, args=[app, msg])
        thr.start()
        return thr
    except Exception as e:
        print('your email is wrong',e)
