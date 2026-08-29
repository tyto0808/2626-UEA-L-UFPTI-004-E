from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange


class ProductoForm(FlaskForm):

    nombre = StringField(
        'Nombre del producto',
        validators=[
            DataRequired(message='El nombre es obligatorio.'),
            Length(min=3, max=100, message='El nombre debe tener entre 3 y 100 caracteres.')
        ]
    )

    categoria = StringField(
        'Categoria',
        validators=[
            DataRequired(message='La categoria es obligatoria.'),
            Length(min=3, max=50, message='La categoria debe tener entre 3 y 50 caracteres.')
        ]
    )

    precio = FloatField(
        'Precio',
        validators=[
            DataRequired(message='El precio es obligatorio.'),
            NumberRange(min=0.01, message='El precio debe ser mayor que 0.')
        ]
    )

    cantidad = IntegerField(
        'Cantidad',
        validators=[
            DataRequired(message='La cantidad es obligatoria.'),
            NumberRange(min=1, message='La cantidad debe ser mayor o igual a 1.')
        ]
    )

    submit = SubmitField('Registrar producto')
