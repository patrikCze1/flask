from os import environ


class Config():
    SECRET_KEY = environ.get('SECRET_KEY') #secret key
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db' #db config
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = environ.get('EMAIL_USER')
    MAIL_PASSWORD = environ.get('EMAIL_PASS')