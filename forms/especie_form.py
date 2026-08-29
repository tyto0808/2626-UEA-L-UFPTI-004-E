# -*- coding: utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, IntegerField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange


class EspecieForm(FlaskForm):

    familia = StringField(
        'Familia',
        validators=[
            DataRequired(message='La familia es obligatoria.'),
            Length(min=3, max=50, message='La familia debe tener entre 3 y 50 caracteres.')
        ]
    )

    genero = StringField(
        'Genero',
        validators=[
            DataRequired(message='El genero es obligatorio.'),
            Length(min=2, max=50, message='El genero debe tener entre 2 y 50 caracteres.')
        ]
    )

    especie = StringField(
        'Especie',
        validators=[
            DataRequired(message='La especie es obligatoria.'),
            Length(min=2, max=80, message='La especie debe tener entre 2 y 80 caracteres.')
        ]
    )

    microhabitat = SelectField(
        'Microhabitat',
        choices=[
            ('', 'Seleccione un microhabitat'),
            ('Arbustos', 'Arbustos'),
            ('Hojarasca', 'Hojarasca'),
            ('Suelo', 'Suelo'),
            ('Troncos', 'Troncos')
        ],
        validators=[
            DataRequired(message='Seleccione un microhabitat.')
        ]
    )

    temporada = SelectField(
        'Temporada',
        choices=[
            ('', 'Seleccione una temporada'),
            ('Invierno', 'Invierno'),
            ('Verano', 'Verano')
        ],
        validators=[
            DataRequired(message='Seleccione una temporada.')
        ]
    )

    tipo_monitoreo = SelectField(
        'Tipo de monitoreo',
        choices=[
            ('', 'Seleccione el tipo de monitoreo'),
            ('Diurno', 'Diurno'),
            ('Nocturno', 'Nocturno')
        ],
        validators=[
            DataRequired(message='Seleccione el tipo de monitoreo.')
        ]
    )

    cantidad = IntegerField(
        'Numero de individuos',
        validators=[
            DataRequired(message='La cantidad es obligatoria.'),
            NumberRange(min=1, max=1000, message='La cantidad debe estar entre 1 y 1000.')
        ]
    )

    observaciones = TextAreaField(
        'Observaciones',
        validators=[
            Length(max=500, message='Las observaciones no pueden superar los 500 caracteres.')
        ]
    )

    submit = SubmitField('Registrar especie')
