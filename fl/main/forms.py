from flask_wtf import FlaskForm
from wtforms import StringField, validators, SubmitField, TextAreaField


class ContactForm(FlaskForm):
    email = StringField('Email Address', [validators.Required(), validators.Email()])
    title = StringField('Title', [validators.Required()])
    text = TextAreaField('Message', [validators.Required()])
    submit = SubmitField('Send')