from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, validators, SubmitField, IntegerField, TextAreaField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.fields.html5 import DateTimeLocalField
from fl.models import Group, Role, User


def getRoles():
    return Role.query.all()


def getUsers():
    return User.query.all()


class BlockUser(FlaskForm):
    reason = StringField('Reason', [validators.DataRequired()])
    until = DateTimeLocalField('Until', [validators.DataRequired()], format='%Y-%m-%dT%H:%M')
    submit = SubmitField('Submit')


class SearchForm(FlaskForm):
    name = StringField('Name')
    email = StringField('Email')
    submit = SubmitField('Filter')


class CreateGroupForm(FlaskForm):
    name = StringField('Name', [validators.DataRequired()])
    active = BooleanField('Active', default=True)
    description = TextAreaField('Description', [validators.Length(max=254)])
    role = QuerySelectField('Role', query_factory=getRoles, allow_blank=True, get_pk=lambda item: item.id)
    submit = SubmitField('Create')

    def validate_name(self, name):
        group = Group.query.filter_by(name=name.data).first()

        if group:
            raise validators.ValidationError('Name already exists')

    
class UpdateGroupForm(FlaskForm):
    name = StringField('Name', [validators.DataRequired()])
    active = BooleanField('Active', default=True)
    description = TextAreaField('Description', [validators.Length(max=254)])
    role = QuerySelectField('Role', query_factory=getRoles, allow_blank=True, get_pk=lambda item: item.id)
    submit = SubmitField('Update')


class AddUserIntoGroup(FlaskForm):
    user = QuerySelectField('User', query_factory=getUsers, allow_blank=True, get_pk=lambda item: item.id)
    submit = SubmitField('Add')


class CreateRoleForm(FlaskForm):
    name = StringField('Name', [validators.DataRequired()])
    active = BooleanField('Active', default=True)
    value = IntegerField('Value', [validators.DataRequired()])
    description = TextAreaField('Description', [validators.Length(max=254)])
    submit = SubmitField('Create')

    def validate_name(self, name):
        role = Role.query.filter_by(name=name.data).first()

        if role:
            raise validators.ValidationError('Name already exists')


class UpdateRoleForm(FlaskForm):
    name = StringField('Name', [validators.DataRequired()])
    active = BooleanField('Active', default=True)
    value = IntegerField('Value', [validators.DataRequired()])
    description = TextAreaField('Description', [validators.Length(max=254)])
    submit = SubmitField('Update')


class CreateCategoryForm(FlaskForm):
    name = StringField('Name', [validators.DataRequired()])
    submit = SubmitField('Create')

    def validate_name(self, name):
        role = Role.query.filter_by(name=name.data).first()

        if role:
            raise validators.ValidationError('Name already exists')