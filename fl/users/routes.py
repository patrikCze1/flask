from flask import Blueprint, render_template, url_for, request, redirect, flash
from flask_login import login_user, current_user, logout_user, login_required
from fl import db, bcrypt, mail
from fl.models import User
from fl.users.forms import RegistrationForm, LoginForm, UpdateAccountForm, ChangePasswordForm, RequestResetForm, ResetPasswordForm
from datetime import datetime
from fl.users.utils import saveImage, checkIfUserIsBlocked, sendEmail, deleteImage

users = Blueprint('users', __name__)

@users.route('/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    form = LoginForm(request.form)
    if request.method == 'POST':
        user = User.query.filter_by(email=form.email.data).first()

        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            banned = checkIfUserIsBlocked(current_user)
            if banned:
                flash(f'You has been banned to {banned}', 'info') 
                logout()
            else:
                nextPage = request.args.get('next')
                flash(f'Last login: {current_user.last_login.strftime("%d/%m/%Y %H:%M:%S")}', 'info') 
                current_user.last_login = datetime.now()
                db.session.commit()
                return redirect(nextPage) if nextPage else redirect(url_for('main.home'))
        else:
            flash('Invalid email or password', 'danger')
    # the code below is executed if the request method
    # was GET or the credentials were invalid
    return render_template('./auth/login.html', title='Login', form=form)


@users.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    form = RegistrationForm()
    if request.method == 'POST' and form.validate():
        hsPassword = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(name=form.username.data, email=form.email.data, password=hsPassword)
        db.session.add(user)
        db.session.commit()
        flash(f'Thanks for registering {form.username.data}', 'success')
        return redirect(url_for('users.login'))
    return render_template('./auth/register.html', title='Register', form=form)


@users.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@users.route('/user/<int:id>')
@login_required
def userProfile(id):
    user = User.query.get_or_404(id)
    return render_template('./account/profile.html', title=f'{user.name} profile', user=user)


@users.route('/updateUser', methods=['GET', 'POST'])
@login_required
def updateUser():
    form = UpdateAccountForm()
    if request.method == 'POST' and form.validate():#update current user
        
        if form.image.data:
            if current_user.image_file is not 'default.png':
                deleteImage(current_user.image_file)

            image_file = saveImage(form.image.data)
            current_user.image_file = image_file

        db.session.commit()#save
        flash('Account has been updated', 'success')
        return redirect(url_for('users.userProfile', id=current_user.id))
    else:
        #form.username.data = current_user.name
        #form.email.data = current_user.email
        return render_template('./account/update.html', title='Update profile', form=form)


@users.route('/changePassword', methods=['GET', 'POST'])
@login_required
def changePassword():
    form = ChangePasswordForm()
    if request.method == 'POST' and form.validate():
        hsPassword = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        current_user.password = hsPassword
        db.session.commit()#save
        flash('Password has been updated', 'success')
        return redirect(url_for('users.userProfile', id=current_user.id))
    else:
        return render_template('./account/password.html', title='Change password', form=form)


@users.route('/resetRequest', methods=['GET', 'POST'])
def resetRequest():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    form = RequestResetForm()

    if form.validate_on_submit():#post
        user = User.query.filter_by(email=form.email.data).first()
        sendEmail(user)
        flash('Email has been send', 'info')
        return redirect(url_for('login'))
    return render_template('./auth/resetRequest.html', title='Reset password', form=form)


@users.route('/resetPassword/<token>', methods=['GET', 'POST'])
def resetPassword(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    user = User.verifyRestToken(token)

    if user is None:
        flash('Token expired', 'warning')
        return redirect(url_for('login'))

    form = ResetPasswordForm()
    if form.validate():
        hsPassword = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hsPassword
        db.session.commit()
        flash('Password has been reseted', 'success')
        return redirect(url_for('login'))
    return render_template('./auth/resetPassword.html', title='Reset password', form=form)
