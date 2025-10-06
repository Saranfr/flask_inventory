from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, SelectField, DateTimeField
from wtforms.validators import DataRequired, Optional, ValidationError
from datetime import datetime

class ProductForm(FlaskForm):
    product_id = StringField('Product ID', validators=[DataRequired()])
    name = StringField('Product Name', validators=[DataRequired()])
    description = TextAreaField('Description')

class LocationForm(FlaskForm):
    location_id = StringField('Location ID', validators=[DataRequired()])
    name = StringField('Location Name', validators=[DataRequired()])

class ProductMovementForm(FlaskForm):
    movement_id = StringField('Movement ID', validators=[DataRequired()])
    product_id = SelectField('Product', validators=[DataRequired()], coerce=str)
    from_location = SelectField('From Location', validators=[Optional()], coerce=str)
    to_location = SelectField('To Location', validators=[Optional()], coerce=str)
    qty = IntegerField('Quantity', validators=[DataRequired()])
    timestamp = DateTimeField('Timestamp', format='%Y-%m-%d %H:%M:%S', default=datetime.now)
    
    def validate(self, extra_validators=None):
        if not super().validate(extra_validators):
            return False
        
        if not self.from_location.data and not self.to_location.data:
            self.from_location.errors.append('At least one of From Location or To Location must be filled')
            return False
        
        if self.from_location.data and self.to_location.data and self.from_location.data == self.to_location.data:
            self.to_location.errors.append('From and To locations must be different')
            return False
        
        return True
