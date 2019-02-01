from flask_mail import Message

from app.extensions import mail
from factory import create_celery_app

celery = create_celery_app()


@celery.task
def send_email(data: dict):
        msg = Message('Registration at flask_dropbox',
                      sender='shokran1337@gmail.com',
                      recipients=[data['email']])
        msg.html = f'<h1>Hello {data["username"]} , you just registered in dropbox_flask </h1>'

        mail.send(msg)
