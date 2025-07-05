from flask import Blueprint, render_template, redirect, url_for, flash
from mi_app import db
from mi_app.models import User
from mi_app.forms import LoginForm, RegistrationForm
from flask_login import login_user, logout_user, current_user

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Felicidades, te has registrado con exito! Ahora puedes iniciar sesion.', 'success')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', title='Registro', form=form)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Email o contrase�a inv�lidos.', 'danger')
            return redirect(url_for('auth.login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('main.dashboard'))
    return render_template('auth/login.html', title='Iniciar Sesi�n', form=form)

@auth_bp.route('/logout')
def logout():
    logout_user()
    flash('Has cerrado sesi�n.', 'info')
    return redirect(url_for('main.index'))
