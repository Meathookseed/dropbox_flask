from celery_worker import worker
from app.extensions import mail
from flask_mail import Message
from main import app


@worker.task
def send_email():
    with app.app_context():
            msg = Message('Registration at flask_dropbox',
                          sender='shokran1337@gmail.com',
                          recipients=['shokran1337@gmail.com'])
            msg.html = '<h1>Hello , your email is </h1>'
            mail.send(msg)
