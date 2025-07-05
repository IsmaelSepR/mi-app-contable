from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FloatField, DateField, SelectField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, Length
from .models import User

class RegistrationForm(FlaskForm):
    username = StringField('Usuario', validators=[DataRequired(), Length(min=4, max=25)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Contrase�a', validators=[DataRequired(), Length(min=6)])
    password2 = PasswordField('Repetir Contrase�a', validators=[DataRequired(), EqualTo('password', message='Las contrase�as deben coincidir.')])
    submit = SubmitField('Registrarse')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Este nombre de usuario ya est� en uso.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Esta direcci�n de email ya est� en uso.')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Contrase�a', validators=[DataRequired()])
    remember_me = BooleanField('Recu�rdame')
    submit = SubmitField('Iniciar Sesi�n')

class TransactionForm(FlaskForm):
    description = StringField('Descripci�n', validators=[DataRequired()])
    amount = FloatField('Monto', validators=[DataRequired(message="El monto no puede estar vac�o.")])
    date = DateField('Fecha', format='%Y-%m-%d', validators=[DataRequired()])
    type = SelectField('Tipo', choices=[('ingreso', 'Ingreso'), ('gasto', 'Gasto')], validators=[DataRequired()])
    submit = SubmitField('Guardar Transacci�n')
