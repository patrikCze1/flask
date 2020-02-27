from flask_mail import Message
from fl import mail


def sendEmail(email, title, text):
    msg = Message('Question', recipients=['default@email.com'], sender=email)
    msg.body = f'{title} <br> {text}'
    mail.send(msg)