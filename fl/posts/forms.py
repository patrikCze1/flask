from flask_wtf import FlaskForm
from wtforms import StringField, validators, SubmitField, TextAreaField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from fl.models import Category


def getCategories():
    return Category.query.all()


class CreatePost(FlaskForm):
    title = StringField('Title', [validators.DataRequired()])
    text = TextAreaField('Text', [validators.DataRequired()])
    category = QuerySelectField('Category', query_factory=getCategories, get_pk=lambda item: item.id)
    submit = SubmitField('Send')


class UpdatePost(FlaskForm):
    title = StringField('Title', [validators.DataRequired()])
    text = TextAreaField('Text', [validators.DataRequired()])
    submit = SubmitField('Update')