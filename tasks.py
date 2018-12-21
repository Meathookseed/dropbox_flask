from factory import create_celery_app
from flask_mail import Message
from app.extensions import mail

celery = create_celery_app()

@celery.task
def send_email():
        msg = Message('Registration at flask_dropbox',
                      sender='shokran1337@gmail.com',
                      recipients=['shokran1337@gmail.com'])
        msg.html = '<h1>Hello , your email is </h1>'

        mail.send(msg)
