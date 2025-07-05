from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FloatField, DateField, SelectField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, Length
from .models import User

class RegistrationForm(FlaskForm):
    username = StringField('Usuario', validators=[DataRequired(), Length(min=4, max=25)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Contrasena', validators=[DataRequired(), Length(min=6)])
    password2 = PasswordField('Repetir Contrasena', validators=[DataRequired(), EqualTo('password', message='Las contrasenas deben coincidir.')])
    submit = SubmitField('Registrarse')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Este nombre de usuario ya esta en uso.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Esta direccion de email ya esta en uso.')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Contrasena', validators=[DataRequired()])
    remember_me = BooleanField('Recuerdame')
    submit = SubmitField('Iniciar Sesion')

class TransactionForm(FlaskForm):
    description = StringField('Descripcion', validators=[DataRequired()])
    amount = FloatField('Monto', validators=[DataRequired(message="El monto no puede estar vacio.")])
    date = DateField('Fecha', format='%Y-%m-%d', validators=[DataRequired()])
    type = SelectField('Tipo', choices=[('ingreso', 'Ingreso'), ('gasto', 'Gasto')], validators=[DataRequired()])
    submit = SubmitField('Guardar Transaccion')





