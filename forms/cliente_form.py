from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, SubmitField
from wtforms.validators import DataRequired, Length, Email


class ClienteForm(FlaskForm):

    nombre = StringField(
        'Nombre completo',
        validators=[
            DataRequired(message='El nombre es obligatorio.'),
            Length(
                min=3,
                max=100,
                message='El nombre debe tener entre 3 y 100 caracteres.'
            )
        ]
    )

    correo = EmailField(
        'Correo electronico',
        validators=[
            DataRequired(message='El correo es obligatorio.'),
            Email(message='Ingrese un correo electronico valido.')
        ]
    )

    telefono = StringField(
        'Telefono',
        validators=[
            DataRequired(message='El telefono es obligatorio.'),
            Length(
                min=7,
                max=20,
                message='El telefono debe tener entre 7 y 20 caracteres.'
            )
        ]
    )

    submit = SubmitField('Registrar cliente')
