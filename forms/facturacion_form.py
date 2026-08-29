from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, IntegerField, SubmitField
from wtforms.validators import DataRequired, NumberRange


class FacturacionForm(FlaskForm):

    cliente = StringField(
        'Cliente',
        validators=[
            DataRequired(message='El cliente es obligatorio.')
        ]
    )

    producto = StringField(
        'Producto',
        validators=[
            DataRequired(message='El producto es obligatorio.')
        ]
    )

    cantidad = IntegerField(
        'Cantidad',
        validators=[
            DataRequired(message='La cantidad es obligatoria.'),
            NumberRange(
                min=1,
                message='La cantidad debe ser mayor o igual a 1.'
            )
        ]
    )

    total = FloatField(
        'Total',
        validators=[
            DataRequired(message='El total es obligatorio.'),
            NumberRange(
                min=0.01,
                message='El total debe ser mayor que 0.'
            )
        ]
    )

    submit = SubmitField('Registrar factura')
