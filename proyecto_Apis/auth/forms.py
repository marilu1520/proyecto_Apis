from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
from models import db, User

class LoginForm(FlaskForm):
    username = StringField('Usuario', validators=[DataRequired()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    remember_me = BooleanField('Recordarme')
    submit = SubmitField('Ingresar')

class RegistrationForm(FlaskForm):
    username = StringField('Usuario', validators=[DataRequired(), Length(1, 64)])
    password = PasswordField('Contraseña', validators=[
        DataRequired(), 
        EqualTo('password2', message='Las contraseñas deben coincidir.')
    ])
    password2 = PasswordField('Confirmar contraseña', validators=[DataRequired()])
    submit = SubmitField('Registrarse')

    def validate_username(self, field):
        usuario_existente = db.session.scalar(db.select(User).filter_by(username=field.data))
        if usuario_existente:
            raise ValidationError('El nombre de usuario ya está registrado.')