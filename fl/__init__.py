from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from fl.config import Config


db = SQLAlchemy()
bcrypt = Bcrypt()
loginManager = LoginManager()
loginManager.login_view = 'users.login'
loginManager.login_message_category = 'info'
mail = Mail()


def createApp(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)#set config

    db.init_app(app)
    bcrypt.init_app(app)
    loginManager.init_app(app)
    mail.init_app(app)

    #import routes
    from fl.users.routes import users
    from fl.posts.routes import posts
    from fl.main.routes import main
    from fl.admin.routes import admin
    
    from fl.errors.handlers import errors

    #register blueprint
    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(admin)
    app.register_blueprint(errors)

    return app