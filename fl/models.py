from fl import db, loginManager
from datetime import datetime
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app as app

 
#terminal
'''
python3
from fl import createApp, db
db.create_all() #create db
from fl.models import User
admin = User(name='admin', email='admin@example.com')
db.session.add(admin)
db.session.commit() #commit data
User.query.all() #query
'''


@loginManager.user_loader
def loadUser(id):
    return User.query.get(int(id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True) 
    name = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.png')
    password = db.Column(db.String(60), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    active = db.Column(db.Boolean, unique=False, default=True)
    posts = db.relationship('Post', backref='author', lazy=True)
    last_login = db.Column(db.DateTime, nullable=True, default=datetime.utcnow)
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'))
    #notifications = db.relationship('Notification', backref='owner', lazy=True)

    def getResetToken(self, expires_sec=1800):#model functions
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod #without self arg
    def verifyResetToken(token):
        s = Serializer(app.config['SECRET_KEY'])

        try:
            userId = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(userId)

    def __repr__(self):
        return f'User {self.name} - {self.email}'

    def getRole(self):
        pass#get role of user -> template admin section


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    active = db.Column(db.Boolean, unique=False, default=True)
    approved = db.Column(db.Boolean, unique=False, default=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)

    def __repr__(self):
        return f'Post {self.title} - {self.created_at}'


class Block(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    reason = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    until = db.Column(db.DateTime, nullable=False)


class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=True)
    active = db.Column(db.Boolean, unique=False, default=True)
    description = db.Column(db.String(255), nullable=True)
    users = db.relationship('User', backref='users', lazy=True)

    def __repr__(self):
        return self.name


class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    active = db.Column(db.Boolean, unique=False, default=True)
    value = db.Column(db.Integer, nullable=False)
    groups = db.relationship('Group', backref='groups', lazy=True)
    description = db.Column(db.String(255), nullable=True)

    def __repr__(self):
        return f'{self.name} - {self.value}'


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    posts = db.relationship('Post', backref='posts', lazy=True)

    def __repr__(self):
        return self.name

'''
class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    viewed = db.Column(db.Boolean, unique=False, default=False)
    text = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
'''