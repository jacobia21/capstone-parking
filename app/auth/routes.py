""" This module holds all the route controllers for the auth package. """
from flask import render_template, flash, redirect, url_for
from flask import request
from flask_login import current_user, login_user, logout_user
from werkzeug.urls import url_parse

from app import db
from app.auth import bp
from app.auth.email import send_password_reset_email
from app.auth.forms import LoginForm, RequestResetPasswordForm, ResetPasswordForm, ActivateUserForm
from app.models import User


@bp.route('/login', methods=["GET", 'POST'])
def login():
    """ Logs in an administrator """

    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return render_template("login.html", title="Login", form=form, error=1)
        login_user(user, remember=form.remember_me.data)
        flash('Welcome back!')
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('admin.home')
        return redirect(next_page)
    return render_template("login.html", title="Login", form=form)


@bp.route('/logout')
def logout():
    """ Logs out an administrator. """

    logout_user()
    return redirect(url_for('main.index'))


@bp.route('/forgot', methods=["GET", "POST"])
def forgot():
    """ 

    Allows an administrator to state they forgot their password,
    triggering a email for further instructions on how to reset their password.

    """

    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RequestResetPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash('Check your email for the instructions to reset your password')
        return redirect(url_for('auth.login'))
    return render_template('forgot.html', title='Reset Password', form=form)


@bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    """ 
    Resets an administrators password.

    :param token: The token generated for the admin when they requested to reset their password.
    :type token: str

    """
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('main.index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset.')
        return redirect(url_for('auth.login'))
    return render_template('reset_password.html', form=form)


@bp.route('/activate_account/<token>', methods=['GET', 'POST'])
def activate_account(token):
    """
    Allows a new administrator to set their password.

    :param token: The token generated when a super administrator creates the new administrator's account.
    :type token: str

    """
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    user = User.verify_activation_token(token)

    if not user:
        return redirect(url_for('main.index'))
    form = ActivateUserForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('You have successfully activated your account!')
        return redirect(url_for('auth.login'))
    return render_template('activate_account.html', form=form)
