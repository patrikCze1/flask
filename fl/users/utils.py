from PIL import Image
from flask_mail import Message
from flask import current_app as app
from fl import  mail
from fl.models import Block
from fl.users.forms import ResetPasswordForm, RequestResetForm
from datetime import datetime
import secrets
import os


def sendEmail(user):
    token = user.getResetToken()
    msg = Message('Password reset request', recipients=[user.email], sender='noreply@app.com')
    msg.body = '''To reset your password follow this link
    {url_for('resetPassword', token, _external=True)}
    If you not make this request, please ignore this message.
    '''
    mail.send(msg)


def saveImage(image):
    name = secrets.token_hex(8)
    _, fileExt = os.path.splitext(image.filename)
    newFileName = name + fileExt
    imagePath = os.path.join(app.root_path, 'static/pictures', newFileName)
    finalSize = (125, 125)
    i = Image.open(image)
    i.thumbnail(finalSize)
    i.save(imagePath)#save resized image with new path and name // or image.save(path)
    
    return newFileName


def checkIfUserIsBlocked(user):
    block = Block.query.filter(Block.user_id==user.id).filter(Block.until>=datetime.now()).all()
    
    if block:
        return block[0].until
    else:
        return None


def deleteImage(image):
    imagePath = os.path.join(app.root_path, 'static/pictures', image)
    os.remove(imagePath)